from flask import Blueprint, render_template, jsonify, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from app.models import Product, Order, User, Cart, CartItem
from app import db
from werkzeug.security import generate_password_hash

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Homepage"""
    return render_template('index.html', title='Wonderland Toy Store')

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Register new user"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validation
        if not username or not email or not password:
            flash('All fields are required', 'error')
            return redirect(url_for('main.register'))
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('main.register'))
        
        # Check if user exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return redirect(url_for('main.register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return redirect(url_for('main.register'))
        
        # Create new user
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        # Create empty cart for user
        cart = Cart(user_id=user.id)
        db.session.add(cart)
        db.session.commit()
        
        flash('Account created successfully! Please login.', 'success')
        return redirect(url_for('main.login'))
    
    return render_template('register.html', title='Register')

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash(f'Welcome back, {username}!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.products'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html', title='Login')

@main_bp.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.index'))

@main_bp.route('/products')
def products():
    """Products page"""
    products = Product.query.all()
    return render_template('products.html', title='Our Products', products=products)

@main_bp.route('/about')
def about():
    """About page"""
    return render_template('about.html', title='About Us')

@main_bp.route('/contact')
def contact():
    """Contact page"""
    return render_template('contact.html', title='Contact Us')

@main_bp.route('/cart')
def view_cart():
    """View shopping cart"""
    if not current_user.is_authenticated:
        flash('Please login to view your cart', 'warning')
        return redirect(url_for('main.login', next=url_for('main.view_cart')))
    
    cart = current_user.cart or Cart(user_id=current_user.id)
    return render_template('cart.html', title='Shopping Cart', cart=cart)

@main_bp.route('/cart/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    """Add product to cart"""
    product = Product.query.get_or_404(product_id)
    quantity = request.form.get('quantity', 1, type=int)
    
    # Get or create cart
    cart = current_user.cart
    if not cart:
        cart = Cart(user_id=current_user.id)
        db.session.add(cart)
        db.session.flush()
    
    # Check if item already in cart
    cart_item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()
    
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(cart_id=cart.id, product_id=product_id, quantity=quantity)
        db.session.add(cart_item)
    
    db.session.commit()
    flash(f'{product.name} added to cart!', 'success')
    return redirect(url_for('main.view_cart'))

@main_bp.route('/cart/remove/<int:item_id>')
@login_required
def remove_from_cart(item_id):
    """Remove item from cart"""
    cart_item = CartItem.query.get_or_404(item_id)
    
    # Verify ownership
    if cart_item.cart.user_id != current_user.id:
        flash('Unauthorized', 'error')
        return redirect(url_for('main.view_cart'))
    
    product_name = cart_item.product.name
    db.session.delete(cart_item)
    db.session.commit()
    
    flash(f'{product_name} removed from cart', 'success')
    return redirect(url_for('main.view_cart'))

@main_bp.route('/cart/update/<int:item_id>', methods=['POST'])
@login_required
def update_cart_item(item_id):
    """Update cart item quantity"""
    cart_item = CartItem.query.get_or_404(item_id)
    
    # Verify ownership
    if cart_item.cart.user_id != current_user.id:
        flash('Unauthorized', 'error')
        return redirect(url_for('main.view_cart'))
    
    quantity = request.form.get('quantity', 1, type=int)
    
    if quantity > 0:
        cart_item.quantity = quantity
    else:
        db.session.delete(cart_item)
    
    db.session.commit()
    flash('Cart updated!', 'success')
    return redirect(url_for('main.view_cart'))

@main_bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    """Checkout and place order"""
    cart = current_user.cart
    
    if not cart or not cart.items:
        flash('Your cart is empty', 'warning')
        return redirect(url_for('main.view_cart'))
    
    if request.method == 'POST':
        # Create orders for each item in cart
        for item in cart.items:
            order = Order(
                user_id=current_user.id,
                product_id=item.product_id,
                quantity=item.quantity,
                total_price=item.product.price * item.quantity
            )
            db.session.add(order)
        
        # Clear cart
        CartItem.query.filter_by(cart_id=cart.id).delete()
        db.session.commit()
        
        flash('Order placed successfully!', 'success')
        return redirect(url_for('main.orders'))
    
    return render_template('checkout.html', title='Checkout', cart=cart)

@main_bp.route('/orders')
@login_required
def orders():
    """View user orders"""
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('orders.html', title='My Orders', orders=orders)

