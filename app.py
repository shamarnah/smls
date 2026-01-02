"""
Main Flask application for the Smart Library Management System (SLMS)
This is a simple web application using Flask framework.
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from models import Database, Book

# Create Flask app instance
app = Flask(__name__)
app.secret_key = 'slms_secret_key_2024'  # Secret key for sessions

# Create database instance (in-memory storage)
db = Database()


@app.route('/')
def index():
    """Home page - redirects to login"""
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page for students"""
    if request.method == 'POST':
        user_id = request.form.get('user_id', '').strip()
        password = request.form.get('password', '').strip()
        
        # Check if it's a valid student ID format
        if db.is_valid_student_id(user_id):
            student = db.get_student(user_id)
            if student.authenticate(password):
                session['user_id'] = user_id
                session['user_type'] = 'student'
                return redirect(url_for('student_dashboard'))
        
        return render_template('login.html', error='Invalid student ID or password')
    
    return render_template('login.html')


@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    """Admin login page"""
    if request.method == 'POST':
        admin_id = request.form.get('admin_id', '').strip()
        password = request.form.get('password', '').strip()
        
        admin = db.get_admin(admin_id)
        if admin and admin.authenticate(password):
            session['user_id'] = admin_id
            session['user_type'] = 'admin'
            return redirect(url_for('admin_dashboard'))
        
        return render_template('admin_login.html', error='Invalid admin credentials')
    
    return render_template('admin_login.html')


@app.route('/student/dashboard')
def student_dashboard():
    """Student dashboard page"""
    if 'user_id' not in session or session.get('user_type') != 'student':
        return redirect(url_for('login'))
    
    student_id = session['user_id']
    student = db.get_student(student_id)
    library = db.get_library()
    
    # Get all books
    all_books = library.get_all_books()
    books_data = [book.to_dict() for book in all_books]
    
    # Get borrowed books
    borrowed_book_ids = student.get_borrowed_books()
    borrowed_count = student.get_borrowed_count()
    max_borrow_limit = student.MAX_BORROW_LIMIT
    
    # Get full information for borrowed books
    borrowed_books_data = []
    for book_id in borrowed_book_ids:
        book = library.get_book(book_id)
        if book:
            borrowed_books_data.append(book.to_dict())
    
    # Get books for sale
    books_for_sale = library.get_books_for_sale()
    books_for_sale_data = [book.to_dict() for book in books_for_sale]
    
    # Get available times for cash payment
    available_times = db.get_available_times()
    
    return render_template('student_dashboard.html', 
                         books=books_data, 
                         borrowed_books=borrowed_book_ids,
                         borrowed_books_data=borrowed_books_data,
                         borrowed_count=borrowed_count,
                         max_borrow_limit=max_borrow_limit,
                         books_for_sale=books_for_sale_data,
                         available_times=available_times,
                         student_id=student_id)


@app.route('/admin/dashboard')
def admin_dashboard():
    """Admin dashboard page"""
    if 'user_id' not in session or session.get('user_type') != 'admin':
        return redirect(url_for('admin_login'))
    
    library = db.get_library()
    all_books = library.get_all_books()
    books_data = [book.to_dict() for book in all_books]
    
    # Get all sales
    all_sales = library.get_all_sales()
    sales_data = [sale.to_dict() for sale in all_sales]
    
    return render_template('admin_dashboard.html', books=books_data, sales=sales_data)


@app.route('/api/borrow', methods=['POST'])
def borrow_book():
    """API endpoint to borrow a book"""
    if 'user_id' not in session or session.get('user_type') != 'student':
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    data = request.json
    book_id = data.get('book_id')
    student_id = session['user_id']
    
    library = db.get_library()
    student = db.get_student(student_id)
    
    # Check if student has reached the borrowing limit
    if not student.can_borrow_more():
        return jsonify({'success': False, 'message': f'You have reached the maximum borrowing limit of {student.MAX_BORROW_LIMIT} books. Please return a book first.'}), 400
    
    if library.borrow_book(student_id, book_id):
        if student.borrow_book(book_id):
            return jsonify({'success': True, 'message': 'Book borrowed successfully'})
        else:
            # Rollback the library borrowing if student borrowing fails
            library.return_book(student_id, book_id)
            return jsonify({'success': False, 'message': 'Cannot borrow this book'}), 400
    else:
        return jsonify({'success': False, 'message': 'Book not available'}), 400


@app.route('/api/return', methods=['POST'])
def return_book():
    """API endpoint to return a book"""
    if 'user_id' not in session or session.get('user_type') != 'student':
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    data = request.json
    book_id = data.get('book_id')
    student_id = session['user_id']
    
    library = db.get_library()
    student = db.get_student(student_id)
    
    if library.return_book(student_id, book_id):
        student.return_book(book_id)
        return jsonify({'success': True, 'message': 'Book returned successfully'})
    else:
        return jsonify({'success': False, 'message': 'Cannot return this book'}), 400


@app.route('/api/add_book', methods=['POST'])
def add_book():
    """API endpoint to add a book (admin only)"""
    if 'user_id' not in session or session.get('user_type') != 'admin':
        return jsonify({'success': False, 'message': 'Not authenticated as admin'}), 401
    
    data = request.json
    book_id = data.get('book_id')
    title = data.get('title')
    author = data.get('author')
    isbn = data.get('isbn')
    copies = int(data.get('copies', 1))
    for_sale = data.get('for_sale', False)
    price = float(data.get('price', 0.0)) if for_sale else 0.0
    
    if not all([book_id, title, author, isbn]):
        return jsonify({'success': False, 'message': 'Missing required fields'}), 400
    
    library = db.get_library()
    book = Book(book_id, title, author, isbn, copies, for_sale=for_sale, price=price)
    
    if library.add_book(book):
        return jsonify({'success': True, 'message': 'Book added successfully', 'book': book.to_dict()})
    else:
        return jsonify({'success': False, 'message': 'Book ID already exists'}), 400


@app.route('/api/purchase', methods=['POST'])
def purchase_book():
    """API endpoint to purchase a book"""
    if 'user_id' not in session or session.get('user_type') != 'student':
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    data = request.json
    book_id = data.get('book_id')
    payment_method = data.get('payment_method')  # 'visa' or 'cash'
    faculty = data.get('faculty')  # Student's faculty
    scheduled_time = data.get('scheduled_time')  # Required for cash payments
    student_id = session['user_id']
    
    if payment_method not in ['visa', 'cash']:
        return jsonify({'success': False, 'message': 'Invalid payment method'}), 400
    
    if not faculty:
        return jsonify({'success': False, 'message': 'Please select your faculty'}), 400
    
    if payment_method == 'cash' and not scheduled_time:
        return jsonify({'success': False, 'message': 'Scheduled time required for cash payment'}), 400
    
    library = db.get_library()
    sale = library.sell_book(student_id, book_id, payment_method, faculty, scheduled_time)
    
    if sale:
        return jsonify({'success': True, 'message': 'Book purchased successfully', 'sale': sale.to_dict()})
    else:
        return jsonify({'success': False, 'message': 'Book not available for purchase'}), 400


@app.route('/api/available_times', methods=['GET'])
def get_available_times():
    """API endpoint to get available times for cash payment"""
    available_times = db.get_available_times()
    return jsonify({'success': True, 'times': available_times})


@app.route('/logout')
def logout():
    """Logout and clear session"""
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)

