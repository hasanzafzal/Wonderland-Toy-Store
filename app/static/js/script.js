// Wonderland Toy Store - Interactive JavaScript

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('🎪 Wonderland Toy Store loaded!');
    
    // Add event listeners
    setupEventListeners();
    
    // Newsletter form
    const newsletterForm = document.getElementById('newsletter-form');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', handleNewsletterSubmit);
    }
    
    // Category cards
    setupCategoryCards();
    
    // Randomize product ratings
    randomizeRatings();
});

// Handle newsletter form submission
function handleNewsletterSubmit(e) {
    e.preventDefault();
    const email = e.target.querySelector('input[type="email"]').value;
    
    if (email) {
        showNotification(`Thank you! We'll send updates to ${email}`);
        e.target.reset();
    }
}

// Show notification
function showNotification(message) {
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: linear-gradient(135deg, #27ae60 0%, #229954 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        z-index: 10000;
        animation: slideInRight 0.3s ease;
        max-width: 300px;
    `;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // Add animation style
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideInRight {
            from {
                transform: translateX(400px);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
    `;
    document.head.appendChild(style);
    
    setTimeout(() => {
        notification.style.animation = 'slideInRight 0.3s ease reverse';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Setup event listeners
function setupEventListeners() {
    // Product cards hover effects
    document.querySelectorAll('.product-card').forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px)';
        });
        card.addEventListener('mouseleave', function() {
            this.style.transform = '';
        });
    });
}

// Setup category cards
function setupCategoryCards() {
    const categoryCards = document.querySelectorAll('.category-card');
    
    categoryCards.forEach(card => {
        card.addEventListener('click', function() {
            const category = this.dataset.category;
            handleCategoryClick(category);
        });
    });
}

// Handle category click
function handleCategoryClick(category) {
    console.log(`Clicked category: ${category}`);
    // Category navigation is handled by the category links themselves
    showNotification(`Navigating to ${category} products`);
}

// Smooth scroll to sections
function smoothScroll(target) {
    document.querySelector(target).scrollIntoView({
        behavior: 'smooth',
        block: 'start'
    });
}

// Add more interactivity - scroll animations
window.addEventListener('scroll', function() {
    // Add parallax effect to hero
    const hero = document.querySelector('.hero');
    if (hero && window.scrollY < 600) {
        hero.style.backgroundPosition = `0 ${window.scrollY * 0.5}px`;
    }
});

// Add keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Press 'h' to go to hero
    if (e.key === 'h' || e.key === 'H') {
        document.querySelector('.hero').scrollIntoView({ behavior: 'smooth' });
    }
    // Press 'p' to go to products
    if (e.key === 'p' || e.key === 'P') {
        document.querySelector('#featured').scrollIntoView({ behavior: 'smooth' });
    }
});
// Randomize product ratings (between 4.0 and 5.0)
function randomizeRatings() {
    const ratingElements = document.querySelectorAll('.rating-value');
    ratingElements.forEach(element => {
        const randomRating = (Math.random() * 1 + 4).toFixed(1); // 4.0 to 5.0
        element.textContent = randomRating;
    });
}