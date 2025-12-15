from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    """Application factory function"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
    
    # SQLite database configuration
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    instance_path = os.path.join(basedir, 'instance')
    os.makedirs(instance_path, exist_ok=True)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(instance_path, "store.db")}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
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
        db.create_all()
        
        # Seed database with initial data if empty
        from app.models import Product
        if Product.query.first() is None:
            products = [
                Product(name='Teddy Bear', price=19.99, description='Cute and cuddly teddy bear', stock=50),
                Product(name='Building Blocks', price=29.99, description='Colorful building blocks set', stock=35),
                Product(name='Action Figure', price=24.99, description='Superhero action figure', stock=40),
                Product(name='Doll House', price=49.99, description='Beautiful dollhouse with furniture', stock=20),
                Product(name='Board Game', price=34.99, description='Fun family board game', stock=30),
            ]
            for product in products:
                db.session.add(product)
            db.session.commit()
    
    return app
