#!/usr/bin/env python
"""Migration script to add is_featured column to existing database"""
import sqlite3
import os

def migrate_database():
    """Add is_featured column to products table if it doesn't exist"""
    db_path = os.path.join(os.path.dirname(__file__), 'instance', 'store.db')
    
    if not os.path.exists(db_path):
        print(f"❌ Database file not found at {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if is_featured column already exists
        cursor.execute("PRAGMA table_info(products)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'is_featured' in columns:
            print("✓ is_featured column already exists in products table")
            conn.close()
            return True
        
        # Add is_featured column with default value of False
        print("Adding is_featured column to products table...")
        cursor.execute("ALTER TABLE products ADD COLUMN is_featured BOOLEAN DEFAULT 0")
        conn.commit()
        
        print("✓ Successfully added is_featured column to products table")
        print("✓ All existing products set to not featured (is_featured=False)")
        
        # Verify the migration
        cursor.execute("PRAGMA table_info(products)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'is_featured' in columns:
            print("✓ Migration verified successfully!")
            conn.close()
            return True
        else:
            print("❌ Migration verification failed")
            conn.close()
            return False
            
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == '__main__':
    print("🔄 Starting database migration...\n")
    if migrate_database():
        print("\n✅ Database migration completed successfully!")
        print("You can now start the app normally.")
    else:
        print("\n❌ Database migration failed!")
