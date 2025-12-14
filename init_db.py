"""Database initialization and seeding script"""
from app import create_app, db
from app.models import Product, Order

def init_db():
    """Initialize the database"""
    app = create_app()
    
    with app.app_context():
        # Drop all tables and recreate them
        db.drop_all()
        db.create_all()
        
        # Add sample products
        products = [
            Product(name='Teddy Bear', price=19.99, description='Cute and cuddly teddy bear'),
            Product(name='Building Blocks', price=29.99, description='Colorful building blocks set'),
            Product(name='Action Figure', price=24.99, description='Superhero action figure'),
            Product(name='Doll House', price=49.99, description='Beautiful dollhouse with furniture'),
            Product(name='Board Game', price=34.99, description='Fun family board game'),
        ]
        
        for product in products:
            db.session.add(product)
        
        db.session.commit()
        print("✓ Database initialized successfully!")
        print(f"✓ Added {len(products)} sample products")

if __name__ == '__main__':
    init_db()
