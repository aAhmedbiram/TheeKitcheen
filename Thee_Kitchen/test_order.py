#!/usr/bin/env python3
"""
Test script for order placement functionality
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app import app
from extensions import db
from models import Order, OrderItem

def test_order_placement():
    """Test the complete order placement flow"""
    
    with app.app_context():
        try:
            print("=== Testing Order Placement Flow ===")
            
            # Simulate a cart with items
            cart = [
                {'id': 1, 'name': 'Test Item 1', 'price': 50.0, 'quantity': 2},
                {'id': 2, 'name': 'Test Item 2', 'price': 30.0, 'quantity': 1}
            ]
            
            # Simulate JSON data from frontend
            json_data = {
                'customer': {
                    'name': 'Test Customer',
                    'phone': '01234567890',
                    'address': 'Test Address 123',
                    'lat': '30.0',
                    'lng': '31.0',
                    'notes': 'Test order notes'
                }
            }
            
            # Create order with the same logic as place_order
            from delivery_service import quote_delivery
            
            delivery_result = quote_delivery(30.0, 31.0)
            if not delivery_result['ok']:
                print('❌ Delivery quote failed')
                return False
            
            subtotal = sum(item['price'] * item['quantity'] for item in cart)
            delivery_fee = delivery_result['delivery_fee']
            total = subtotal + delivery_fee
            deposit_amount = round(total * 0.20, 2)
            
            # Create order
            order = Order(
                user_id=None,  # Guest order
                status='pending',
                subtotal=subtotal,
                delivery_fee=delivery_fee,
                distance_km=delivery_result['distance_km'],
                total=total,
                deposit_amount=deposit_amount,
                address_text=json_data['customer']['address'],
                customer_lat=float(json_data['customer']['lat']),
                customer_lng=float(json_data['customer']['lng']),
                customer_name=json_data['customer']['name'],
                customer_phone=json_data['customer']['phone']
            )
            
            db.session.add(order)
            db.session.flush()
            
            # Create order items
            for cart_item in cart:
                order_item = OrderItem(
                    order_id=order.id,
                    menu_item_id=cart_item.get('id'),
                    item_name=cart_item['name'],
                    unit_price=cart_item['price'],
                    quantity=cart_item['quantity'],
                    line_total=cart_item['price'] * cart_item['quantity']
                )
                db.session.add(order_item)
            
            db.session.commit()
            
            print('✅ Test order created successfully!')
            print('Order ID:', order.id)
            print('Customer:', order.customer_name)
            print('Total:', order.total, 'EGP')
            print('Delivery Fee:', order.delivery_fee, 'EGP')
            print('Distance:', order.distance_km, 'km')
            print('Items:', len(order.items))
            
            return True
            
        except Exception as e:
            print('❌ Error:', e)
            db.session.rollback()
            return False

if __name__ == "__main__":
    success = test_order_placement()
    if success:
        print('\n🎉 Order placement test PASSED!')
    else:
        print('\n❌ Order placement test FAILED!')
