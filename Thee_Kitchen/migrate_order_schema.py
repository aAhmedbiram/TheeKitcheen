#!/usr/bin/env python3
"""
Migration script to update Order table schema for guest orders support
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

def migrate_order_table():
    """Update Order table schema to support guest orders"""
    
    with app.app_context():
        try:
            print("🔄 Starting Order table migration...")
            
            # Check current schema
            result = db.session.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'orders' 
                ORDER BY ordinal_position
            """))
            current_columns = [row[0] for row in result.fetchall()]
            print(f"📋 Current columns: {current_columns}")
            
            # Add missing columns
            migrations = [
                # Add distance_km if missing
                ("distance_km", "NUMERIC(10, 2)", "ALTER TABLE orders ADD COLUMN distance_km NUMERIC(10, 2)"),
                
                # Add total if missing (rename from total_amount)
                ("total", "NUMERIC(10, 2)", "ALTER TABLE orders ADD COLUMN total NUMERIC(10, 2)"),
                
                # Add deposit_amount if missing (rename from advance_amount)
                ("deposit_amount", "NUMERIC(10, 2)", "ALTER TABLE orders ADD COLUMN deposit_amount NUMERIC(10, 2)"),
                
                # Add address_text if missing
                ("address_text", "TEXT", "ALTER TABLE orders ADD COLUMN address_text TEXT"),
                
                # Add customer_lat if missing
                ("customer_lat", "FLOAT", "ALTER TABLE orders ADD COLUMN customer_lat FLOAT"),
                
                # Add customer_lng if missing
                ("customer_lng", "FLOAT", "ALTER TABLE orders ADD COLUMN customer_lng FLOAT"),
                
                # Add customer_name if missing
                ("customer_name", "VARCHAR(80)", "ALTER TABLE orders ADD COLUMN customer_name VARCHAR(80) NOT NULL DEFAULT 'Guest Customer'"),
                
                # Add customer_phone if missing
                ("customer_phone", "VARCHAR(20)", "ALTER TABLE orders ADD COLUMN customer_phone VARCHAR(20) NOT NULL DEFAULT '0000000000'"),
                
                # Make user_id nullable for guest orders
                ("user_id_nullable", "INTEGER", "ALTER TABLE orders ALTER COLUMN user_id DROP NOT NULL"),
            ]
            
            for column_name, data_type, sql in migrations:
                if column_name not in current_columns:
                    print(f"➕ Adding {column_name}: {data_type}")
                    db.session.execute(text(sql))
                else:
                    print(f"✅ {column_name} already exists")
            
            # Handle column renames/migrations
            if "total_amount" in current_columns and "total" not in current_columns:
                print("🔄 Renaming total_amount to total")
                db.session.execute(text("ALTER TABLE orders RENAME COLUMN total_amount TO total"))
            
            if "advance_amount" in current_columns and "deposit_amount" not in current_columns:
                print("🔄 Renaming advance_amount to deposit_amount")
                db.session.execute(text("ALTER TABLE orders RENAME COLUMN advance_amount TO deposit_amount"))
            
            if "delivery_address" in current_columns and "address_text" not in current_columns:
                print("🔄 Renaming delivery_address to address_text")
                db.session.execute(text("ALTER TABLE orders RENAME COLUMN delivery_address TO address_text"))
            
            # Make user_id nullable if it's not already
            if "user_id" in current_columns:
                print("🔄 Making user_id nullable for guest orders")
                try:
                    db.session.execute(text("ALTER TABLE orders ALTER COLUMN user_id DROP NOT NULL"))
                except Exception as e:
                    print(f"⚠️  Could not make user_id nullable: {e}")
            
            db.session.commit()
            print("✅ Migration completed successfully!")
            
            # Verify new schema
            result = db.session.execute(text("""
                SELECT column_name, data_type, is_nullable 
                FROM information_schema.columns 
                WHERE table_name = 'orders' 
                ORDER BY ordinal_position
            """))
            print("\n📋 Updated Order table schema:")
            for row in result.fetchall():
                print(f"  {row[0]}: {row[1]} ({row[2]})")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Migration failed: {e}")
            raise

if __name__ == "__main__":
    migrate_order_table()
