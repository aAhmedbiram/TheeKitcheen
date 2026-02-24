#!/usr/bin/env python3
"""
Migration script to add missing columns to OrderItem table
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app import app
from extensions import db
from sqlalchemy import text

def fix_orderitem_schema():
    """Add missing columns to OrderItem table"""
    
    with app.app_context():
        try:
            print("🔄 Fixing OrderItem table schema...")
            
            # Check current columns
            result = db.session.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'order_items' 
                ORDER BY ordinal_position
            """))
            current_columns = [row[0] for row in result.fetchall()]
            print(f"📋 Current columns: {current_columns}")
            
            # Add missing columns
            missing_columns = [
                ("item_name", "ALTER TABLE order_items ADD COLUMN item_name VARCHAR(255)"),
                ("line_total", "ALTER TABLE order_items ADD COLUMN line_total NUMERIC(10, 2)"),
            ]
            
            for column_name, sql in missing_columns:
                if column_name not in current_columns:
                    print(f"➕ Adding {column_name}")
                    db.session.execute(text(sql))
                else:
                    print(f"✅ {column_name} already exists")
            
            db.session.commit()
            print("✅ OrderItem schema fix completed!")
            
            # Verify final schema
            result = db.session.execute(text("""
                SELECT column_name, data_type, is_nullable 
                FROM information_schema.columns 
                WHERE table_name = 'order_items' 
                ORDER BY ordinal_position
            """))
            print("\n📋 Final OrderItem table schema:")
            for row in result.fetchall():
                print(f"  {row[0]}: {row[1]} ({row[2]})")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Schema fix failed: {e}")
            raise

if __name__ == "__main__":
    fix_orderitem_schema()
