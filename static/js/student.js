// JavaScript for Student Dashboard

// Function to show a message to the user
function showMessage(text, type) {
    const messageDiv = document.getElementById('message');
    messageDiv.textContent = text;
    messageDiv.className = 'message ' + type;
    
    // Hide message after 3 seconds
    setTimeout(function() {
        messageDiv.className = 'message';
        messageDiv.textContent = '';
    }, 3000);
}

// Function to borrow a book
function borrowBook(bookId) {
    fetch('/api/borrow', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            book_id: bookId
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showMessage(data.message, 'success');
            // Reload page after 1 second to update the book list
            setTimeout(function() {
                window.location.reload();
            }, 1000);
        } else {
            showMessage(data.message, 'error');
        }
    })
    .catch(error => {
        showMessage('Error borrowing book. Please try again.', 'error');
        console.error('Error:', error);
    });
}

// Function to return a book
function returnBook(bookId) {
    fetch('/api/return', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            book_id: bookId
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showMessage(data.message, 'success');
            // Reload page after 1 second to update the book list
            setTimeout(function() {
                window.location.reload();
            }, 1000);
        } else {
            showMessage(data.message, 'error');
        }
    })
    .catch(error => {
        showMessage('Error returning book. Please try again.', 'error');
        console.error('Error:', error);
    });
}

