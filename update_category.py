#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, '/app')
os.chdir('/app')

from app import create_app, db
from app.models import Category

app = create_app()

with app.app_context():
    category = Category.query.filter_by(name='Mattel').first()
    if category:
        print(f'Before: {category.name}')
        category.name = 'Barbie'
        db.session.commit()
        print(f'After: {category.name}')
    else:
        print('Mattel category not found')
    
    # Verify all categories
    print('\nAll categories:')
    categories = Category.query.all()
    for cat in categories:
        print(f'  {cat.id}: {cat.name}')
