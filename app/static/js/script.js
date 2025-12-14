// Wonderland Toy Store - JavaScript

document.addEventListener('DOMContentLoaded', function() {
    console.log('Wonderland Toy Store loaded!');
    
    // Add to cart button functionality
    const buttons = document.querySelectorAll('.product-card button');
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            alert('Item added to cart!');
        });
    });
});
