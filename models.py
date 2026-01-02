"""
OOP Classes for the Smart Library Management System (SLMS)
This module contains all the core classes using Object-Oriented Programming concepts.
"""

from datetime import datetime


class User:
    """Base class for all users in the system"""
    
    def __init__(self, user_id, password):
        self.user_id = user_id
        self.password = password
    
    def authenticate(self, password):
        """Check if the provided password matches"""
        return self.password == password
    
    def get_user_id(self):
        """Get the user ID"""
        return self.user_id


class Student(User):
    """Class representing a student user"""
    
    MAX_BORROW_LIMIT = 2  # Maximum number of books a student can borrow
    
    def __init__(self, student_id, password):
        super().__init__(student_id, password)
        self.borrowed_books = []  # List of book IDs borrowed by this student
    
    def can_borrow_more(self):
        """Check if the student can borrow more books (limit is 2)"""
        return len(self.borrowed_books) < self.MAX_BORROW_LIMIT
    
    def borrow_book(self, book_id):
        """Add a book to the student's borrowed books list"""
        # Check if student has reached the borrowing limit
        if not self.can_borrow_more():
            return False
        if book_id not in self.borrowed_books:
            self.borrowed_books.append(book_id)
            return True
        return False
    
    def return_book(self, book_id):
        """Remove a book from the student's borrowed books list"""
        if book_id in self.borrowed_books:
            self.borrowed_books.remove(book_id)
            return True
        return False
    
    def get_borrowed_books(self):
        """Get list of borrowed book IDs"""
        return self.borrowed_books
    
    def get_borrowed_count(self):
        """Get the number of books currently borrowed"""
        return len(self.borrowed_books)


class Admin(User):
    """Class representing an admin user"""
    
    def __init__(self, admin_id, password):
        super().__init__(admin_id, password)
    
    def add_book(self, library, book):
        """Add a book to the library catalog"""
        return library.add_book(book)


class Book:
    """Class representing a book in the library"""
    
    def __init__(self, book_id, title, author, isbn, copies=1, for_sale=False, price=0.0):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.isbn = isbn
        self.copies = copies  # Total copies available
        self.available_copies = copies  # Copies currently available
        self.for_sale = for_sale  # Whether the book can be purchased
        self.price = price  # Price in JOD (Jordanian Dinar)
    
    def borrow(self):
        """Borrow a copy of the book"""
        if self.available_copies > 0:
            self.available_copies -= 1
            return True
        return False
    
    def return_copy(self):
        """Return a copy of the book"""
        if self.available_copies < self.copies:
            self.available_copies += 1
            return True
        return False
    
    def is_available(self):
        """Check if the book is available for borrowing"""
        return self.available_copies > 0
    
    def to_dict(self):
        """Convert book to dictionary for JSON serialization"""
        return {
            'book_id': self.book_id,
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'copies': self.copies,
            'available_copies': self.available_copies,
            'for_sale': self.for_sale,
            'price': self.price
        }
    
    def sell(self):
        """Sell a copy of the book (reduce available copies)"""
        if self.available_copies > 0:
            self.available_copies -= 1
            self.copies -= 1  # Also reduce total copies when sold
            return True
        return False


class Sale:
    """Class representing a book sale"""
    
    def __init__(self, sale_id, student_id, book_id, book_title, price, payment_method, faculty, scheduled_time=None):
        self.sale_id = sale_id
        self.student_id = student_id
        self.book_id = book_id
        self.book_title = book_title
        self.price = price
        self.payment_method = payment_method  # "visa" or "cash"
        self.faculty = faculty  # Student's faculty
        self.scheduled_time = scheduled_time  # For cash payments, the scheduled pickup time
        self.sale_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Set when sale is created
    
    def to_dict(self):
        """Convert sale to dictionary for JSON serialization"""
        return {
            'sale_id': self.sale_id,
            'student_id': self.student_id,
            'book_id': self.book_id,
            'book_title': self.book_title,
            'price': self.price,
            'payment_method': self.payment_method,
            'faculty': self.faculty,
            'scheduled_time': self.scheduled_time,
            'sale_date': self.sale_date
        }


class Library:
    """Class representing the library that manages books and borrowings"""
    
    def __init__(self):
        self.books = {}  # Dictionary: book_id -> Book object
        self.borrowings = {}  # Dictionary: (student_id, book_id) -> True
        self.sales = {}  # Dictionary: sale_id -> Sale object
        self.sale_counter = 0  # Counter for generating unique sale IDs
    
    def add_book(self, book):
        """Add a book to the library catalog"""
        if book.book_id not in self.books:
            self.books[book.book_id] = book
            return True
        return False
    
    def get_book(self, book_id):
        """Get a book by its ID"""
        return self.books.get(book_id)
    
    def get_all_books(self):
        """Get all books in the library"""
        return list(self.books.values())
    
    def borrow_book(self, student_id, book_id):
        """Process a book borrowing"""
        book = self.get_book(book_id)
        if book and book.is_available():
            if book.borrow():
                self.borrowings[(student_id, book_id)] = True
                return True
        return False
    
    def return_book(self, student_id, book_id):
        """Process a book return"""
        book = self.get_book(book_id)
        if book and (student_id, book_id) in self.borrowings:
            if book.return_copy():
                del self.borrowings[(student_id, book_id)]
                return True
        return False
    
    def sell_book(self, student_id, book_id, payment_method, faculty, scheduled_time=None):
        """Process a book sale"""
        book = self.get_book(book_id)
        if book and book.for_sale and book.available_copies > 0:
            if book.sell():
                self.sale_counter += 1
                sale = Sale(
                    sale_id=f"SALE{self.sale_counter:04d}",
                    student_id=student_id,
                    book_id=book_id,
                    book_title=book.title,
                    price=book.price,
                    payment_method=payment_method,
                    faculty=faculty,
                    scheduled_time=scheduled_time
                )
                self.sales[sale.sale_id] = sale
                return sale
        return None
    
    def get_all_sales(self):
        """Get all sales"""
        return list(self.sales.values())
    
    def get_books_for_sale(self):
        """Get all books that are for sale"""
        return [book for book in self.books.values() if book.for_sale]


class Database:
    """Class to manage data storage (using in-memory storage for simplicity)"""
    
    def __init__(self):
        self.students = {}  # Dictionary: student_id -> Student object
        self.admins = {}  # Dictionary: admin_id -> Admin object
        self.library = Library()
        self._initialize_default_data()
    
    def _initialize_default_data(self):
        """Initialize with some default data"""
        # Create default admin
        admin = Admin("admin", "admin")
        self.admins["admin"] = admin
        
        # Add some sample books (for borrowing)
        book1 = Book("B001", "Introduction to Python", "John Smith", "978-0123456789", 3)
        book2 = Book("B002", "Data Structures and Algorithms", "Jane Doe", "978-0987654321", 2)
        book3 = Book("B003", "Object-Oriented Programming", "Bob Johnson", "978-1122334455", 1)
        
        # Add some sample books (for sale)
        book4 = Book("S001", "Advanced Python Programming", "Sarah Williams", "978-2233445566", 5, for_sale=True, price=25.50)
        book5 = Book("S002", "Machine Learning Basics", "Michael Brown", "978-3344556677", 3, for_sale=True, price=30.00)
        book6 = Book("S003", "Web Development Guide", "Emily Davis", "978-4455667788", 1, for_sale=True, price=22.75)  # Only 1 copy - will be sold
        
        self.library.add_book(book1)
        self.library.add_book(book2)
        self.library.add_book(book3)
        self.library.add_book(book4)
        self.library.add_book(book5)
        self.library.add_book(book6)
        
        # Add a sample sale (one book already sold - S003 is sold out)
        sample_student_id = "202420455asu"
        sample_student = self.get_student(sample_student_id)
        # Sell the only copy of book6 (S003) via Visa payment
        sale = self.library.sell_book(sample_student_id, "S003", "visa", "Engineering and Technology", None)
        if sale:
            # Book S003 is now sold out (0 available copies)
            pass
    
    def get_available_times(self):
        """Get available times for cash payment pickup"""
        # Default schedule: Sunday to Thursday, 9 AM to 4 PM, every hour
        times = []
        days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"]
        hours = ["9:00 AM", "10:00 AM", "11:00 AM", "12:00 PM", "1:00 PM", "2:00 PM", "3:00 PM", "4:00 PM"]
        
        for day in days:
            for hour in hours:
                times.append(f"{day} - {hour}")
        
        return times
    
    def get_student(self, student_id):
        """Get a student by ID, create if doesn't exist"""
        if student_id not in self.students:
            # Create new student with password same as student_id
            student = Student(student_id, student_id)
            self.students[student_id] = student
        return self.students[student_id]
    
    def get_admin(self, admin_id):
        """Get an admin by ID"""
        return self.admins.get(admin_id)
    
    def is_valid_student_id(self, student_id):
        """Check if student ID follows the format: XXXXXXXXXasu"""
        if not student_id.endswith("asu"):
            return False
        prefix = student_id[:-3]  # Everything except the last 3 characters ("asu")
        return prefix.isdigit() and len(prefix) == 9
    
    def get_library(self):
        """Get the library instance"""
        return self.library

