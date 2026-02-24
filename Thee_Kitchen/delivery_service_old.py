import requests
import time
import math
from typing import Dict, Any, Optional, Tuple
from config import Config
from flask import current_app


class DeliveryService:
    """Delivery pricing service using Google Distance Matrix API"""
    
    def __init__(self):
        self.api_key = Config.GOOGLE_MAPS_API_KEY
        self.hubs = Config.DELIVERY_HUBS
        self.fee_near = Config.DELIVERY_FEE_NEAR
        self.fee_far = Config.DELIVERY_FEE_FAR
        self.threshold_near_km = Config.DELIVERY_THRESHOLD_NEAR_KM
        self.max_km = Config.DELIVERY_MAX_KM
        self.cache = {}
        self.cache_ttl = 600  # 10 minutes
        
    def _get_cache_key(self, lat: float, lng: float) -> Tuple[int, int]:
        """Generate cache key with rounded coordinates"""
        return (round(lat, 5), round(lng, 5))
    
    def _is_cache_valid(self, timestamp: float) -> bool:
        """Check if cache entry is still valid"""
        return time.time() - timestamp < self.cache_ttl
    
    def _call_google_distance_matrix(self, origin_lat: float, origin_lng: float, 
                                 dest_lat: float, dest_lng: float) -> Optional[float]:
        """Call Google Distance Matrix API to get driving distance"""
        if not self.api_key:
            try:
                current_app.logger.error("Google Maps API key not configured")
            except RuntimeError:
                print("Google Maps API key not configured")
            return None
        
        url = "https://maps.googleapis.com/maps/api/distancematrix/json"
        params = {
            'origins': f"{origin_lat},{origin_lng}",
            'destinations': f"{dest_lat},{dest_lng}",
            'mode': 'driving',
            'units': 'metric',
            'key': self.api_key
        }
        
        try:
            response = requests.get(url, params=params, timeout=8)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('status') != 'OK':
                try:
                    current_app.logger.error(f"Google Distance Matrix API error: {data.get('status')}")
                except RuntimeError:
                    print(f"Google Distance Matrix API error: {data.get('status')}")
                return None
                
            elements = data.get('rows', [{}])[0].get('elements', [])
            if not elements:
                try:
                    current_app.logger.error("No elements in Google Distance Matrix response")
                except RuntimeError:
                    print("No elements in Google Distance Matrix response")
                return None
                
            element = elements[0]
            if element.get('status') != 'OK':
                try:
                    current_app.logger.error(f"Google Distance Matrix element error: {element.get('status')}")
                except RuntimeError:
                    print(f"Google Distance Matrix element error: {element.get('status')}")
                return None
                
            distance_meters = element.get('distance', {}).get('value')
            if distance_meters is None:
                try:
                    current_app.logger.error("No distance value in Google Distance Matrix response")
                except RuntimeError:
                    print("No distance value in Google Distance Matrix response")
                return None
                
            return distance_meters / 1000.0  # Convert to kilometers
            
        except requests.exceptions.Timeout:
            try:
                current_app.logger.error("Google Distance Matrix API timeout")
            except RuntimeError:
                print("Google Distance Matrix API timeout")
            return None
        except requests.exceptions.RequestException as e:
            try:
                current_app.logger.error(f"Google Distance Matrix API request error: {e}")
            except RuntimeError:
                print(f"Google Distance Matrix API request error: {e}")
            return None
        except (KeyError, ValueError, TypeError) as e:
            try:
                current_app.logger.error(f"Google Distance Matrix API parsing error: {e}")
            except RuntimeError:
                print(f"Google Distance Matrix API parsing error: {e}")
            return None
    
    def _get_distance_from_hubs(self, lat: float, lng: float) -> Optional[float]:
        """Get minimum driving distance from all hubs"""
        min_distance = None
        
        for hub in self.hubs:
            # Check cache first
            cache_key = self._get_cache_key(lat, lng)
            hub_cache_key = self._get_cache_key(hub['lat'], hub['lng'])
            
            # Try to get from cache
            cache_entry = self.cache.get((cache_key, hub_cache_key))
            if cache_entry and self._is_cache_valid(cache_entry['timestamp']):
                distance = cache_entry['distance']
            else:
                # Call API with retry
                distance = None
                for attempt in range(2):  # Try twice
                    distance = self._call_google_distance_matrix(
                        hub['lat'], hub['lng'], lat, lng
                    )
                    if distance is not None:
                        break
                    if attempt == 0:
                        time.sleep(1)  # Wait 1 second before retry
                
                # Cache the result
                if distance is not None:
                    self.cache[(cache_key, hub_cache_key)] = {
                        'distance': distance,
                        'timestamp': time.time()
                    }
            
            if distance is not None:
                if min_distance is None or distance < min_distance:
                    min_distance = distance
        
        return min_distance
    
    def quote_delivery(self, lat: float, lng: float) -> Dict[str, Any]:
        """
        Calculate delivery quote based on nearest hub distance
        
        Args:
            lat: Customer latitude
            lng: Customer longitude
            
        Returns:
            Dict with keys: ok, out_of_range, delivery_fee, distance_km
        """
        try:
            # Validate coordinates
            if not isinstance(lat, (int, float)) or not isinstance(lng, (int, float)):
                return {'ok': False, 'error': 'Invalid coordinates'}
            
            if not (-90 <= lat <= 90) or not (-180 <= lng <= 180):
                return {'ok': False, 'error': 'Invalid coordinates range'}
            
            # Get minimum distance from hubs
            distance_km = self._get_distance_from_hubs(lat, lng)
            
            if distance_km is None:
                return {'ok': False, 'error': 'Unable to calculate distance'}
            
            # Apply delivery rules
            if distance_km <= self.threshold_near_km:
                delivery_fee = self.fee_near
                out_of_range = False
            elif distance_km <= self.max_km:
                delivery_fee = self.fee_far
                out_of_range = False
            else:
                delivery_fee = 0
                out_of_range = True
            
            return {
                'ok': True,
                'out_of_range': out_of_range,
                'delivery_fee': delivery_fee,
                'distance_km': round(distance_km, 2)
            }
            
        except Exception as e:
            # Handle logging outside of Flask context
            try:
                current_app.logger.error(f"Delivery calculation error: {e}")
            except RuntimeError:
                # Outside application context, use print for debugging
                print(f"Delivery calculation error: {e}")
            return {'ok': False, 'error': f'Delivery calculation failed: {str(e)}'}
    
    def test_boundary_logic(self):
        """Test boundary conditions for delivery pricing"""
        test_cases = [
            (25.0, self.fee_near, False),    # Exactly at near threshold
            (25.01, self.fee_far, False),    # Just over near threshold
            (70.0, self.fee_far, False),    # Exactly at max threshold
            (70.01, 0, True),              # Just over max threshold
        ]
        
        results = []
        for distance, expected_fee, expected_out_of_range in test_cases:
            # Mock the distance calculation
            result = self._apply_delivery_rules(distance)
            results.append({
                'distance_km': distance,
                'expected_fee': expected_fee,
                'expected_out_of_range': expected_out_of_range,
                'actual_fee': result['delivery_fee'],
                'actual_out_of_range': result['out_of_range'],
                'passed': (
                    result['delivery_fee'] == expected_fee and
                    result['out_of_range'] == expected_out_of_range
                )
            })
        
        return results
    
    def _apply_delivery_rules(self, distance_km: float) -> Dict[str, Any]:
        """Apply delivery pricing rules to a given distance"""
        if distance_km <= self.threshold_near_km:
            delivery_fee = self.fee_near
            out_of_range = False
        elif distance_km <= self.max_km:
            delivery_fee = self.fee_far
            out_of_range = False
        else:
            delivery_fee = 0
            out_of_range = True
        
        return {
            'delivery_fee': delivery_fee,
            'out_of_range': out_of_range,
            'distance_km': distance_km
        }


# Global instance
delivery_service = DeliveryService()


def quote_delivery(lat: float, lng: float) -> Dict[str, Any]:
    """
    Convenience function for delivery quoting
    
    Args:
        lat: Customer latitude
        lng: Customer longitude
        
    Returns:
        Dict with delivery quote information
    """
    return delivery_service.quote_delivery(lat, lng)
