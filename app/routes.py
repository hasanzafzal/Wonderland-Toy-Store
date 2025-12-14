from flask import Blueprint, render_template, jsonify
from app.models import Product, Order
from app import db

main_bp = Blueprint('main', __name__)

# Sample product data for demo
PRODUCTS_DATA = {
    'action': [
        {'id': 1, 'name': 'Action Hero Set', 'price': 29.99, 'icon': '🦸', 'description': 'Premium action figures'},
        {'id': 2, 'name': 'Super Soldier', 'price': 24.99, 'icon': '💪', 'description': 'Military action figure'},
    ],
    'building': [
        {'id': 3, 'name': 'Build Master Blocks', 'price': 39.99, 'icon': '🧱', 'description': 'Educational blocks'},
        {'id': 4, 'name': 'Castle Creator', 'price': 49.99, 'icon': '🏰', 'description': 'Build your own castle'},
    ],
    'puzzle': [
        {'id': 5, 'name': 'Puzzle Challenge', 'price': 24.99, 'icon': '🧩', 'description': '1000-piece puzzle'},
        {'id': 6, 'name': 'Brain Teaser', 'price': 19.99, 'icon': '🧠', 'description': '3D brain teaser'},
    ],
    'outdoor': [
        {'id': 7, 'name': 'Outdoor Adventure Pack', 'price': 44.99, 'icon': '🚴', 'description': 'Outdoor play set'},
        {'id': 8, 'name': 'Skateboard Pro', 'price': 54.99, 'icon': '🛹', 'description': 'Professional skateboard'},
    ],
    'art': [
        {'id': 9, 'name': 'Art Studio Deluxe', 'price': 34.99, 'icon': '🎨', 'description': 'Premium art supplies'},
        {'id': 10, 'name': 'Craft Master Kit', 'price': 29.99, 'icon': '✏️', 'description': 'Complete craft kit'},
    ],
    'plush': [
        {'id': 11, 'name': 'Cuddle Companion', 'price': 19.99, 'icon': '🧸', 'description': 'Soft plush toy'},
        {'id': 12, 'name': 'Huggable Friend', 'price': 24.99, 'icon': '🐻', 'description': 'Teddy bear plush'},
    ]
}

@main_bp.route('/')
def index():
    """Homepage"""
    return render_template('index.html', title='Wonderland Toy Store')

@main_bp.route('/about')
def about():
    """About page"""
    return render_template('about.html', title='About Us')

@main_bp.route('/contact')
def contact():
    """Contact page"""
    return render_template('contact.html', title='Contact Us')

@main_bp.route('/products')
def products():
    """Products page"""
    all_products = []
    for category, items in PRODUCTS_DATA.items():
        for item in items:
            item['category'] = category.capitalize()
        all_products.extend(items)
    return render_template('products.html', title='Our Products', products=all_products)

@main_bp.route('/category/<category>')
def category(category):
    """Category page"""
    products = PRODUCTS_DATA.get(category, [])
    return render_template('category.html', title=f'{category.capitalize()} Toys', category=category, products=products)

@main_bp.route('/api/products')
def api_products():
    """API endpoint for products"""
    all_products = []
    for category, items in PRODUCTS_DATA.items():
        for item in items:
            item['category'] = category.capitalize()
        all_products.extend(items)
    return jsonify(all_products)

@main_bp.route('/api/categories')
def api_categories():
    """API endpoint for categories"""
    categories = list(PRODUCTS_DATA.keys())
    return jsonify(categories)
