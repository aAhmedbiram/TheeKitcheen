import pytest
import json
from unittest.mock import patch
from flask import session
from models import Order, OrderItem
from conftest import login_user, set_cart_in_session


class TestCheckoutRouting:
    """Test checkout page routing and authentication"""

    def test_checkout_requires_login(self, client):
        """Test GET /checkout redirects to login when not logged in"""
        response = client.get('/checkout', follow_redirects=False)
        
        assert response.status_code == 302
        assert '/login' in response.location

    def test_checkout_shows_cart_when_logged_in(self, logged_in_client, sample_cart_items):
        """Test GET /checkout shows cart when user is logged in"""
        set_cart_in_session(logged_in_client, sample_cart_items)
        
        response = logged_in_client.get('/checkout')
        
        assert response.status_code == 200
        assert b'checkout-container' in response.data
        assert b'Test Item 1' in response.data
        assert b'200.0' in response.data  # subtotal

    def test_checkout_empty_cart_redirects_to_menu(self, logged_in_client):
        """Test GET /checkout with empty cart redirects to menu"""
        set_cart_in_session(logged_in_client, [])
        
        response = logged_in_client.get('/checkout', follow_redirects=False)
        
        assert response.status_code == 302
        assert '/menu' in response.location


class TestOrderPlacement:
    """Test order placement with form data"""

    def test_place_order_blocks_without_location(self, app, logged_in_client, sample_cart_items):
        """Test order placement fails without location data"""
        set_cart_in_session(logged_in_client, sample_cart_items)
        
        response = logged_in_client.post('/place_order', data={
            'name': 'Test User',
            'phone': '01234567890',
            'address_text': 'Test Address',
            # Missing lat/lng
        })
        
        # Should redirect back to checkout with error
        assert response.status_code == 302
        assert '/checkout' in response.location
        
        # Verify no order was created
        with app.app_context():
            order_count = Order.query.count()
            assert order_count == 0

    def test_place_order_blocks_out_of_range(self, app, logged_in_client, sample_cart_items):
        """Test order placement blocked when out of delivery range"""
        set_cart_in_session(logged_in_client, sample_cart_items)
        
        with patch('app.quote_delivery') as mock_quote:
            mock_quote.return_value = {
                'ok': True,
                'out_of_range': True,
                'distance_km': 80.0
            }
            
            response = logged_in_client.post('/place_order', data={
                'name': 'Test User',
                'phone': '01234567890',
                'address_text': 'Test Address',
                'lat': '30.0',
                'lng': '31.0'
            })
            
            # Should redirect back to checkout with error
            assert response.status_code == 302
            assert '/checkout' in response.location
            
            # Verify no order was created
            with app.app_context():
                order_count = Order.query.count()
                assert order_count == 0

    def test_place_order_saves_order_and_items(self, app, logged_in_client, sample_cart_items, sample_user, sample_user_obj):
        """Test successful order creation saves order and items to database"""
        set_cart_in_session(logged_in_client, sample_cart_items)
        login_user(logged_in_client, sample_user, app)
        
        with patch('app.quote_delivery') as mock_quote:
            mock_quote.return_value = {
                'ok': True,
                'out_of_range': False,
                'distance_km': 10.0,
                'delivery_fee': 50
            }
            
            response = logged_in_client.post('/place_order', data={
                'name': 'Test User',
                'phone': '01234567890',
                'address_text': 'Test Address',
                'lat': '30.0',
                'lng': '31.0'
            })
            
            # Should redirect to home with success
            assert response.status_code == 302
            assert '/' in response.location
            
            # Verify order was created
            with app.app_context():
                order = Order.query.first()
                assert order is not None
                assert order.user_id == sample_user
                assert order.status == 'pending'
                assert order.subtotal == 250.0  # 100*2 + 50*1
                assert order.delivery_fee == 50
                assert order.distance_km == 10.0
                assert order.total == 300.0  # 250 + 50
                assert order.deposit_amount == 60.0  # 300 * 0.20
                assert order.address_text == 'Test Address'
                assert order.customer_lat == 30.0
                assert order.customer_lng == 31.0
                
                # Verify order items were created
                order_items = OrderItem.query.filter_by(order_id=order.id).all()
                assert len(order_items) == 2
                
                # Check first item
                item1 = next((i for i in order_items if i.item_name == 'Test Item 1'), None)
                assert item1 is not None
                assert item1.unit_price == 100.0
                assert item1.quantity == 2
                assert item1.line_total == 200.0
                
                # Check second item
                item2 = next((i for i in order_items if i.item_name == 'Test Item 2'), None)
                assert item2 is not None
                assert item2.unit_price == 50.0
                assert item2.quantity == 1
                assert item2.line_total == 50.0

    def test_place_order_clears_cart(self, app, logged_in_client, sample_cart_items):
        """Test successful order clears session cart"""
        set_cart_in_session(logged_in_client, sample_cart_items)
        
        with patch('app.quote_delivery') as mock_quote:
            mock_quote.return_value = {
                'ok': True,
                'out_of_range': False,
                'distance_km': 10.0,
                'delivery_fee': 50
            }
            
            response = logged_in_client.post('/place_order', data={
                'name': 'Test User',
                'phone': '01234567890',
                'address_text': 'Test Address',
                'lat': '30.0',
                'lng': '31.0'
            })
            
            # Cart should be empty after successful order
            with logged_in_client.session_transaction() as sess:
                assert 'cart' not in sess or sess.get('cart') == []

    def test_place_order_requires_login(self, client):
        """Test order placement requires login"""
        response = client.post('/place_order', data={
            'name': 'Test User',
            'phone': '01234567890',
            'address_text': 'Test Address',
            'lat': '30.0',
            'lng': '31.0'
        })
        
        # Should redirect to login
        assert response.status_code == 302
        assert '/login' in response.location

    def test_place_order_empty_cart(self, logged_in_client):
        """Test order placement with empty cart"""
        set_cart_in_session(logged_in_client, [])
        
        response = logged_in_client.post('/place_order', data={
            'name': 'Test User',
            'phone': '01234567890',
            'address_text': 'Test Address',
            'lat': '30.0',
            'lng': '31.0'
        })
        
        # Should redirect back to checkout with error
        assert response.status_code == 302
        assert '/checkout' in response.location


class TestSecurity:
    """Test security aspects of order placement"""

    def test_server_recomputes_fee(self, app, logged_in_client, sample_cart_items):
        """Test server recomputes delivery fee regardless of client tampering"""
        set_cart_in_session(logged_in_client, sample_cart_items)
        
        with patch('app.quote_delivery') as mock_quote:
            mock_quote.return_value = {
                'ok': True,
                'out_of_range': False,
                'distance_km': 40.0,  # Should give 80 EGP fee
                'delivery_fee': 80
            }
            
            # Client tries to tamper by sending fake delivery_fee
            response = logged_in_client.post('/place_order', data={
                'name': 'Test User',
                'phone': '01234567890',
                'address_text': 'Test Address',
                'lat': '30.0',
                'lng': '31.0',
                'delivery_fee': '999999'  # Tampered value
            })
            
            # Order should use server-computed fee (80), not tampered value
            with app.app_context():
                order = Order.query.first()
                assert order is not None
                assert order.delivery_fee == 80  # Server value, not tampered

    def test_server_enforces_out_of_range(self, app, logged_in_client, sample_cart_items):
        """Test server enforces out of range regardless of client tampering"""
        set_cart_in_session(logged_in_client, sample_cart_items)
        
        with patch('app.quote_delivery') as mock_quote:
            mock_quote.return_value = {
                'ok': True,
                'out_of_range': True,  # Out of range
                'distance_km': 80.0
            }
            
            # Client tries to override out_of_range status
            response = logged_in_client.post('/place_order', data={
                'name': 'Test User',
                'phone': '01234567890',
                'address_text': 'Test Address',
                'lat': '30.0',
                'lng': '31.0'
            })
            
            # Should be blocked regardless of client data
            assert response.status_code == 302
            assert '/checkout' in response.location
            
            # Verify no order was created
            with app.app_context():
                order_count = Order.query.count()
                assert order_count == 0


class TestLocalization:
    """Test localization functionality"""

    def test_localization_messages_change(self, logged_in_client, sample_cart_items):
        """Test that changing language changes messages"""
        set_cart_in_session(logged_in_client, sample_cart_items)
        
        # Test Arabic
        with logged_in_client.session_transaction() as sess:
            sess['lang'] = 'ar'
            
        response = logged_in_client.post('/api/delivery/quote', data={
            'lat': '30.0',
            'lng': '31.0'
        })
        
        # Should contain Arabic error message for invalid data
        response = logged_in_client.post('/api/delivery/quote', data={})
        data = json.loads(response.data)
        assert data['ok'] is False
        assert 'error' in data
        
        # Test English
        with logged_in_client.session_transaction() as sess:
            sess['lang'] = 'en'
            
        response = logged_in_client.post('/api/delivery/quote', data={})
        data = json.loads(response.data)
        assert data['ok'] is False
        assert 'error' in data
