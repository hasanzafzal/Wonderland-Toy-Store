from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from sqlalchemy import inspect, text, event
from sqlalchemy.pool import StaticPool

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    """Application factory function"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
    
    # SQLite database configuration
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    instance_path = os.path.join(basedir, 'instance')
    
    try:
        os.makedirs(instance_path, exist_ok=True)
        # Ensure instance directory is writable
        os.chmod(instance_path, 0o777)
    except (OSError, PermissionError):
        # Vercel's filesystem may not allow chmod, ignore
        pass
    
    db_path = os.path.join(instance_path, 'store.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}?timeout=10&check_same_thread=False'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'connect_args': {
            'timeout': 10,
            'check_same_thread': False
        }
    }
    
    # Initialize database
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'
    
    # User loader for flask-login
    from app.models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Register blueprints
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    # Create tables and seed data
    with app.app_context():
        # Enable WAL mode for SQLite for better concurrency
        @event.listens_for(db.engine, 'connect')
        def set_sqlite_pragma(dbapi_conn, connection_record):
            if 'sqlite' in str(db.engine.url):
                cursor = dbapi_conn.cursor()
                cursor.execute('PRAGMA journal_mode=WAL')
                cursor.execute('PRAGMA synchronous=NORMAL')
                cursor.execute('PRAGMA cache_size=-64000')
                cursor.execute('PRAGMA foreign_keys=ON')
                cursor.close()
        
        db.create_all()
        
        # Ensure database file has proper permissions
        db_path = os.path.join(instance_path, 'store.db')
        if os.path.exists(db_path):
            try:
                os.chmod(db_path, 0o666)
            except (OSError, PermissionError):
                # Vercel's filesystem may not allow chmod, ignore
                pass
        
        # Add category_id column to products table if it doesn't exist
        inspector = inspect(db.engine)
        products_columns = [col['name'] for col in inspector.get_columns('products')]
        orders_columns = [col['name'] for col in inspector.get_columns('orders')]
        
        # Helper function to refresh column list
        def refresh_columns():
            nonlocal products_columns, orders_columns
            inspector = inspect(db.engine)
            products_columns = [col['name'] for col in inspector.get_columns('products')]
            orders_columns = [col['name'] for col in inspector.get_columns('orders')]
        
        if 'category_id' not in products_columns:
            try:
                with db.engine.connect() as connection:
                    connection.execute(text('ALTER TABLE products ADD COLUMN category_id INTEGER'))
                    connection.commit()
                refresh_columns()
            except:
                pass
        
        # Add image_filename column to products table if it doesn't exist
        if 'image_filename' not in products_columns:
            try:
                with db.engine.connect() as connection:
                    connection.execute(text('ALTER TABLE products ADD COLUMN image_filename VARCHAR(255)'))
                    connection.commit()
                refresh_columns()
            except:
                pass
        
        # Add shipping and payment columns to orders table if they don't exist
        order_columns_to_add = [
            ('full_name', 'VARCHAR(200)'),
            ('email', 'VARCHAR(120)'),
            ('phone', 'VARCHAR(20)'),
            ('city', 'VARCHAR(100)'),
            ('state', 'VARCHAR(100)'),
            ('postal_code', 'VARCHAR(20)'),
            ('payment_method', "VARCHAR(50) DEFAULT 'cash_on_delivery'"),
            ('payment_status', "VARCHAR(20) DEFAULT 'pending'"),
            ('transaction_id', 'VARCHAR(100)'),
        ]
        
        for column_name, column_type in order_columns_to_add:
            if column_name not in orders_columns:
                try:
                    with db.engine.connect() as connection:
                        connection.execute(text(f'ALTER TABLE orders ADD COLUMN {column_name} {column_type}'))
                        connection.commit()
                    refresh_columns()
                except Exception as e:
                    # Column might already exist or other error - continue
                    pass
        
        # Fix any empty string datetime values in users table
        with db.engine.connect() as connection:
            try:
                connection.execute(text("UPDATE users SET reset_token_expires = NULL WHERE reset_token_expires = ''"))
                connection.commit()
            except:
                pass  # If the operation fails, it's okay
        
        # Seed database with initial data if empty
        from app.models import Product, Category
        
        # Create categories if they don't exist
        if Category.query.first() is None:
            categories_data = [
                {'name': 'Lego', 'description': 'Building blocks and construction sets'},
                {'name': 'Plush toys', 'description': 'Soft and cuddly plush toys'},
                {'name': 'Board games', 'description': 'Family and strategy board games'},
                {'name': 'Arts and Crafts', 'description': 'Creative art and craft supplies'},
                {'name': 'Hotwheels', 'description': 'Die-cast model cars'},
            ]
            for cat_data in categories_data:
                category = Category(name=cat_data['name'], description=cat_data['description'])
                db.session.add(category)
            db.session.commit()
        
        if Product.query.first() is None:
            lego_cat = Category.query.filter_by(name='Lego').first()
            products = [
                Product(name='Teddy Bear', price=19.99, description='Cute and cuddly teddy bear', stock=50, category_id=None),
                Product(name='Building Blocks', price=29.99, description='Colorful building blocks set', stock=35, category_id=lego_cat.id if lego_cat else None),
                Product(name='Action Figure', price=24.99, description='Superhero action figure', stock=40, category_id=None),
                Product(name='Doll House', price=49.99, description='Beautiful dollhouse with furniture', stock=20, category_id=None),
                Product(name='Board Game', price=34.99, description='Fun family board game', stock=30, category_id=None),
            ]
            for product in products:
                db.session.add(product)
            db.session.commit()
    
    return app
