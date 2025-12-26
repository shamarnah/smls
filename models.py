"""
OOP Classes for the Smart Library Management System (SLMS)
This module contains all the core classes using Object-Oriented Programming concepts.
"""


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
    
    def __init__(self, book_id, title, author, isbn, copies=1):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.isbn = isbn
        self.copies = copies  # Total copies available
        self.available_copies = copies  # Copies currently available
    
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
            'available_copies': self.available_copies
        }


class Library:
    """Class representing the library that manages books and borrowings"""
    
    def __init__(self):
        self.books = {}  # Dictionary: book_id -> Book object
        self.borrowings = {}  # Dictionary: (student_id, book_id) -> True
    
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
        
        # Add some sample books
        book1 = Book("B001", "Introduction to Python", "John Smith", "978-0123456789", 3)
        book2 = Book("B002", "Data Structures and Algorithms", "Jane Doe", "978-0987654321", 2)
        book3 = Book("B003", "Object-Oriented Programming", "Bob Johnson", "978-1122334455", 1)
        
        self.library.add_book(book1)
        self.library.add_book(book2)
        self.library.add_book(book3)
    
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
        """Check if student ID follows the format: asuXXXXXXstd"""
        if not student_id.startswith("asu") or not student_id.endswith("std"):
            return False
        middle = student_id[3:-3]
        return middle.isdigit() and len(middle) == 6
    
    def get_library(self):
        """Get the library instance"""
        return self.library

