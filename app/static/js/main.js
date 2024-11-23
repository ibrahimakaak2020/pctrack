// Delete confirmation
document.addEventListener('DOMContentLoaded', function() {
    const deleteButtons = document.querySelectorAll('.btn-danger');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this item?')) {
                e.preventDefault();
            }
        });
    });
});

// Form validation
function validateForm(form) {
    let isValid = true;
    const requiredFields = form.querySelectorAll('[required]');
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

// Dynamic form handling
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(this)) {
                e.preventDefault();
            }
        });
    });
});

// Auto-dismiss flash messages
document.addEventListener('DOMContentLoaded', function() {
    // Function to fade out and remove an element
    function fadeOutAndRemove(element) {
        element.style.transition = 'opacity 0.5s ease';
        element.style.opacity = '0';
        setTimeout(() => {
            element.remove();
        }, 500);
    }

    // Handle flash messages
    const flashMessages = document.querySelectorAll('.alert');
    if (flashMessages.length > 0) {
        flashMessages.forEach(message => {
            // Add animation class
            message.style.transition = 'opacity 0.5s ease';
            
            // Set timeout to remove message
            setTimeout(() => {
                fadeOutAndRemove(message);
            }, 5000);
        });
    }

    // Remove the flash-messages container if empty
    setInterval(() => {
        const container = document.getElementById('flash-messages');
        if (container && container.children.length === 0) {
            container.remove();
        }
    }, 1000);
});

// Function to show custom toast messages
function showToast(message, category = 'info') {
    const container = document.getElementById('flash-messages') || createMessageContainer();
    const alert = createAlert(message, category);
    container.appendChild(alert);

    setTimeout(() => {
        fadeOutAndRemove(alert);
    }, 5000);
}

// Helper function to create message container
function createMessageContainer() {
    const container = document.createElement('div');
    container.id = 'flash-messages';
    document.querySelector('.container').insertBefore(container, document.querySelector('.container').firstChild);
    return container;
}

// Helper function to create alert element
function createAlert(message, category) {
    const alert = document.createElement('div');
    alert.className = `alert alert-${category} alert-dismissible fade show`;
    alert.role = 'alert';
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    return alert;
}

// Handle back button functionality
document.addEventListener('DOMContentLoaded', function() {
    const backButtons = document.querySelectorAll('[data-action="go-back"]');
    
    backButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            const fallbackUrl = button.getAttribute('href');
            
            if (window.history.length > 1) {
                window.history.back();
            } else {
                window.location.href = fallbackUrl;
            }
        });
    });
}); 