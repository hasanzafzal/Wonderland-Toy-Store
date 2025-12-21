from flask import Blueprint, render_template, jsonify, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from app.models import Product, Order, User, Cart, CartItem, Wishlist, Category
from app import db
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from functools import wraps
import os
import secrets
from datetime import datetime

# File upload configuration
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_product_image(file, product_id):
    """Save product image and return filename"""
    if not file or file.filename == '':
        return None
    
    if not allowed_file(file.filename):
        return None
    
    # Create uploads directory if it doesn't exist
    upload_folder = os.path.join(os.path.dirname(__file__), 'static', 'images', 'products')
    os.makedirs(upload_folder, exist_ok=True)
    
    # Create unique filename
    ext = secure_filename(file.filename).rsplit('.', 1)[1].lower()
    filename = f'product_{product_id}_{int(datetime.utcnow().timestamp())}.{ext}'
    filepath = os.path.join(upload_folder, filename)
    
    # Save file
    file.save(filepath)
    return filename

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Homepage"""
    categories = Category.query.all()
    featured_products = Product.query.filter_by(is_featured=True).all()
    return render_template('index.html', title='Wonderland Toy Store', categories=categories, featured_products=featured_products)

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
            if next_page:
                return redirect(next_page)
            # Redirect admins to admin dashboard, regular users to products
            return redirect(url_for('main.admin_dashboard')) if user.is_admin else redirect(url_for('main.products'))
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

@main_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Forgot password page"""
    if current_user.is_authenticated:
        return redirect(url_for('main.products'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        
        if user:
            # Generate reset token
            reset_token = user.generate_reset_token()
            db.session.commit()
            
            # In a real app, you would send this via email
            # For now, we'll show it in a flash message (for demo purposes)
            reset_link = url_for('main.reset_password', token=reset_token, _external=True)
            
            flash(f'Password reset link: {reset_link}', 'info')
            flash('If an account exists with this email, a password reset link will be sent.', 'success')
        else:
            # Don't reveal if email exists for security
            flash('If an account exists with this email, a password reset link will be sent.', 'success')
        
        return redirect(url_for('main.login'))
    
    return render_template('forgot_password.html', title='Forgot Password')

@main_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Reset password with token"""
    if current_user.is_authenticated:
        return redirect(url_for('main.products'))
    
    user = User.query.filter_by(reset_token=token).first()
    
    if not user or not user.verify_reset_token(token):
        flash('Invalid or expired password reset link.', 'error')
        return redirect(url_for('main.login'))
    
    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if not password or not confirm_password:
            flash('All fields are required', 'error')
            return redirect(url_for('main.reset_password', token=token))
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('main.reset_password', token=token))
        
        if len(password) < 6:
            flash('Password must be at least 6 characters', 'error')
            return redirect(url_for('main.reset_password', token=token))
        
        # Set new password and clear token
        user.set_password(password)
        user.clear_reset_token()
        db.session.commit()
        
        flash('Your password has been reset successfully. Please login with your new password.', 'success')
        return redirect(url_for('main.login'))
    
    return render_template('reset_password.html', title='Reset Password', token=token)

@main_bp.route('/products')
def products():
    """Products page - shows categories"""
    categories = Category.query.all()
    return render_template('products.html', title='Our Products', categories=categories, view_mode='categories')

@main_bp.route('/products/all')
def all_products():
    """View all products"""
    products = Product.query.all()
    categories = Category.query.all()
    return render_template('products.html', title='All Products', products=products, categories=categories, view_mode='all')

@main_bp.route('/products/category/<int:category_id>')
def category_products(category_id):
    """View all products in a specific category"""
    category = Category.query.get_or_404(category_id)
    products = Product.query.filter_by(category_id=category_id).all()
    categories = Category.query.all()
    return render_template('products.html', title=category.name, category=category, products=products, categories=categories, view_mode='category')

@main_bp.route('/categories')
def all_categories():
    """View all product categories"""
    categories = Category.query.all()
    return render_template('category.html', title='All Categories', categories=categories)

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
    
    # Remove from wishlist if it exists
    wishlist_item = Wishlist.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if wishlist_item:
        db.session.delete(wishlist_item)
    
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
        # Get form data
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        shipping_address = request.form.get('shipping_address')
        city = request.form.get('city')
        state = request.form.get('state')
        postal_code = request.form.get('postal_code')
        payment_method = request.form.get('payment_method')
        
        # Validate required fields
        if not all([full_name, email, phone, shipping_address, city, state, postal_code, payment_method]):
            flash('All fields are required', 'error')
            return redirect(url_for('main.checkout'))
        
        # Validate email format
        if '@' not in email:
            flash('Invalid email address', 'error')
            return redirect(url_for('main.checkout'))
        
        # Validate payment method
        valid_payment_methods = [Order.PAYMENT_CARD, Order.PAYMENT_CASH_ON_DELIVERY, Order.PAYMENT_PAYPAL]
        if payment_method not in valid_payment_methods:
            flash('Invalid payment method', 'error')
            return redirect(url_for('main.checkout'))
        
        # For card payment, redirect to payment page
        if payment_method == Order.PAYMENT_CARD:
            session['checkout_data'] = {
                'full_name': full_name,
                'email': email,
                'phone': phone,
                'shipping_address': shipping_address,
                'city': city,
                'state': state,
                'postal_code': postal_code,
                'payment_method': payment_method
            }
            return redirect(url_for('main.payment_card'))
        
        # For non-card payments, create orders directly
        try:
            cart_total = cart.get_total()
            
            # Create orders for each item in cart
            for item in cart.items:
                # Generate random tracking number
                tracking_number = f"WTS{datetime.utcnow().strftime('%Y%m%d')}{secrets.token_hex(4).upper()}"
                # Generate unique transaction ID
                transaction_id = f"TXN{datetime.utcnow().strftime('%Y%m%d%H%M%S')}{secrets.token_hex(6).upper()}"
                
                order = Order(
                    user_id=current_user.id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    total_price=item.product.price * item.quantity,
                    full_name=full_name,
                    email=email,
                    phone=phone,
                    shipping_address=shipping_address,
                    city=city,
                    state=state,
                    postal_code=postal_code,
                    payment_method=payment_method,
                    payment_status=Order.PAYMENT_COMPLETED if payment_method == Order.PAYMENT_PAYPAL else Order.PAYMENT_PENDING,
                    tracking_number=tracking_number,
                    transaction_id=transaction_id
                )
                db.session.add(order)
            
            # Clear cart
            CartItem.query.filter_by(cart_id=cart.id).delete()
            db.session.commit()
            
            flash('Order placed successfully! Check your email for confirmation.', 'success')
            return redirect(url_for('main.orders'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while placing your order. Please try again.', 'error')
            return redirect(url_for('main.checkout'))
    
    return render_template('checkout.html', title='Checkout', cart=cart, user=current_user)

@main_bp.route('/payment/card', methods=['GET', 'POST'])
@login_required
def payment_card():
    """Process credit card payment"""
    checkout_data = session.get('checkout_data')
    
    if not checkout_data:
        flash('Invalid payment session. Please start checkout again.', 'error')
        return redirect(url_for('main.checkout'))
    
    cart = current_user.cart
    
    if not cart or not cart.items:
        flash('Your cart is empty', 'warning')
        return redirect(url_for('main.view_cart'))
    
    if request.method == 'POST':
        # Get card details from form
        card_holder = request.form.get('card_holder')
        card_number = request.form.get('card_number', '').replace(' ', '')
        expiry_month = request.form.get('expiry_month')
        expiry_year = request.form.get('expiry_year')
        cvv = request.form.get('cvv')
        save_card = request.form.get('save_card') == 'on'
        
        # Validate card details
        if not all([card_holder, card_number, expiry_month, expiry_year, cvv]):
            flash('All card fields are required', 'error')
            return redirect(url_for('main.payment_card'))
        
        # Basic card validation
        if len(card_number) not in [13, 14, 15, 16]:
            flash('Invalid card number', 'error')
            return redirect(url_for('main.payment_card'))
        
        if not card_number.isdigit():
            flash('Card number must contain only digits', 'error')
            return redirect(url_for('main.payment_card'))
        
        if len(cvv) not in [3, 4]:
            flash('Invalid CVV', 'error')
            return redirect(url_for('main.payment_card'))
        
        if not cvv.isdigit():
            flash('CVV must contain only digits', 'error')
            return redirect(url_for('main.payment_card'))
        
        try:
            # Process payment (simulated)
            # In a real app, this would call a payment gateway like Stripe or PayPal
            
            # Create orders for each item in cart
            for item in cart.items:
                # Generate random tracking number
                tracking_number = f"WTS{datetime.utcnow().strftime('%Y%m%d')}{secrets.token_hex(4).upper()}"
                # Generate unique transaction ID
                transaction_id = f"TXN{datetime.utcnow().strftime('%Y%m%d%H%M%S')}{secrets.token_hex(6).upper()}"
                
                order = Order(
                    user_id=current_user.id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    total_price=item.product.price * item.quantity,
                    full_name=checkout_data['full_name'],
                    email=checkout_data['email'],
                    phone=checkout_data['phone'],
                    shipping_address=checkout_data['shipping_address'],
                    city=checkout_data['city'],
                    state=checkout_data['state'],
                    postal_code=checkout_data['postal_code'],
                    payment_method=Order.PAYMENT_CARD,
                    payment_status=Order.PAYMENT_COMPLETED,
                    tracking_number=tracking_number,
                    transaction_id=transaction_id
                )
                db.session.add(order)
            
            # Clear cart
            CartItem.query.filter_by(cart_id=cart.id).delete()
            db.session.commit()
            
            # Clear session data
            if 'checkout_data' in session:
                session.pop('checkout_data')
            
            flash('Payment successful! Your order has been confirmed.', 'success')
            return redirect(url_for('main.orders'))
        
        except Exception as e:
            db.session.rollback()
            flash('Payment processing failed. Please try again.', 'error')
            return redirect(url_for('main.payment_card'))
    
    return render_template('payment_card.html', title='Card Payment', checkout_data=checkout_data, cart=cart, user=current_user)

@main_bp.route('/orders')
@login_required
def orders():
    """View user orders"""
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('orders.html', title='My Orders', orders=orders)

# Admin decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You do not have permission to access this page.', 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

# Wishlist routes
@main_bp.route('/wishlist')
@login_required
def view_wishlist():
    """View user's wishlist"""
    wishlist_items = Wishlist.query.filter_by(user_id=current_user.id).all()
    return render_template('wishlist.html', title='My Wishlist', wishlist_items=wishlist_items)

@main_bp.route('/wishlist/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_wishlist(product_id):
    """Add product to wishlist"""
    product = Product.query.get_or_404(product_id)
    
    # Check if already in wishlist
    existing = Wishlist.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if existing:
        flash('Product already in wishlist!', 'warning')
        return redirect(url_for('main.products'))
    
    wishlist_item = Wishlist(user_id=current_user.id, product_id=product_id)
    db.session.add(wishlist_item)
    db.session.commit()
    
    flash(f'{product.name} added to wishlist!', 'success')
    return redirect(url_for('main.products'))

@main_bp.route('/wishlist/remove/<int:item_id>', methods=['POST'])
@login_required
def remove_from_wishlist(item_id):
    """Remove product from wishlist"""
    item = Wishlist.query.get_or_404(item_id)
    
    if item.user_id != current_user.id:
        flash('Unauthorized', 'error')
        return redirect(url_for('main.view_wishlist'))
    
    product_name = item.product.name
    db.session.delete(item)
    db.session.commit()
    
    flash(f'{product_name} removed from wishlist', 'success')
    return redirect(url_for('main.view_wishlist'))

# User dashboard
@main_bp.route('/dashboard')
@login_required
def dashboard():
    """User dashboard"""
    user_orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).limit(5).all()
    wishlist_count = Wishlist.query.filter_by(user_id=current_user.id).count()
    total_spent = db.session.query(db.func.sum(Order.total_price)).filter_by(user_id=current_user.id).scalar() or 0
    orders_count = Order.query.filter_by(user_id=current_user.id).count()
    
    return render_template('dashboard.html', 
                         title='My Dashboard',
                         user_orders=user_orders,
                         wishlist_count=wishlist_count,
                         total_spent=total_spent,
                         orders_count=orders_count)

# Admin dashboard routes
@main_bp.route('/admin')
@admin_required
def admin_dashboard():
    """Admin dashboard"""
    total_users = User.query.count()
    total_products = Product.query.count()
    total_orders = Order.query.count()
    total_revenue = db.session.query(db.func.sum(Order.total_price)).scalar() or 0
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(10).all()
    
    return render_template('admin/dashboard.html',
                         title='Admin Dashboard',
                         total_users=total_users,
                         total_products=total_products,
                         total_orders=total_orders,
                         total_revenue=total_revenue,
                         recent_orders=recent_orders)

@main_bp.route('/admin/products')
@admin_required
def admin_products():
    """Admin products management"""
    products = Product.query.all()
    return render_template('admin/products.html', title='Manage Products', products=products)

@main_bp.route('/admin/products/add', methods=['GET', 'POST'])
@admin_required
def admin_add_product():
    """Add new product"""
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        description = request.form.get('description')
        stock = request.form.get('stock')
        category_id = request.form.get('category_id')
        
        if not all([name, price, stock, category_id]):
            flash('Name, price, stock, and category are required', 'error')
            return redirect(url_for('main.admin_add_product'))
        
        product = Product(name=name, price=float(price), description=description, stock=int(stock), category_id=int(category_id))
        db.session.add(product)
        db.session.flush()  # Get the product ID without committing
        
        # Handle image upload
        if 'image' in request.files:
            file = request.files['image']
            image_filename = save_product_image(file, product.id)
            if image_filename:
                product.image_filename = image_filename
            elif file.filename != '':
                flash('Invalid file type. Only PNG, JPG, JPEG, and GIF are allowed.', 'error')
                db.session.rollback()
                return redirect(url_for('main.admin_add_product'))
        
        db.session.commit()
        flash('Product added successfully!', 'success')
        return redirect(url_for('main.admin_products'))
    
    categories = Category.query.all()
    return render_template('admin/add_product.html', title='Add Product', categories=categories)

@main_bp.route('/admin/products/edit/<int:product_id>', methods=['GET', 'POST'])
@admin_required
def admin_edit_product(product_id):
    """Edit product"""
    product = Product.query.get_or_404(product_id)
    
    if request.method == 'POST':
        product.name = request.form.get('name')
        product.price = float(request.form.get('price'))
        product.description = request.form.get('description')
        product.stock = int(request.form.get('stock'))
        product.category_id = int(request.form.get('category_id'))
        
        # Handle image upload
        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '':
                image_filename = save_product_image(file, product.id)
                if image_filename:
                    # Delete old image if exists
                    if product.image_filename:
                        old_image_path = os.path.join(os.path.dirname(__file__), 'static', 'images', 'products', product.image_filename)
                        if os.path.exists(old_image_path):
                            os.remove(old_image_path)
                    product.image_filename = image_filename
                else:
                    flash('Invalid file type. Only PNG, JPG, JPEG, and GIF are allowed.', 'error')
                    return redirect(url_for('main.admin_edit_product', product_id=product.id))
        
        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('main.admin_products'))
    
    categories = Category.query.all()
    return render_template('admin/edit_product.html', title='Edit Product', product=product, categories=categories)

@main_bp.route('/admin/products/delete/<int:product_id>')
@admin_required
def admin_delete_product(product_id):
    """Delete product"""
    product = Product.query.get_or_404(product_id)
    product_name = product.name
    db.session.delete(product)
    db.session.commit()
    
    flash(f'Product "{product_name}" deleted successfully!', 'success')
    return redirect(url_for('main.admin_products'))

@main_bp.route('/admin/products/<int:product_id>/toggle-feature', methods=['POST'])
@admin_required
def admin_toggle_product_feature(product_id):
    """Toggle product featured status"""
    product = Product.query.get_or_404(product_id)
    product.is_featured = not product.is_featured
    db.session.commit()
    
    return jsonify({
        'success': True,
        'is_featured': product.is_featured
    })

@main_bp.route('/admin/orders')
@admin_required
def admin_orders():
    """Admin orders management"""
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('admin/orders.html', title='Manage Orders', orders=orders)

@main_bp.route('/admin/orders/<int:order_id>/status/<new_status>')
@admin_required
def admin_update_order_status(order_id, new_status):
    """Update order status"""
    order = Order.query.get_or_404(order_id)
    valid_statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']
    
    if new_status not in valid_statuses:
        flash('Invalid status', 'error')
        return redirect(url_for('main.admin_orders'))
    
    order.status = new_status
    db.session.commit()
    
    flash(f'Order status updated to {new_status}', 'success')
    return redirect(url_for('main.admin_orders'))

@main_bp.route('/admin/users')
@admin_required
def admin_users():
    """Admin users management"""
    users = User.query.all()
    return render_template('admin/users.html', title='Manage Users', users=users)

@main_bp.route('/admin/users/<int:user_id>/make-admin')
@admin_required
def admin_make_admin(user_id):
    """Make user admin"""
    user = User.query.get_or_404(user_id)
    user.is_admin = True
    db.session.commit()
    
    flash(f'{user.username} is now an admin', 'success')
    return redirect(url_for('main.admin_users'))

@main_bp.route('/admin/users/<int:user_id>/remove-admin')
@admin_required
def admin_remove_admin(user_id):
    """Remove admin privileges"""
    user = User.query.get_or_404(user_id)
    user.is_admin = False
    db.session.commit()
    
    flash(f'{user.username} admin privileges removed', 'success')
    return redirect(url_for('main.admin_users'))

@main_bp.route('/admin/users/<int:user_id>/delete', methods=['POST'])
@admin_required
def admin_delete_user(user_id):
    """Delete a user"""
    user = User.query.get_or_404(user_id)
    
    # Prevent deleting the current user
    if user.id == current_user.id:
        flash('You cannot delete your own account', 'error')
        return redirect(url_for('main.admin_users'))
    
    username = user.username
    
    # Delete user's cart if it exists
    if user.cart:
        db.session.delete(user.cart)
    
    # Delete user's wishlist items
    for wishlist_item in user.wishlist_items:
        db.session.delete(wishlist_item)
    
    # Delete the user
    db.session.delete(user)
    db.session.commit()
    
    flash(f'User "{username}" deleted successfully', 'success')
    return redirect(url_for('main.admin_users'))
