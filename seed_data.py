#!/usr/bin/env python
"""Seed script to create initial admin user and test data"""
from app import create_app, db
from app.models import User, Product

app = create_app()

with app.app_context():
    # Check if admin already exists
    admin_exists = User.query.filter_by(username='admin').first()
    if admin_exists:
        print("✓ Admin user already exists")
    else:
        # Create admin user
        admin = User(username='admin', email='admin@wonderland.com', is_admin=True)
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("✓ Admin user created: admin / admin123")
    
    # Create test products if none exist
    product_count = Product.query.count()
    if product_count == 0:
        products = [
            Product(name='Teddy Bear', price=19.99, description='Soft and cuddly teddy bear', stock=50),
            Product(name='Action Figure', price=29.99, description='Cool superhero action figure', stock=30),
            Product(name='Puzzle Game', price=14.99, description='Brain teaser puzzle set', stock=100),
            Product(name='Building Blocks', price=34.99, description='Colorful building blocks set', stock=45),
            Product(name='Remote Control Car', price=49.99, description='Fast RC car with turbo mode', stock=25),
        ]
        db.session.add_all(products)
        db.session.commit()
        print(f"✓ {len(products)} test products created")
    else:
        print(f"✓ {product_count} products already exist")

print("\n🎉 Seed data initialized!")
print("\nAdmin Login Credentials:")
print("  Username: admin")
print("  Password: admin123")
print("\nAccess admin panel at: http://localhost:5000/admin")
