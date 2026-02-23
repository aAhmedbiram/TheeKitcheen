import time
import requests
from typing import Optional, Dict, Any
from flask import current_app
from config import Config

class DeliveryService:
    """Service for calculating delivery fees using OpenRouteService Matrix API"""
    
    def __init__(self):
        self.api_key = Config.ORS_API_KEY
        self.hubs = Config.DELIVERY_HUBS
        self.fee_near = Config.DELIVERY_FEE_NEAR
        self.fee_far = Config.DELIVERY_FEE_FAR
        self.threshold_near_km = Config.DELIVERY_THRESHOLD_NEAR_KM
        self.max_km = Config.DELIVERY_MAX_KM
        self.cache_ttl = 600  # 10 minutes
        self.cache = {}
    
    def _get_cache_key(self, lat: float, lng: float) -> str:
        """Generate cache key for coordinates"""
        return f"{round(lat, 5)},{round(lng, 5)}"
    
    def _is_cache_valid(self, timestamp: float) -> bool:
        """Check if cache entry is still valid"""
        return time.time() - timestamp < self.cache_ttl
    
    def _call_ors_matrix(self, hub_lat: float, hub_lng: float, 
                       dest_lat: float, dest_lng: float) -> Optional[float]:
        """Call OpenRouteService Matrix API to get driving distance"""
        if not self.api_key:
            try:
                current_app.logger.error("OpenRouteService API key not configured")
            except RuntimeError:
                print("OpenRouteService API key not configured")
            return None
        
        url = "https://api.openrouteservice.org/v2/matrix/driving-car"
        headers = {
            'Authorization': self.api_key,
            'Content-Type': 'application/json'
        }
        
        # OpenRouteService expects [lng, lat] order
        payload = {
            "locations": [
                [hub_lng, hub_lat],      # Hub location
                [dest_lng, dest_lat]     # Customer location
            ],
            "sources": [0],
            "destinations": [1],
            "metrics": ["distance"]
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=7)
            response.raise_for_status()
            
            data = response.json()
            
            if 'error' in data:
                try:
                    current_app.logger.error(f"OpenRouteService API error: {data['error']}")
                except RuntimeError:
                    print(f"OpenRouteService API error: {data['error']}")
                return None
                
            distances = data.get('distances', [])
            if not distances or not distances[0]:
                try:
                    current_app.logger.error("No distances in OpenRouteService response")
                except RuntimeError:
                    print("No distances in OpenRouteService response")
                return None
                
            distance_meters = distances[0][0]
            if distance_meters is None:
                try:
                    current_app.logger.error("Null distance in OpenRouteService response")
                except RuntimeError:
                    print("Null distance in OpenRouteService response")
                return None
                
            return distance_meters / 1000.0  # Convert to kilometers
            
        except requests.exceptions.Timeout:
            try:
                current_app.logger.error("OpenRouteService API timeout")
            except RuntimeError:
                print("OpenRouteService API timeout")
            return None
        except requests.exceptions.RequestException as e:
            try:
                current_app.logger.error(f"OpenRouteService API request error: {e}")
            except RuntimeError:
                print(f"OpenRouteService API request error: {e}")
            return None
        except (KeyError, ValueError, TypeError) as e:
            try:
                current_app.logger.error(f"OpenRouteService API parsing error: {e}")
            except RuntimeError:
                print(f"OpenRouteService API parsing error: {e}")
            return None
    
    def _get_distance_from_hubs(self, lat: float, lng: float) -> Optional[float]:
        """Get minimum driving distance from all hubs"""
        min_distance = None
        
        for hub in self.hubs:
            # Check cache first
            cache_key = self._get_cache_key(lat, lng)
            hub_cache_key = self._get_cache_key(hub['lat'], hub['lng'])
            combined_key = f"{hub_cache_key}-{cache_key}"
            
            if combined_key in self.cache:
                timestamp, distance = self.cache[combined_key]
                if self._is_cache_valid(timestamp):
                    if min_distance is None or distance < min_distance:
                        min_distance = distance
                    continue
            
            # Call API with retry
            distance = self._call_ors_matrix_with_retry(hub['lat'], hub['lng'], lat, lng)
            
            if distance is not None:
                # Cache the result
                self.cache[combined_key] = (time.time(), distance)
                
                if min_distance is None or distance < min_distance:
                    min_distance = distance
        
        return min_distance
    
    def _call_ors_matrix_with_retry(self, hub_lat: float, hub_lng: float, 
                                  dest_lat: float, dest_lng: float) -> Optional[float]:
        """Call OpenRouteService Matrix API with retry logic"""
        # First attempt
        result = self._call_ors_matrix(hub_lat, hub_lng, dest_lat, dest_lng)
        if result is not None:
            return result
        
        # Retry once
        try:
            current_app.logger.info("Retrying OpenRouteService API call")
        except RuntimeError:
            print("Retrying OpenRouteService API call")
        
        return self._call_ors_matrix(hub_lat, hub_lng, dest_lat, dest_lng)
    
    def _apply_delivery_rules(self, distance_km: float) -> Dict[str, Any]:
        """Apply delivery pricing rules based on distance"""
        if distance_km > self.max_km:
            return {
                'delivery_fee': 0,
                'out_of_range': True
            }
        elif distance_km <= self.threshold_near_km:
            return {
                'delivery_fee': self.fee_near,
                'out_of_range': False
            }
        else:
            return {
                'delivery_fee': self.fee_far,
                'out_of_range': False
            }
    
    def quote_delivery(self, lat: float, lng: float) -> Dict[str, Any]:
        """Get delivery quote for given coordinates"""
        # Validate coordinates
        if not self._validate_coordinates(lat, lng):
            return {'ok': False, 'error': 'Invalid coordinates'}
        
        try:
            # Get distance from nearest hub
            distance_km = self._get_distance_from_hubs(lat, lng)
            
            if distance_km is None:
                try:
                    current_app.logger.error("Unable to calculate distance")
                except RuntimeError:
                    print("Unable to calculate distance")
                return {'ok': False, 'error': 'Unable to calculate distance'}
            
            # Apply delivery rules
            pricing = self._apply_delivery_rules(distance_km)
            
            return {
                'ok': True,
                'out_of_range': pricing['out_of_range'],
                'delivery_fee': pricing['delivery_fee'],
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
    
    def _validate_coordinates(self, lat: float, lng: float) -> bool:
        """Validate latitude and longitude ranges"""
        if lat is None or lng is None:
            return False
        
        try:
            lat_float = float(lat)
            lng_float = float(lng)
        except (ValueError, TypeError):
            return False
        
        return (-90 <= lat_float <= 90) and (-180 <= lng_float <= 180)

# Global instance
delivery_service = DeliveryService()

def quote_delivery(lat: float, lng: float) -> Dict[str, Any]:
    """Convenience function to get delivery quote"""
    return delivery_service.quote_delivery(lat, lng)
