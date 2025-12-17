#!/usr/bin/env python
"""Seed script to create initial admin user and test data"""
from app import create_app, db
from app.models import User, Product, Category

app = create_app()

with app.app_context():
    # Create categories
    categories_data = [
        {'name': 'Lego', 'description': 'Building blocks and construction sets'},
        {'name': 'Masito (Toy Cars)', 'description': 'Toy cars and racing sets'},
        {'name': 'Plush toys', 'description': 'Soft and cuddly plush toys'},
        {'name': 'Board games', 'description': 'Family and strategy board games'},
        {'name': 'Arts and Crafts', 'description': 'Creative art and craft supplies'},
        {'name': 'Hotwheels', 'description': 'Die-cast model cars'},
    ]
    
    for cat_data in categories_data:
        if not Category.query.filter_by(name=cat_data['name']).first():
            category = Category(name=cat_data['name'], description=cat_data['description'])
            db.session.add(category)
    
    db.session.commit()
    print("✓ Categories created")
    
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
        lego_cat = Category.query.filter_by(name='Lego').first()
        cars_cat = Category.query.filter_by(name='Masito (Toy Cars)').first()
        plush_cat = Category.query.filter_by(name='Plush toys').first()
        games_cat = Category.query.filter_by(name='Board games').first()
        arts_cat = Category.query.filter_by(name='Arts and Crafts').first()
        hotwheels_cat = Category.query.filter_by(name='Hotwheels').first()
        
        products = [
            Product(name='Lego City Set', price=49.99, description='Build your own city with this classic Lego set', stock=20, category_id=lego_cat.id),
            Product(name='Lego Creator Space Rocket', price=79.99, description='Three models in one', stock=15, category_id=lego_cat.id),
            Product(name='Masito Sport Car', price=15.99, description='Fast and furious toy sports car', stock=30, category_id=cars_cat.id),
            Product(name='Masito Racing Set', price=34.99, description='Complete racing track with multiple cars', stock=25, category_id=cars_cat.id),
            Product(name='Soft Teddy Bear', price=24.99, description='Cuddly teddy bear perfect for all ages', stock=25, category_id=plush_cat.id),
            Product(name='Pink Bunny Plush', price=19.99, description='Adorable pink bunny plush toy', stock=20, category_id=plush_cat.id),
            Product(name='Classic Board Game Pack', price=39.99, description='Collection of classic family board games', stock=18, category_id=games_cat.id),
            Product(name='Strategy Chess Set', price=29.99, description='Professional wooden chess set', stock=22, category_id=games_cat.id),
            Product(name='Art Supplies Set', price=44.99, description='Complete set of markers, crayons, and colored pencils', stock=28, category_id=arts_cat.id),
            Product(name='DIY Craft Kit', price=32.99, description='Create your own jewelry and decorations', stock=16, category_id=arts_cat.id),
            Product(name='Hotwheels 5-Car Pack', price=12.99, description='Set of 5 die-cast Hotwheels cars', stock=35, category_id=hotwheels_cat.id),
            Product(name='Hotwheels Track Set', price=54.99, description='Exciting track set with looping and jumps', stock=12, category_id=hotwheels_cat.id),
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
