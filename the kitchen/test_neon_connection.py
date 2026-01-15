import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def test_connection():
    try:
        # Test with individual credentials
        conn = psycopg2.connect(
            host=os.environ.get("DB_HOST"),
            database=os.environ.get("DB_NAME"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
            sslmode=os.environ.get("DB_SSLMODE", "require")
        )
        print("✅ Connection successful with individual credentials!")
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Individual credentials failed: {e}")
    
    try:
        # Test with connection string
        conn_string = os.environ.get("NEON_CONNECTION_STRING")
        if conn_string:
            conn = psycopg2.connect(conn_string)
            print("✅ Connection successful with connection string!")
            conn.close()
            return True
    except Exception as e:
        print(f"❌ Connection string failed: {e}")
    
    return False

if __name__ == "__main__":
    print("Testing Neon database connection...")
    print(f"DB_HOST: {os.environ.get('DB_HOST')}")
    print(f"DB_USER: {os.environ.get('DB_USER')}")
    print(f"DB_NAME: {os.environ.get('DB_NAME')}")
    print(f"DB_PASSWORD length: {len(os.environ.get('DB_PASSWORD', ''))}")
    print("-" * 50)
    
    test_connection()
