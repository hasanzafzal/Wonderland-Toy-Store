from flask import Blueprint, render_template
from app.models import Product, Order
from app import db

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
    all_products = Product.query.all()
    return render_template('products.html', title='Our Products', products=all_products)
