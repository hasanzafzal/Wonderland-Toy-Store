// Wonderland Toy Store - Interactive JavaScript

// Sample product data for featured section
const featuredProducts = [
    {
        id: 1,
        name: 'Action Hero Set',
        category: 'Action Figures',
        price: 29.99,
        rating: 4.8,
        icon: '🦸',
        description: 'Premium action figures with articulated joints'
    },
    {
        id: 2,
        name: 'Build Master Blocks',
        category: 'Building Sets',
        price: 39.99,
        rating: 4.9,
        icon: '🧱',
        description: 'Educational building blocks for creative minds'
    },
    {
        id: 3,
        name: 'Puzzle Challenge',
        category: 'Puzzles',
        price: 24.99,
        rating: 4.7,
        icon: '🧩',
        description: '1000-piece challenging puzzle for all ages'
    },
    {
        id: 4,
        name: 'Outdoor Adventure Pack',
        category: 'Outdoor',
        price: 44.99,
        rating: 4.6,
        icon: '🚴',
        description: 'Complete outdoor play equipment set'
    },
    {
        id: 5,
        name: 'Art Studio Deluxe',
        category: 'Arts & Crafts',
        price: 34.99,
        rating: 4.8,
        icon: '🎨',
        description: 'Premium art supplies and craft materials'
    },
    {
        id: 6,
        name: 'Cuddle Companion',
        category: 'Plush Toys',
        price: 19.99,
        rating: 4.9,
        icon: '🧸',
        description: 'Soft and cuddly plush toy for all ages'
    }
];

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('🎪 Wonderland Toy Store loaded!');
    
    // Render featured products
    renderFeaturedProducts();
    
    // Add event listeners
    setupEventListeners();
    
    // Newsletter form
    const newsletterForm = document.getElementById('newsletter-form');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', handleNewsletterSubmit);
    }
    
    // Category cards
    setupCategoryCards();
});

// Render featured products
function renderFeaturedProducts() {
    const container = document.getElementById('featured-products');
    if (!container) return;
    
    container.innerHTML = featuredProducts.map(product => `
        <div class="product-card" data-product-id="${product.id}">
            <div class="product-image">
                <span>${product.icon}</span>
            </div>
            <div class="product-info">
                <div class="product-category">${product.category}</div>
                <h3 class="product-name">${product.name}</h3>
                <p class="product-description">${product.description}</p>
                <div class="product-footer">
                    <div class="product-price">$${product.price}</div>
                    <div class="product-rating">⭐ ${product.rating}</div>
                </div>
                <button class="btn-add-cart" data-product-id="${product.id}">Add to Cart</button>
            </div>
        </div>
    `).join('');
    
    // Add event listeners to "Add to Cart" buttons
    document.querySelectorAll('.btn-add-cart').forEach(btn => {
        btn.addEventListener('click', handleAddToCart);
    });
}

// Handle "Add to Cart" button click
function handleAddToCart(e) {
    const productId = e.target.dataset.productId;
    const product = featuredProducts.find(p => p.id == productId);
    
    if (product) {
        // Show success message
        const btn = e.target;
        const originalText = btn.textContent;
        btn.textContent = '✓ Added!';
        btn.style.background = '#27ae60';
        
        setTimeout(() => {
            btn.textContent = originalText;
            btn.style.background = '';
        }, 2000);
        
        // Log to console (in real app, would add to cart state)
        console.log(`Added ${product.name} to cart`);
        showNotification(`${product.name} added to cart!`);
    }
}

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
    // Filter products by category (in real app, would navigate or filter)
    const filtered = featuredProducts.filter(p => 
        p.category.toLowerCase().includes(category.toLowerCase())
    );
    console.log(`Found ${filtered.length} products in ${category}`);
    showNotification(`Showing ${filtered.length} products in ${category}`);
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
