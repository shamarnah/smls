// JavaScript for Admin Dashboard

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

// Toggle price field based on for_sale checkbox
function togglePriceField() {
    const forSale = document.getElementById('for_sale');
    const priceGroup = document.getElementById('priceGroup');
    const priceInput = document.getElementById('price');
    
    if (forSale.checked) {
        priceGroup.style.display = 'block';
        priceInput.setAttribute('required', 'required');
    } else {
        priceGroup.style.display = 'none';
        priceInput.removeAttribute('required');
        priceInput.value = '';
    }
}

// Handle form submission for adding a book
document.getElementById('addBookForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent default form submission
    
    // Get form values
    const bookId = document.getElementById('book_id').value.trim();
    const title = document.getElementById('title').value.trim();
    const author = document.getElementById('author').value.trim();
    const isbn = document.getElementById('isbn').value.trim();
    const copies = parseInt(document.getElementById('copies').value);
    const forSale = document.getElementById('for_sale').checked;
    const price = forSale ? parseFloat(document.getElementById('price').value) : 0;
    
    // Validate inputs
    if (!bookId || !title || !author || !isbn) {
        showMessage('Please fill in all required fields', 'error');
        return;
    }
    
    if (forSale && (!price || price <= 0)) {
        showMessage('Please enter a valid price for books for sale', 'error');
        return;
    }
    
    // Send request to add book
    fetch('/api/add_book', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            book_id: bookId,
            title: title,
            author: author,
            isbn: isbn,
            copies: copies,
            for_sale: forSale,
            price: price
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showMessage(data.message, 'success');
            // Clear form
            document.getElementById('addBookForm').reset();
            // Reload page after 1 second to show the new book
            setTimeout(function() {
                window.location.reload();
            }, 1000);
        } else {
            showMessage(data.message, 'error');
        }
    })
    .catch(error => {
        showMessage('Error adding book. Please try again.', 'error');
        console.error('Error:', error);
    });
});

