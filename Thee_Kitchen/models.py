from extensions import db
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)  # Changed from username to name
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20))  # Added phone field
    is_admin = db.Column(db.Boolean, default=False)  # Changed from is_verified to is_admin
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.name}>'


class MenuItem(db.Model):
    __tablename__ = 'menu_items'
    
    id = db.Column(db.Integer, primary_key=True)
    name_ar = db.Column(db.String(100), nullable=False)
    name_en = db.Column(db.String(100), nullable=False)
    description_ar = db.Column(db.Text, nullable=False)
    description_en = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    is_available = db.Column(db.Boolean, default=True)
    image_urls = db.Column(db.String(255), default='')
    category = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    def get_name(self, lang='ar'):
        return self.name_ar if lang == 'ar' else self.name_en
    
    def get_description(self, lang='ar'):
        return self.description_ar if lang == 'ar' else self.description_en
    
    def get_display_image(self):
        # Return actual image URL if available, otherwise use emoji fallback
        if self.image_urls and self.image_urls.strip():
            return self.image_urls
        else:
            # Use food emojis as fallback images
            category_emojis = {
                'main': '🍗',
                'side': '🍚', 
                'dessert': '🍰',
                'appetizer': '🥟'
            }
            return category_emojis.get(self.category, '🍽️')
    
    def __repr__(self):
        return f'<MenuItem {self.name_ar}>'


class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # Allow nullable for guest orders
    status = db.Column(db.String(50), default='pending')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)
    delivery_fee = db.Column(db.Numeric(10, 2), nullable=False)
    distance_km = db.Column(db.Numeric(10, 2), nullable=False)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    deposit_amount = db.Column(db.Numeric(10, 2), nullable=False)
    address_text = db.Column(db.Text, nullable=False)
    customer_lat = db.Column(db.Float, nullable=False)
    customer_lng = db.Column(db.Float, nullable=False)
    customer_name = db.Column(db.String(80), nullable=False)  # Customer name for guest orders
    customer_phone = db.Column(db.String(20), nullable=False)  # Customer phone for guest orders
    
    # Relationship
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Order {self.id}>'


class OrderItem(db.Model):
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_items.id'), nullable=True)
    item_name = db.Column(db.String(200), nullable=False)  # Snapshot of item name
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)  # Snapshot of price
    quantity = db.Column(db.Integer, nullable=False)
    line_total = db.Column(db.Numeric(10, 2), nullable=False)
    
    def __repr__(self):
        return f'<OrderItem {self.item_name}>'
