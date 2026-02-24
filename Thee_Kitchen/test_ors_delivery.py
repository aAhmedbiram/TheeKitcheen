#!/usr/bin/env python3
"""
Test script for OpenRouteService delivery pricing
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from delivery_service import delivery_service

def test_ors_delivery():
    """Test OpenRouteService delivery with Cairo coordinates"""
    print("🧪 Testing OpenRouteService Delivery API")
    print("=" * 50)
    
    # Test with Cairo coordinates
    cairo_lat, cairo_lng = 30.0444, 31.2357
    
    print(f"Testing coordinates: {cairo_lat}, {cairo_lng}")
    print("Calling OpenRouteService API...")
    
    result = delivery_service.quote_delivery(cairo_lat, cairo_lng)
    
    if result['ok']:
        print(f"✅ OpenRouteService API test PASSED")
        print(f"   Distance: {result['distance_km']} km")
        print(f"   Delivery Fee: {result['delivery_fee']} EGP")
        print(f"   Out of range: {result['out_of_range']}")
        
        # Verify pricing rules
        if result['out_of_range']:
            print("   📍 Location is out of delivery range")
        elif result['delivery_fee'] == 50:
            print("   📍 Location is in near delivery range (≤25km)")
        elif result['delivery_fee'] == 80:
            print("   📍 Location is in far delivery range (>25km, ≤70km)")
        
        return True
    else:
        print(f"❌ OpenRouteService API test FAILED: {result.get('error', 'Unknown error')}")
        return False

def test_boundary_logic():
    """Test boundary conditions"""
    print("\n🧪 Testing Boundary Logic")
    print("=" * 50)
    
    test_cases = [
        (25.0, 50, False, "Exactly at near threshold"),
        (25.01, 80, False, "Just over near threshold"),
        (70.0, 80, False, "Exactly at max threshold"),
        (70.01, 0, True, "Just over max threshold"),
    ]
    
    all_passed = True
    
    for distance_km, expected_fee, expected_out_of_range, description in test_cases:
        result = delivery_service._apply_delivery_rules(distance_km)
        
        actual_fee = result['delivery_fee']
        actual_out_of_range = result['out_of_range']
        
        fee_passed = actual_fee == expected_fee
        range_passed = actual_out_of_range == expected_out_of_range
        test_passed = fee_passed and range_passed
        
        status = "✅ PASS" if test_passed else "❌ FAIL"
        
        print(f"{status} - {description}")
        print(f"   Distance: {distance_km} km")
        print(f"   Expected: Fee={expected_fee}, Out_of_range={expected_out_of_range}")
        print(f"   Actual:   Fee={actual_fee}, Out_of_range={actual_out_of_range}")
        
        if not test_passed:
            all_passed = False
    
    return all_passed

if __name__ == "__main__":
    print("🚀 Thee Kitchen OpenRouteService Test Suite")
    print("Testing delivery pricing with OpenRouteService...")
    
    # Run tests
    boundary_passed = test_boundary_logic()
    ors_passed = test_ors_delivery()
    
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    print(f"Boundary Logic:     {'✅ PASS' if boundary_passed else '❌ FAIL'}")
    print(f"ORS API:           {'✅ PASS' if ors_passed else '❌ FAIL'}")
    
    if boundary_passed and ors_passed:
        print("\n🎉 OpenRouteService delivery system is working correctly!")
    else:
        print("\n❌ Some tests failed!")
