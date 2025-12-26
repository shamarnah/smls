# Smart Library Management System (SLMS)

A simple web-based library management system built with Python Flask for an Object-Oriented Programming course project.

## Features

- **Student Login**: Students can log in using their student ID (format: `asuXXXXXXstd`) with password same as student ID
- **Book Borrowing**: Students can browse available books and borrow them
- **Book Returns**: Students can return borrowed books
- **Admin Panel**: Admins can add new books to the library catalog
- **Simple UI**: Clean and beginner-friendly HTML/CSS/JavaScript interface

## OOP Concepts Used

This project demonstrates several Object-Oriented Programming concepts:

1. **Classes**: `User`, `Student`, `Admin`, `Book`, `Library`, `Database`
2. **Inheritance**: `Student` and `Admin` inherit from the base `User` class
3. **Encapsulation**: Data and methods are encapsulated within classes
4. **Polymorphism**: Different user types (Student, Admin) can be used through the base User interface
5. **Abstraction**: Complex operations are abstracted into simple method calls

## Project Structure

```
smls/
├── app.py                 # Main Flask application
├── models.py              # OOP classes (User, Student, Admin, Book, Library, Database)
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/            # HTML templates
│   ├── login.html
│   ├── admin_login.html
│   ├── student_dashboard.html
│   └── admin_dashboard.html
└── static/               # Static files (CSS, JS)
    ├── css/
    │   └── style.css
    └── js/
        ├── student.js
        └── admin.js
```

## Setup Instructions

### 1. Install Python

Make sure you have Python 3.7 or higher installed on your system.

### 2. Install Dependencies

Open a terminal in the project directory and run:

```bash
pip install -r requirements.txt
```

### 3. Run the Application

Start the Flask server:

```bash
python app.py
```

The application will start on `http://localhost:5000`

### 4. Access the Application

Open your web browser and navigate to:
- **Student Login**: `http://localhost:5000/login`
- **Admin Login**: `http://localhost:5000/admin`

## Usage

### For Students

1. Go to the login page
2. Enter your student ID in the format: `asuXXXXXXstd` (e.g., `asu123456std`)
3. Enter the same student ID as the password
4. Browse available books
5. Click "Borrow Book" to borrow a book
6. Click "Return Book" to return a borrowed book

### For Admins

1. Go to `/admin` page
2. Login with:
   - **Admin ID**: `admin`
   - **Password**: `admin`
3. Fill in the form to add a new book:
   - Book ID (e.g., B001, B002)
   - Title
   - Author
   - ISBN
   - Number of copies
4. Click "Add Book" to add it to the catalog

## Default Data

The system comes with some sample data:

- **Admin Account**: 
  - ID: `admin`
  - Password: `admin`

- **Sample Books**:
  - Introduction to Python (3 copies)
  - Data Structures and Algorithms (2 copies)
  - Object-Oriented Programming (1 copy)

## How It Works

### Data Storage

The system uses **in-memory storage** (Python dictionaries) for simplicity. This means:
- Data is stored in RAM while the application is running
- All data is lost when you stop the server
- Perfect for learning and testing

### Authentication

- Students don't need to create accounts
- Any valid student ID format (`asuXXXXXXstd`) will automatically create a student account
- Password is the same as the student ID

### Session Management

The application uses Flask sessions to keep users logged in. When you log in, a session is created that remembers who you are until you log out.

## Code Explanation

### models.py

Contains all the OOP classes:

- **User**: Base class with authentication
- **Student**: Inherits from User, can borrow/return books
- **Admin**: Inherits from User, can add books
- **Book**: Represents a book with availability tracking
- **Library**: Manages the book catalog and borrowings
- **Database**: Main data store that creates and manages all objects

### app.py

The Flask web server that:
- Handles HTTP requests
- Renders HTML pages
- Provides API endpoints for borrowing/returning books
- Manages user sessions

### Templates

HTML files that define the user interface:
- `login.html`: Student login page
- `admin_login.html`: Admin login page
- `student_dashboard.html`: Student's main page
- `admin_dashboard.html`: Admin's main page

## Learning Points

This project helps you understand:

1. **Web Development Basics**: How web applications work (client-server model)
2. **OOP Principles**: Classes, inheritance, encapsulation
3. **Python Flask**: A simple web framework
4. **Frontend-Backend Communication**: How JavaScript talks to Python
5. **Session Management**: How to keep users logged in

## Troubleshooting

- **Port already in use**: Change the port in `app.py` (line: `app.run(debug=True, port=5000)`)
- **Module not found**: Make sure you installed requirements: `pip install -r requirements.txt`
- **Page not loading**: Check that the Flask server is running

## Future Enhancements (Optional)

If you want to extend this project, you could add:

- SQLite database for persistent storage
- Due dates for borrowed books
- Fine calculation for overdue books
- Search functionality for books
- User profiles
- Book categories/genres

## License

This is an educational project for learning purposes.

# smls
