from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Homepage"""
    return render_template('index.html', title='Wonderland Toy Store')

@main_bp.route('/about')
def about():
    """About page"""
    return render_template('about.html', title='About Us')

@main_bp.route('/products')
def products():
    """Products page"""
    return render_template('products.html', title='Our Products')
