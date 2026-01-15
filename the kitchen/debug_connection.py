import os
from dotenv import load_dotenv

load_dotenv()

print("=== NEON CONNECTION DEBUG ===")
print(f"Project Name: the kitchen")
print(f"DB_USER: {os.environ.get('DB_USER')}")
print(f"DB_PASSWORD: {os.environ.get('DB_PASSWORD')}")
print(f"DB_HOST: {os.environ.get('DB_HOST')}")
print(f"DB_NAME: {os.environ.get('DB_NAME')}")
print(f"DB_SSLMODE: {os.environ.get('DB_SSLMODE')}")
print()

print("=== CONNECTION STRING ===")
conn_str = os.environ.get('NEON_CONNECTION_STRING')
print(f"Full connection string: {conn_str}")
print()

# Try to parse and show components
if conn_str:
    try:
        import urllib.parse
        parsed = urllib.parse.urlparse(conn_str)
        print(f"Parsed username: {parsed.username}")
        print(f"Parsed password: {parsed.password}")
        print(f"Parsed hostname: {parsed.hostname}")
        print(f"Parsed database: {parsed.path[1:]}")  # Remove leading /
        print(f"Parsed query: {parsed.query}")
    except Exception as e:
        print(f"Error parsing connection string: {e}")

print("\n=== POSSIBLE ISSUES ===")
print("1. Password might be incorrect")
print("2. Database name might be different")
print("3. Project might not be fully set up")
print("4. Connection string format might be wrong")
