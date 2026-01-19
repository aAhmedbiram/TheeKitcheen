from app import create_app
from extensions import db
from models import User
from werkzeug.security import generate_password_hash

app = create_app()
with app.app_context():
    # Check if admin user exists
    admin = User.query.filter_by(email='admin@thekitchen.com').first()
    if not admin:
        # Create admin user
        admin = User(
            first_name='Admin',
            last_name='User',
            email='admin@thekitchen.com',
            phone='00000000000',
            address='Admin Address',
            password_hash=generate_password_hash('admin123'),
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print('Admin user created successfully!')
        print('Email: admin@thekitchen.com')
        print('Password: admin123')
    else:
        print('Admin user already exists!')
