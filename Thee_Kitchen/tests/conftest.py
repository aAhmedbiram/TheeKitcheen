import os
import sys
import pytest
import warnings
from flask import session

# Suppress SQLAlchemy warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)
warnings.filterwarnings('ignore', message='.*datetime.utcnow.*')
warnings.filterwarnings('ignore', message='.*Query.get.*')

# Add project root to sys.path for reliable imports on Windows
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Set test database URI before importing app to avoid initialization error
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'

# Import correctly - avoid shadowing fixture names
from app import app as flask_app
from extensions import db
from models import User, MenuItem, Order, OrderItem


@pytest.fixture
def app():
    """Create application for testing with proper configuration"""
    # Configure app for testing
    flask_app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'WTF_CSRF_ENABLED': False,
        'SECRET_KEY': 'test-secret-key'
    })
    
    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


@pytest.fixture(autouse=True)
def _db_cleanup(app):
    """Automatic database cleanup after each test"""
    yield
    with app.app_context():
        db.session.rollback()
        db.session.remove()


@pytest.fixture
def sample_user(app):
    """Create a sample user for testing and return user ID"""
    with app.app_context():
        user = User(
            name='Test User',
            email='test@example.com',
            phone='01234567890',
            is_admin=False
        )
        user.set_password('testpassword')
        db.session.add(user)
        db.session.commit()
        return user.id


@pytest.fixture
def sample_user_obj(app, sample_user):
    """Get the actual user object for tests that need it"""
    with app.app_context():
        return db.session.get(User, sample_user)


@pytest.fixture
def logged_in_client(client, app, sample_user):
    """Create a client with logged in user"""
    with app.app_context():
        user = db.session.get(User, sample_user)
        with client.session_transaction() as sess:
            sess['user_id'] = user.id
            sess['user_name'] = user.name
            sess['is_admin'] = False
            sess['lang'] = 'en'
    return client


@pytest.fixture
def sample_cart_items():
    """Create sample cart items for testing"""
    return [
        {
            'id': 1,
            'name': 'Test Item 1',
            'price': 100.0,
            'quantity': 2
        },
        {
            'id': 2,
            'name': 'Test Item 2',
            'price': 50.0,
            'quantity': 1
        }
    ]


@pytest.fixture
def sample_menu_items(app):
    """Create sample menu items for testing"""
    with app.app_context():
        items = [
            MenuItem(
                name_ar='طبق اختبار',
                name_en='Test Dish',
                description_ar='وصف اختبار',
                description_en='Test description',
                price=100.0,
                category='main'
            ),
            MenuItem(
                name_ar='طبق اختبار 2',
                name_en='Test Dish 2',
                description_ar='وصف اختبار 2',
                description_en='Test description 2',
                price=50.0,
                category='main'
            )
        ]
        
        for item in items:
            db.session.add(item)
        db.session.commit()
        
        return items


def login_user(client, user, app=None):
    """Helper to login a user"""
    if isinstance(user, int):
        # user is an ID, fetch the user object
        if app:
            with app.app_context():
                user_obj = db.session.get(User, user)
                user_id = user_obj.id
                user_name = user_obj.name
                is_admin = user_obj.is_admin
        else:
            # Fallback for tests that don't pass app fixture
            user_id = user
            user_name = 'Test User'
            is_admin = False
    else:
        # user is an object
        user_id = user.id
        user_name = user.name
        is_admin = user.is_admin if hasattr(user, 'is_admin') else False
    
    with client.session_transaction() as sess:
        sess['user_id'] = user_id
        sess['user_name'] = user_name
        sess['is_admin'] = is_admin
        sess['lang'] = 'en'


def set_cart_in_session(client, cart_items):
    """Helper to set cart in session"""
    with client.session_transaction() as sess:
        sess['cart'] = cart_items
