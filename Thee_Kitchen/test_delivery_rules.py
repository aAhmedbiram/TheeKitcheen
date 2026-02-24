#!/usr/bin/env python3
"""
Simple test to verify delivery service works without API calls
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from delivery_service import delivery_service

def test_delivery_rules_only():
    """Test delivery pricing rules without API calls"""
    print("🧪 Testing Delivery Rules (No API Required)")
    print("=" * 50)
    
    # Test the pricing rules directly
    test_cases = [
        (10.0, 50, False, "Near distance"),
        (25.0, 50, False, "Exactly at near threshold"),
        (30.0, 80, False, "Far distance"),
        (70.0, 80, False, "Exactly at max threshold"),
        (80.0, 0, True, "Out of range"),
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
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All delivery rules tests PASSED!")
        print("✅ Delivery pricing logic is working correctly!")
    else:
        print("❌ Some delivery rules tests FAILED!")
    
    return all_passed

if __name__ == "__main__":
    print("🚀 Thee Kitchen Delivery Rules Test")
    print("Testing delivery pricing rules without API...")
    
    # Test delivery rules
    rules_passed = test_delivery_rules_only()
    
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    print(f"Delivery Rules: {'✅ PASS' if rules_passed else '❌ FAIL'}")
    
    if rules_passed:
        print("\n🎉 Delivery pricing system is ready!")
        print("💡 Add Google Maps API key to enable real distance calculations")
    else:
        print("\n❌ Delivery pricing system has issues!")
