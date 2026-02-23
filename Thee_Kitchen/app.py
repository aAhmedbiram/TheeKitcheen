from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, current_app
from extensions import db
from models import User, MenuItem, Order, OrderItem
from translations import translations
from datetime import datetime
from delivery_service import quote_delivery
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Startup verification - check database configuration
if not app.config.get('TESTING', False):
    if not app.config.get('SQLALCHEMY_DATABASE_URI'):
        print("=" * 60)
        print("❌ DATABASE_URL not configured!")
        print("")
        print("To fix this issue:")
        print("1. Create a .env file in the project root")
        print("2. Add your Neon PostgreSQL connection string:")
        print("   DATABASE_URL=postgresql://USER:PASSWORD@HOST/DB?sslmode=require")
        print("3. Install python-dotenv: pip install python-dotenv")
        print("")
        print("See .env.example for a template.")
        print("=" * 60)
        raise RuntimeError("DATABASE_URL not configured. See .env.example for setup instructions.")

db.init_app(app)

# Database diagnostics - run once at startup
def _get_database_fingerprint():
    """Get safe database connection information"""
    try:
        with app.app_context():
            # Get database info (safe queries only)
            result = db.session.execute(db.text("""
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
            
            # Store in app config for later access
            app.config['DB_FINGERPRINT'] = result_dict
            
            # Log safe connection info
            print(f"🔗 Connected DB: {result_dict['database']} user:{result_dict['user']} server:{result_dict['server_ip']}")
            
    except Exception as e:
        # Fallback info if queries fail
        app.config['DB_FINGERPRINT'] = {
            'database': 'Unknown',
            'user': 'Unknown',
            'server_ip': 'Unknown',
            'version': 'Unknown',
            'error': str(e)
        }
        print(f"⚠️ Database connection info unavailable: {e}")

# Run diagnostics at startup
_get_database_fingerprint()

# Print runtime banner
print(f"🚀 Thee Kitchen Starting Up")
print(f"📊 ENV={app.config['ENV']} DB={app.config['SANITIZED_DB_URI']}")

# Create database tables if they don't exist
with app.app_context():
    db.create_all()


@app.context_processor
def inject_globals():
    current_lang = session.get('lang', 'ar')
    return dict(
        t=translations.get(current_lang, translations['ar']),
        current_lang=current_lang,
        is_rtl=current_lang == 'ar',
        current_user=session.get('user_name'),
        is_logged_in='user_id' in session,
        is_admin=session.get('is_admin', False)
    )


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/menu')
def menu():
    from models import MenuItem  # Import here to avoid circular import
    from extensions import db
    
    current_lang = session.get('lang', 'ar')
    category_filter = request.args.get('category', 'all')
    
    # Create sample items if database is empty
    if MenuItem.query.first() is None:
        with app.app_context():
            sample_items = [
                MenuItem(
                    name_ar="كبسة الدجاج",
                    name_en="Chicken Kabsa",
                    description_ar="طبق تقليدي شهير من الدجاج مع الأرز البسمتي والتوابل العربية",
                    description_en="Traditional famous dish of chicken with basmati rice and Arabic spices",
                    price=120.0,
                    category="main"
                ),
                MenuItem(
                    name_ar="مندي لحم",
                    name_en="Mandi Lamb",
                    description_ar="لحم ضأن مطهو ببطء على الفحم مع أرز معطر",
                    description_en="Slow-cooked lamb on charcoal with fragrant rice",
                    price=150.0,
                    category="main"
                ),
                MenuItem(
                    name_ar="سمبوسك خضار",
                    name_en="Vegetable Samosa",
                    description_ar="معجنات مقرمشة محشوة بالخضار المتبلة",
                    description_en="Crispy pastries filled with seasoned vegetables",
                    price=25.0,
                    category="side"
                ),
                MenuItem(
                    name_ar="سلطة عربية",
                    name_en="Arabic Salad",
                    description_ar="سلطة طازجة بالخضار الموسمية وتوابل السماق",
                    description_en="Fresh salad with seasonal vegetables and sumac spices",
                    price=30.0,
                    category="side"
                ),
                MenuItem(
                    name_ar="أم علي",
                    name_en="Um Ali",
                    description_ar="حلوى مصرية تقليدية بالكريم والتمر والمكسرات",
                    description_en="Traditional Egyptian dessert with cream, dates and nuts",
                    price=35.0,
                    category="dessert"
                ),
                MenuItem(
                    name_ar="كنافة بالجبن",
                    name_en="Kunafa with Cheese",
                    description_ar="كنافة مقرمشة بالجبن والشرق الحلو",
                    description_en="Crispy kunafa with cheese and sweet syrup",
                    price=40.0,
                    category="dessert"
                )
            ]
            
            for item in sample_items:
                db.session.add(item)
            db.session.commit()
    
    # Get all available items
    items_query = MenuItem.query.filter_by(is_available=True)
    
    # Filter by category if specified
    if category_filter != 'all':
        items_query = items_query.filter_by(category=category_filter)
    
    menu_items = items_query.all()
    
    # Check if any items exist for empty state handling
    has_items = len(menu_items) > 0
    
    # Group items by category and build proper structure for template
    categories = {}
    for item in menu_items:
        if item.category not in categories:
            categories[item.category] = {'items': []}
        categories[item.category]['items'].append(item)
    
    # Define category names for template iteration
    category_names = {
        'main': {'name_ar': 'الأطباق الرئيسية', 'name_en': 'Main Dishes'},
        'side': {'name_ar': 'الأطباق الجانبية', 'name_en': 'Side Dishes'}, 
        'dessert': {'name_ar': 'الحلويات', 'name_en': 'Desserts'}
    }
    
    return render_template('menu.html', 
                         categories=categories,
                         category_names=category_names,
                         current_category=category_filter,
                         current_lang=current_lang,
                         has_items=has_items)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        from models import User  # Import here to avoid circular import
        
        username = request.form.get('username')  # Changed from email to username to match form field
        password = request.form.get('password')
        
        if not username or not password:
            flash('❌ Please enter both username and password', 'error')
            return render_template('login.html')
        
        # Find user by username (or email if you prefer)
        user = User.query.filter_by(name=username).first()  # Changed from email to username
        
        # Check if user exists and password is correct
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['user_name'] = user.name
            session['is_admin'] = user.is_admin
            flash(f'✅ Welcome back, {user.name}!', 'success')
            
            # Check if user came from checkout
            next_page = request.form.get('next') or request.args.get('next')
            if next_page and next_page == url_for('checkout'):
                return redirect(url_for('checkout'))
            return redirect(url_for('home'))
        else:
            flash('❌ Invalid username or password', 'error')
    
    # Store the next page for redirect after login
    next_page = request.args.get('next')
    return render_template('login.html', next_page=next_page)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        from models import User  # Import here to avoid circular import
        
        name = request.form.get('username')  # Changed from 'name' to 'username' to match form field
        email = request.form.get('email')
        password = request.form.get('password')
        phone = request.form.get('phone', '')  # Get phone from form
        
        # Validation
        if not name or not email or not password:
            flash('❌ Please fill in all required fields', 'error')
            return render_template('signup.html')
        
        # Skip password confirmation check since form doesn't have confirm field
        # if password != confirm_password:
        #     flash('❌ Passwords do not match', 'error')
        #     return render_template('signup.html')
        
        if len(password) < 6:
            flash('❌ Password must be at least 6 characters long', 'error')
            return render_template('signup.html')
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('❌ An account with this email already exists', 'error')
            return render_template('signup.html')
        
        # Create new user
        new_user = User(
            name=name,
            email=email,
            phone=phone,  # Use phone from form
            is_admin=False
        )
        new_user.set_password(password)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('✅ Account created successfully! Please login.', 'success')
            
            # Check if user came from checkout
            next_page = request.form.get('next') or request.args.get('next')
            if next_page and next_page == url_for('checkout'):
                return redirect(url_for('login', next=url_for('checkout')))
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('❌ Error creating account. Please try again.', 'error')
            return render_template('signup.html')
    
    # Store the next page for redirect after signup/login
    next_page = request.args.get('next')
    return render_template('signup.html', next_page=next_page)


@app.route('/change-password', methods=['GET', 'POST'])
def change_password():
    if request.method == 'POST':
        # TODO: change password logic
        flash("✅ Password changed (demo).", "success")
        return redirect(url_for('home'))
    return render_template('changePassword.html')


@app.route('/logout')
def logout():
    user_name = session.get('user_name', 'User')
    session.clear()
    flash(f'✅ Goodbye, {user_name}!', 'success')
    return redirect(url_for('home'))


@app.route('/toggle-language')
def toggle_language():
    session['lang'] = 'en' if session.get('lang', 'ar') == 'ar' else 'ar'
    return redirect(request.referrer or url_for('home'))


@app.route('/resend-verification')
def resend_verification():
    flash("📩 Verification email resent (demo).", "success")
    return redirect(url_for('login'))


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    from models import MenuItem
    
    item_id = request.json.get('item_id')
    quantity = request.json.get('quantity', 1)
    
    if not item_id:
        return {'success': False, 'message': 'Item ID is required'}
    
    item = db.session.get(MenuItem, item_id)
    if not item or not item.is_available:
        return {'success': False, 'message': 'Item not found or not available'}
    
    # Get current cart from session or create new one
    cart = session.get('cart', [])
    
    # Check if item already in cart
    existing_item_index = None
    for i, cart_item in enumerate(cart):
        if cart_item['id'] == item_id:
            existing_item_index = i
            break
    
    if existing_item_index is not None:
        # Update quantity of existing item
        cart[existing_item_index]['quantity'] += quantity
    else:
        # Add new item to cart
        cart.append({
            'id': item.id,
            'name': item.get_name(session.get('lang', 'ar')),
            'price': item.price,
            'quantity': quantity
        })
    
    # Save cart back to session
    session['cart'] = cart
    
    return {
        'success': True, 
        'message': 'Item added to cart',
        'cart_count': sum(item['quantity'] for item in cart)
    }


@app.route('/get_cart')
def get_cart():
    cart = session.get('cart', [])
    cart_count = sum(item['quantity'] for item in cart)
    
    return {
        'success': True,
        'cart': cart,
        'cart_count': cart_count
    }


@app.route('/update_cart', methods=['POST'])
def update_cart():
    item_id = request.json.get('item_id')
    change = request.json.get('change', 0)
    
    if not item_id:
        return {'success': False, 'message': 'Item ID is required'}
    
    cart = session.get('cart', [])
    
    # Find and update item
    for i, cart_item in enumerate(cart):
        if cart_item['id'] == item_id:
            cart[i]['quantity'] += change
            if cart[i]['quantity'] <= 0:
                cart.pop(i)
            break
    
    session['cart'] = cart
    cart_count = sum(item['quantity'] for item in cart)
    
    return {
        'success': True,
        'cart': cart,
        'cart_count': cart_count
    }


@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    item_id = request.json.get('item_id')
    
    if not item_id:
        return {'success': False, 'message': 'Item ID is required'}
    
    cart = session.get('cart', [])
    cart = [item for item in cart if item['id'] != item_id]
    
    session['cart'] = cart
    cart_count = sum(item['quantity'] for item in cart)
    
    return {
        'success': True,
        'cart': cart,
        'cart_count': cart_count
    }


@app.route('/clear_cart')
def clear_cart():
    session['cart'] = []
    return {'success': True, 'message': 'Cart cleared'}


@app.route('/api/delivery/quote', methods=['POST'])
def delivery_quote():
    """API endpoint for delivery quote"""
    try:
        # Get coordinates from form data or JSON
        if request.form:
            lat = request.form.get('lat')
            lng = request.form.get('lng')
        else:
            data = request.get_json()
            lat = data.get('lat') if data else None
            lng = data.get('lng') if data else None
        
        if not lat or not lng:
            return jsonify({
                'ok': False,
                'error': translations.get(session.get('lang', 'ar'), {}).get('delivery_required', 'Coordinates are required')
            })
        
        result = quote_delivery(lat, lng)
        
        if not result['ok']:
            return jsonify(result)
        
        if result.get('out_of_range'):
            return jsonify({
                'ok': True,
                'out_of_range': True,
                'distance_km': result['distance_km'],
                'message': translations.get(session.get('lang', 'ar'), {}).get('out_of_delivery_range', 'Out of delivery range')
            })
        
        return jsonify({
            'ok': True,
            'out_of_range': False,
            'delivery_fee': result['delivery_fee'],
            'distance_km': result['distance_km']
        })
        
    except Exception as e:
        current_app.logger.error(f"Delivery quote error: {e}")
        return jsonify({
            'ok': False,
            'error': translations.get(session.get('lang', 'ar'), {}).get('delivery_try_again', 'Please try again')
        })


@app.route('/checkout')
def checkout():
    """Display checkout page - allow both logged-in and guest users"""
    # Get cart from session
    cart = session.get('cart', [])
    
    if not cart:
        return redirect(url_for('menu'))
    
    # Calculate totals
    subtotal = sum(item['price'] * item['quantity'] for item in cart)
    
    # Check if user is logged in
    is_logged_in = 'user_id' in session
    user_info = None
    if is_logged_in:
        # Get user information for pre-filling
        user_id = session['user_id']
        user = db.session.get(User, user_id)
        if user:
            user_info = {
                'name': user.name,
                'phone': user.phone
            }
    
    return render_template('checkout.html', 
                     cart=cart,
                     subtotal=subtotal,
                     is_logged_in=is_logged_in,
                     user_info=user_info,
                     current_lang=session.get('lang', 'ar'))


@app.route('/place_order', methods=['POST'])
def place_order():
    """Handle order placement with JSON data and database persistence"""
    try:
        # Get cart from session
        cart = session.get('cart', [])
        if not cart:
            flash(translations.get(session.get('lang', 'ar'), {}).get('empty_cart_checkout', 'Your cart is empty'), 'error')
            return redirect(url_for('checkout'))
        
        # Handle both JSON and form data
        if request.is_json:
            # Handle JSON data from fetch
            data = request.get_json()
            address_text = data.get('customer', {}).get('address', '')
            customer_lat = data.get('customer', {}).get('lat', '')
            customer_lng = data.get('customer', {}).get('lng', '')
            customer_name = data.get('customer', {}).get('name', '')
            customer_phone = data.get('customer', {}).get('phone', '')
        else:
            # Handle traditional form data
            address_text = request.form.get('address_text')
            customer_lat = request.form.get('lat')
            customer_lng = request.form.get('lng')
            customer_name = request.form.get('name')
            customer_phone = request.form.get('phone')
        
        # Validate required fields
        if not address_text or not customer_lat or not customer_lng or not customer_name or not customer_phone:
            flash(translations.get(session.get('lang', 'ar'), {}).get('delivery_required', 'All fields are required'), 'error')
            return redirect(url_for('checkout'))
        
        # Parse coordinates
        try:
            customer_lat = float(customer_lat)
            customer_lng = float(customer_lng)
        except (ValueError, TypeError):
            flash(translations.get(session.get('lang', 'ar'), {}).get('delivery_required', 'Invalid delivery address'), 'error')
            return redirect(url_for('checkout'))
        
        # Get delivery quote server-side (never trust client)
        delivery_result = quote_delivery(customer_lat, customer_lng)
        
        if not delivery_result['ok']:
            flash(translations.get(session.get('lang', 'ar'), {}).get('delivery_try_again', 'Unable to calculate delivery. Please try again.'), 'error')
            return redirect(url_for('checkout'))
        
        if delivery_result.get('out_of_range'):
            flash(translations.get(session.get('lang', 'ar'), {}).get('out_of_delivery_range', 'Your address is out of our delivery range'), 'error')
            return redirect(url_for('checkout'))
        
        # Calculate totals
        subtotal = sum(item['price'] * item['quantity'] for item in cart)
        delivery_fee = delivery_result['delivery_fee']
        total = subtotal + delivery_fee
        deposit_amount = round(total * 0.20, 2)  # 20% deposit
        
        # Check if user is logged in
        is_logged_in = 'user_id' in session
        user_id = session['user_id'] if is_logged_in else None
        
        # Create order
        order = Order(
            user_id=user_id,
            status='pending',
            subtotal=subtotal,
            delivery_fee=delivery_fee,
            distance_km=delivery_result['distance_km'],
            total=total,
            deposit_amount=deposit_amount,
            address_text=address_text,
            customer_lat=customer_lat,
            customer_lng=customer_lng,
            customer_name=customer_name,  # Store customer name for guest orders
            customer_phone=customer_phone   # Store customer phone for guest orders
        )
        
        db.session.add(order)
        db.session.flush()  # Get order ID without committing
        
        # Create order items
        for cart_item in cart:
            order_item = OrderItem(
                order_id=order.id,
                menu_item_id=cart_item.get('id'),  # May be None if item deleted
                item_name=cart_item['name'],
                unit_price=cart_item['price'],
                quantity=cart_item['quantity'],
                line_total=cart_item['price'] * cart_item['quantity']
            )
            db.session.add(order_item)
        
        # Commit everything
        db.session.commit()
        
        # Clear cart
        session['cart'] = []
        
        # Return appropriate response
        if request.is_json:
            return jsonify({
                'success': True,
                'message': 'Order created successfully!',
                'order_id': order.id
            })
        else:
            # Flash success message and redirect for traditional form submission
            flash(translations.get(session.get('lang', 'ar'), {}).get('order_created_success', 'Order created successfully!'), 'success')
            return redirect(url_for('home'))
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Place order error: {e}")
        
        # Return appropriate error response
        if request.is_json:
            return jsonify({
                'success': False,
                'message': translations.get(session.get('lang', 'ar'), {}).get('order_error', 'Error creating order. Please try again.')
            })
        else:
            flash(translations.get(session.get('lang', 'ar'), {}).get('order_error', 'Error creating order. Please try again.'), 'error')
            return redirect(url_for('checkout'))


@app.route('/admin/db-info')
def admin_db_info():
    """Admin-only database information endpoint"""
    # Check if user is admin
    if not session.get('is_admin'):
        return jsonify({'error': 'Admin access required'}), 403
    
    try:
        # Get database fingerprint from app config
        db_info = app.config.get('DB_FINGERPRINT', {})
        
        # Add sanitized database URI
        response_data = {
            'database': db_info.get('database', 'Unknown'),
            'user': db_info.get('user', 'Unknown'),
            'server_ip': db_info.get('server_ip', 'Unknown'),
            'uri': app.config.get('SANITIZED_DB_URI', 'Unknown')
        }
        
        # Add version if available
        if 'version' in db_info:
            response_data['version'] = db_info['version']
        
        # Add error if present
        if 'error' in db_info:
            response_data['error'] = db_info['error']
        
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
