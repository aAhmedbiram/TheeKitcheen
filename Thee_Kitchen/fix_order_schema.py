#!/usr/bin/env python3
"""
Simple migration script to add missing columns to Order table
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

def fix_order_schema():
    """Add missing columns to Order table"""
    
    with app.app_context():
        try:
            print("🔄 Fixing Order table schema...")
            
            # Check current columns
            result = db.session.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'orders' 
                ORDER BY ordinal_position
            """))
            current_columns = [row[0] for row in result.fetchall()]
            print(f"📋 Current columns: {current_columns}")
            
            # Add only the missing columns
            missing_columns = [
                ("distance_km", "ALTER TABLE orders ADD COLUMN distance_km NUMERIC(10, 2)"),
                ("customer_lat", "ALTER TABLE orders ADD COLUMN customer_lat FLOAT"),
                ("customer_lng", "ALTER TABLE orders ADD COLUMN customer_lng FLOAT"),
                ("customer_name", "ALTER TABLE orders ADD COLUMN customer_name VARCHAR(80)"),
                ("customer_phone", "ALTER TABLE orders ADD COLUMN customer_phone VARCHAR(20)"),
            ]
            
            for column_name, sql in missing_columns:
                if column_name not in current_columns:
                    print(f"➕ Adding {column_name}")
                    db.session.execute(text(sql))
                else:
                    print(f"✅ {column_name} already exists")
            
            # Handle column renames if needed
            if "total_amount" in current_columns and "total" not in current_columns:
                print("🔄 Renaming total_amount to total")
                db.session.execute(text("ALTER TABLE orders RENAME COLUMN total_amount TO total"))
            
            if "advance_amount" in current_columns and "deposit_amount" not in current_columns:
                print("🔄 Renaming advance_amount to deposit_amount")
                db.session.execute(text("ALTER TABLE orders RENAME COLUMN advance_amount TO deposit_amount"))
            
            if "delivery_address" in current_columns and "address_text" not in current_columns:
                print("🔄 Renaming delivery_address to address_text")
                db.session.execute(text("ALTER TABLE orders RENAME COLUMN delivery_address TO address_text"))
            
            # Make user_id nullable for guest orders
            if "user_id" in current_columns:
                print("🔄 Making user_id nullable for guest orders")
                try:
                    db.session.execute(text("ALTER TABLE orders ALTER COLUMN user_id DROP NOT NULL"))
                except Exception as e:
                    print(f"⚠️  Could not make user_id nullable: {e}")
            
            db.session.commit()
            print("✅ Schema fix completed!")
            
            # Verify final schema
            result = db.session.execute(text("""
                SELECT column_name, data_type, is_nullable 
                FROM information_schema.columns 
                WHERE table_name = 'orders' 
                ORDER BY ordinal_position
            """))
            print("\n📋 Final Order table schema:")
            for row in result.fetchall():
                print(f"  {row[0]}: {row[1]} ({row[2]})")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Schema fix failed: {e}")
            raise

if __name__ == "__main__":
    fix_order_schema()
