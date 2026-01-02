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

// Purchase Modal Functions
function showPurchaseModal(bookId, bookTitle, price) {
    document.getElementById('purchaseModal').style.display = 'block';
    document.getElementById('purchaseBookId').value = bookId;
    document.getElementById('modalBookTitle').textContent = 'Book: ' + bookTitle;
    document.getElementById('modalBookPrice').textContent = 'Price: ' + price.toFixed(2) + ' JOD';
    
    // Reset form
    document.getElementById('purchaseForm').reset();
    document.getElementById('purchaseBookId').value = bookId;
    document.querySelector('input[name="payment_method"][value="visa"]').checked = true;
    
    // Update payment option styling
    document.querySelectorAll('.payment-option').forEach(option => {
        option.classList.remove('checked');
    });
    document.querySelector('input[name="payment_method"][value="visa"]').closest('.payment-option').classList.add('checked');
    
    togglePaymentMethod();
}

function closePurchaseModal() {
    document.getElementById('purchaseModal').style.display = 'none';
    document.getElementById('purchaseForm').reset();
}

function togglePaymentMethod() {
    const paymentMethod = document.querySelector('input[name="payment_method"]:checked').value;
    const visaFields = document.getElementById('visaFields');
    const cashFields = document.getElementById('cashFields');
    const scheduledTime = document.getElementById('scheduled_time');
    
    // Update payment option styling
    document.querySelectorAll('.payment-option').forEach(option => {
        option.classList.remove('checked');
    });
    document.querySelector('input[name="payment_method"]:checked').closest('.payment-option').classList.add('checked');
    
    if (paymentMethod === 'visa') {
        visaFields.style.display = 'block';
        cashFields.style.display = 'none';
        scheduledTime.removeAttribute('required');
    } else {
        visaFields.style.display = 'none';
        cashFields.style.display = 'block';
        scheduledTime.setAttribute('required', 'required');
    }
}

// Format card number input
document.addEventListener('DOMContentLoaded', function() {
    const cardNumber = document.getElementById('card_number');
    if (cardNumber) {
        cardNumber.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\s/g, '');
            let formattedValue = value.match(/.{1,4}/g)?.join(' ') || value;
            e.target.value = formattedValue;
        });
    }
    
    const expiryDate = document.getElementById('expiry_date');
    if (expiryDate) {
        expiryDate.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length >= 2) {
                value = value.substring(0, 2) + '/' + value.substring(2, 4);
            }
            e.target.value = value;
        });
    }
    
    // Handle purchase form submission
    const purchaseForm = document.getElementById('purchaseForm');
    if (purchaseForm) {
        purchaseForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const bookId = document.getElementById('purchaseBookId').value;
            const faculty = document.getElementById('faculty').value;
            const paymentMethod = document.querySelector('input[name="payment_method"]:checked').value;
            const scheduledTime = document.getElementById('scheduled_time').value;
            
            if (!faculty) {
                showMessage('Please select your faculty', 'error');
                return;
            }
            
            if (paymentMethod === 'cash' && !scheduledTime) {
                showMessage('Please select a pickup time for cash payment', 'error');
                return;
            }
            
            fetch('/api/purchase', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    book_id: bookId,
                    faculty: faculty,
                    payment_method: paymentMethod,
                    scheduled_time: scheduledTime || null
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showMessage(data.message, 'success');
                    closePurchaseModal();
                    setTimeout(function() {
                        window.location.reload();
                    }, 1000);
                } else {
                    showMessage(data.message, 'error');
                }
            })
            .catch(error => {
                showMessage('Error purchasing book. Please try again.', 'error');
                console.error('Error:', error);
            });
        });
    }
    
    // Close modal when clicking outside
    window.onclick = function(event) {
        const modal = document.getElementById('purchaseModal');
        if (event.target == modal) {
            closePurchaseModal();
        }
    }
});

