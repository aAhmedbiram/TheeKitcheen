#!/usr/bin/env python3
"""
Neon Database Connection Verification Script
Windows-friendly script to verify and fix Neon PostgreSQL connection issues.
"""

import os
import sys
from pathlib import Path
from urllib.parse import urlparse
from dotenv import load_dotenv

def _sanitize_db_url(db_url):
    """Sanitize database URL for logging (remove credentials)"""
    if not db_url:
        return "Not configured"
    
    try:
        parsed = urlparse(db_url)
        if parsed.scheme == 'postgresql':
            return f"{parsed.scheme}://[REDACTED]@{parsed.hostname}/{parsed.path.lstrip('/')}"
        else:
            return db_url
    except:
        return "Invalid URL format"

def _get_project_root():
    """Get project root directory"""
    # Start from current file and go up until we find indicators
    current = Path(__file__).resolve().parent
    while current != current.parent:
        if (current / 'app.py').exists() and (current / 'config.py').exists():
            return current
        current = current.parent
    return Path.cwd()  # Fallback to current directory

def main():
    """Main verification function"""
    print("🔍 Neon Database Connection Verification")
    print("=" * 50)
    
    # 1. Check current working directory
    project_root = _get_project_root()
    current_dir = Path.cwd()
    print(f"📁 Current working directory: {current_dir}")
    print(f"📁 Project root detected: {project_root}")
    
    # 2. Check .env file existence
    env_file = project_root / '.env'
    env_exists = env_file.exists()
    print(f"📄 .env file exists: {env_exists}")
    if env_exists:
        print(f"📄 .env file location: {env_file}")
    else:
        print("❌ .env file NOT found in project root!")
    
    # 3. Load .env and check DATABASE_URL
    print("\n🔧 Loading environment variables...")
    try:
        # Load .env from project root
        load_dotenv(dotenv_path=env_file, override=False)
        print("✅ .env loaded successfully")
    except Exception as e:
        print(f"❌ Error loading .env: {e}")
        return 1
    
    # 4. Check DATABASE_URL environment variable
    raw_db_url = os.getenv('DATABASE_URL')
    print(f"\n🔗 DATABASE_URL environment variable:")
    print(f"   Set: {'Yes' if raw_db_url else 'No'}")
    if raw_db_url:
        sanitized = _sanitize_db_url(raw_db_url)
        print(f"   Value: {sanitized}")
    
    # 5. Check what Config uses
    print(f"\n⚙️  Configuration check:")
    try:
        # Import config after loading .env
        sys.path.insert(0, str(project_root))
        from config import Config
        
        config_uri = Config.SQLALCHEMY_DATABASE_URI
        sanitized_config = _sanitize_db_url(config_uri)
        print(f"   Config.SQLALCHEMY_DATABASE_URI: {sanitized_config}")
        print(f"   Config.ENV: {Config.ENV}")
        print(f"   Config.USING_SQLITE: {getattr(Config, 'USING_SQLITE', 'Not Available')}")
        
    except Exception as e:
        print(f"❌ Error importing config: {e}")
        return 1
    
    # 6. Determine action needed
    print(f"\n🎯 Analysis:")
    
    if not env_exists:
        print("❌ ACTION REQUIRED: .env file missing")
        print("\n📋 Steps to fix:")
        print(f"1. Create .env file in: {project_root}")
        print("2. Copy content from .env.example")
        print("3. Set DATABASE_URL to your Neon connection string")
        print("4. Restart your terminal/PowerShell session")
        return 1
    
    elif not raw_db_url:
        print("❌ ACTION REQUIRED: DATABASE_URL not set in .env")
        print("\n📋 Steps to fix:")
        print(f"1. Edit .env file: {env_file}")
        print("2. Add: DATABASE_URL=postgresql://USER:PASSWORD@HOST/neondb?sslmode=require")
        print("3. Replace with your actual Neon connection string")
        print("4. Restart your terminal/PowerShell session")
        return 1
    
    elif config_uri.startswith('sqlite'):
        print("❌ ACTION REQUIRED: SQLite detected - Neon PostgreSQL required")
        print("\n📋 Steps to fix:")
        print(f"1. Edit .env file: {env_file}")
        print("2. Set DATABASE_URL to your Neon PostgreSQL connection string")
        print("3. Remove any SQLite database references")
        print("4. Restart your terminal/PowerShell session")
        return 1
    
    # 7. Test database connection
    print(f"\n🔌 Testing database connection...")
    try:
        from sqlalchemy import create_engine, text
        
        # Create engine with the configured URI
        engine = create_engine(config_uri)
        
        # Test connection and get fingerprint
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT 
                    current_database() as database,
                    current_user as user,
                    inet_server_addr() as server_ip,
                    version() as version
            """))
            
            if result.returns_rows:
                row = result.fetchone()
                result_dict = {
                    'database': row[0],
                    'user': row[1], 
                    'server_ip': row[2],
                    'version': row[3]
                }
            else:
                raise Exception("No rows returned from database query")
            
            print("✅ Database connection successful!")
            print(f"📊 Database fingerprint:")
            print(f"   Database: {result_dict['database']}")
            print(f"   User: {result_dict['user']}")
            print(f"   Server IP: {result_dict['server_ip']}")
            print(f"   Version: {result_dict['version'][:50]}...")
            
            # Verify it's PostgreSQL
            if 'postgresql' in result_dict['version'].lower():
                print("✅ Connected to PostgreSQL (Neon)")
                return 0
            else:
                print("⚠️  Connected to database, but not PostgreSQL")
                return 1
                
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("\n📋 Possible causes:")
        print("1. Invalid connection string")
        print("2. Network connectivity issues")
        print("3. Neon database is not running")
        print("4. Incorrect credentials")
        return 1

if __name__ == "__main__":
    exit_code = main()
    print(f"\n{'='*50}")
    if exit_code == 0:
        print("✅ Verification PASSED - Connected to Neon PostgreSQL")
    else:
        print("❌ Verification FAILED - See steps above to fix")
    sys.exit(exit_code)
