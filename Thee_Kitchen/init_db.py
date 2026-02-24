from app import app
from extensions import db
from models import User, MenuItem

def check_existing_tables():
    """Check existing database tables"""
    with app.app_context():
        # Check if users table exists and its structure
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"Existing tables: {tables}")
        
        if 'users' in tables:
            columns = inspector.get_columns('users')
            print(f"Users table columns: {[col['name'] for col in columns]}")

def init_db():
    """Initialize the database with tables"""
    with app.app_context():
        # Create all tables (will skip existing ones)
        db.create_all()
        print("Database tables created/verified successfully!")

def create_admin_user():
    """Create an admin user for testing"""
    with app.app_context():
        try:
            # Check if admin user already exists (using name instead of username)
            admin = User.query.filter_by(name='admin').first()
            if not admin:
                admin = User(
                    name='admin',
                    email='admin@theekitchen.com',
                    phone='01234567890',
                    is_admin=True  # Changed from is_verified to is_admin
                )
                admin.set_password('admin123')
                db.session.add(admin)
                db.session.commit()
                print("Admin user created successfully!")
            else:
                print("Admin user already exists!")
        except Exception as e:
            print(f"Error creating admin user: {e}")

def create_sample_menu_items():
    """Create sample menu items for testing"""
    with app.app_context():
        try:
            # Check if menu items already exist
            if MenuItem.query.count() > 0:
                print("Sample menu items already exist!")
                return
            
            # Add sample menu items
            menu_items = [
                MenuItem(
                    name_ar="كبدة دجاج",
                    name_en="Chicken Liver",
                    description_ar="كبدة دجاج طازجة مع التوابل",
                    description_en="Fresh chicken liver with spices",
                    price=45.0,
                    category="main"
                ),
                MenuItem(
                    name_ar="أرز بالشعيرية",
                    name_en="Rice with Vermicelli",
                    description_ar="أرز أبيض مع الشعيرية",
                    description_en="White rice with vermicelli",
                    price=15.0,
                    category="side"
                ),
                MenuItem(
                    name_ar="سلطة طحينة",
                    name_en="Tahini Salad",
                    description_ar="سلطة طحينة بالخضار",
                    description_en="Tahini salad with vegetables",
                    price=20.0,
                    category="appetizer"
                )
            ]
            
            for item in menu_items:
                db.session.add(item)
            
            db.session.commit()
            print(f"✅ {len(menu_items)} sample menu items created successfully!")
            
        except Exception as e:
            print(f"Error creating sample menu items: {e}")
            db.session.rollback()

if __name__ == '__main__':
    check_existing_tables()
    init_db()
    create_admin_user()
    create_sample_menu_items()
