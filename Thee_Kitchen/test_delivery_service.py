#!/usr/bin/env python3
"""
Test script for delivery pricing boundary logic
Tests the exact boundary conditions as specified in requirements
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from delivery_service import delivery_service

def test_delivery_boundary_logic():
    """Test boundary conditions for delivery pricing"""
    print("🧪 Testing Delivery Pricing Boundary Logic")
    print("=" * 50)
    
    # Test cases as specified in requirements
    test_cases = [
        (25.0, 50, False, "Exactly at near threshold"),
        (25.01, 80, False, "Just over near threshold"),
        (70.0, 80, False, "Exactly at max threshold"),
        (70.01, 0, True, "Just over max threshold"),
    ]
    
    all_passed = True
    
    for distance_km, expected_fee, expected_out_of_range, description in test_cases:
        # Test the delivery rules directly
        result = delivery_service._apply_delivery_rules(distance_km)
        
        actual_fee = result['delivery_fee']
        actual_out_of_range = result['out_of_range']
        
        fee_passed = actual_fee == expected_fee
        range_passed = actual_out_of_range == expected_out_of_range
        test_passed = fee_passed and range_passed
        
        status = "✅ PASS" if test_passed else "❌ FAIL"
        
        print(f"\n{status} - {description}")
        print(f"   Distance: {distance_km} km")
        print(f"   Expected: Fee={expected_fee}, Out_of_range={expected_out_of_range}")
        print(f"   Actual:   Fee={actual_fee}, Out_of_range={actual_out_of_range}")
        
        if not test_passed:
            all_passed = False
            if not fee_passed:
                print(f"   ❌ Fee mismatch: expected {expected_fee}, got {actual_fee}")
            if not range_passed:
                print(f"   ❌ Range mismatch: expected {expected_out_of_range}, got {actual_out_of_range}")
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All boundary tests PASSED!")
    else:
        print("❌ Some boundary tests FAILED!")
    
    return all_passed

def test_coordinate_validation():
    """Test coordinate validation"""
    print("\n🧪 Testing Coordinate Validation")
    print("=" * 50)
    
    # Test invalid coordinates
    invalid_coords = [
        (None, 31.2357, "None latitude"),
        (30.0444, None, "None longitude"),
        ("invalid", 31.2357, "String latitude"),
        (30.0444, "invalid", "String longitude"),
        (91.0, 31.2357, "Latitude > 90"),
        (-91.0, 31.2357, "Latitude < -90"),
        (30.0444, 181.0, "Longitude > 180"),
        (30.0444, -181.0, "Longitude < -180"),
    ]
    
    all_passed = True
    
    for lat, lng, description in invalid_coords:
        result = delivery_service.quote_delivery(lat, lng)
        
        if not result['ok']:
            print(f"✅ PASS - {description}: {result.get('error', 'Error')}")
        else:
            print(f"❌ FAIL - {description}: Should have failed but passed")
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All coordinate validation tests PASSED!")
    else:
        print("❌ Some coordinate validation tests FAILED!")
    
    return all_passed

def test_api_integration():
    """Test API integration with real coordinates"""
    print("\n🧪 Testing API Integration (requires Google Maps API key)")
    print("=" * 50)
    
    # Test with Cairo coordinates (should be in range)
    cairo_lat, cairo_lng = 30.0444, 31.2357
    
    result = delivery_service.quote_delivery(cairo_lat, cairo_lng)
    
    if result['ok']:
        print(f"✅ Cairo API test PASSED")
        print(f"   Distance: {result['distance_km']} km")
        print(f"   Delivery Fee: {result['delivery_fee']} EGP")
        print(f"   Out of range: {result['out_of_range']}")
    else:
        print(f"❌ Cairo API test FAILED: {result.get('error', 'Unknown error')}")
        print("   Note: This may fail if Google Maps API key is not configured")
    
    return result['ok']

if __name__ == "__main__":
    print("🚀 Thee Kitchen Delivery Service Test Suite")
    print("Testing delivery pricing implementation...")
    
    # Run all tests
    boundary_passed = test_delivery_boundary_logic()
    validation_passed = test_coordinate_validation()
    api_passed = test_api_integration()
    
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    print(f"Boundary Logic:     {'✅ PASS' if boundary_passed else '❌ FAIL'}")
    print(f"Coordinate Validation: {'✅ PASS' if validation_passed else '❌ FAIL'}")
    print(f"API Integration:     {'✅ PASS' if api_passed else '❌ FAIL'}")
    
    if boundary_passed and validation_passed:
        print("\n🎉 Core functionality is working correctly!")
        if not api_passed:
            print("💡 API test failed - check Google Maps API key configuration")
    else:
        print("\n❌ Critical functionality issues detected!")
