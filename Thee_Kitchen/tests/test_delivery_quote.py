import pytest
import json
from unittest.mock import patch, MagicMock
from app import app
from delivery_service import quote_delivery, _distance_cache

class TestDeliveryQuote:
    """Test delivery quote API endpoint and service logic"""

    def test_quote_ok_near_fee(self, client):
        """Test quote with distance <= 25km returns 50 EGP fee"""
        with patch('delivery_service.osrm_distance_km') as mock_distance:
            mock_distance.return_value = 10.0  # 10km distance
            
            response = client.post('/api/delivery/quote', data={
                'lat': '30.0',
                'lng': '31.0'
            })
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['ok'] is True
            assert data['out_of_range'] is False
            assert data['delivery_fee'] == 50
            assert data['distance_km'] == 10.0

    def test_quote_ok_far_fee(self, client):
        """Test quote with distance 40km returns 80 EGP fee"""
        with patch('delivery_service.osrm_distance_km') as mock_distance:
            mock_distance.return_value = 40.0  # 40km distance
            
            response = client.post('/api/delivery/quote', data={
                'lat': '30.0',
                'lng': '31.0'
            })
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['ok'] is True
            assert data['out_of_range'] is False
            assert data['delivery_fee'] == 80
            assert data['distance_km'] == 40.0

    def test_quote_out_of_range(self, client):
        """Test quote with distance > 70km returns out of range"""
        with patch('delivery_service.osrm_distance_km') as mock_distance:
            mock_distance.return_value = 80.0  # 80km distance
            
            response = client.post('/api/delivery/quote', data={
                'lat': '30.0',
                'lng': '31.0'
            })
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['ok'] is True
            assert data['out_of_range'] is True
            assert data['distance_km'] == 80.0
            assert 'delivery_fee' not in data

    def test_quote_invalid_latlng(self, client):
        """Test quote with missing/invalid coordinates returns error"""
        # Test missing coordinates
        response = client.post('/api/delivery/quote', data={})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['ok'] is False
        assert 'error' in data

        # Test invalid coordinates
        response = client.post('/api/delivery/quote', data={
            'lat': 'invalid',
            'lng': '31.0'
        })
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['ok'] is False
        assert 'error' in data

    def test_quote_json_input(self, client):
        """Test quote API accepts JSON input"""
        with patch('delivery_service.osrm_distance_km') as mock_distance:
            mock_distance.return_value = 15.0
            
            response = client.post('/api/delivery/quote', 
                              json={'lat': '30.0', 'lng': '31.0'},
                              content_type='application/json')
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['ok'] is True
            assert data['delivery_fee'] == 50

    def test_osrm_service_error(self, client):
        """Test quote when OSRM service fails"""
        with patch('delivery_service.osrm_distance_km') as mock_distance:
            mock_distance.return_value = None  # Service failure
            
            response = client.post('/api/delivery/quote', data={
                'lat': '30.0',
                'lng': '31.0'
            })
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['ok'] is False
            assert 'error' in data


class TestDeliveryService:
    """Test delivery service logic directly"""

    def test_boundary_25_fee_50(self):
        """Test exact boundary at 25km returns 50 EGP"""
        with patch('delivery_service.osrm_distance_km') as mock_distance:
            mock_distance.return_value = 25.0
            
            result = quote_delivery('30.0', '31.0')
            
            assert result['ok'] is True
            assert result['out_of_range'] is False
            assert result['delivery_fee'] == 50
            assert result['distance_km'] == 25.0

    def test_boundary_25_01_fee_80(self):
        """Test just over 25km boundary returns 80 EGP"""
        with patch('delivery_service.osrm_distance_km') as mock_distance:
            mock_distance.return_value = 25.01
            
            result = quote_delivery('30.0', '31.0')
            
            assert result['ok'] is True
            assert result['out_of_range'] is False
            assert result['delivery_fee'] == 80
            assert result['distance_km'] == 25.01

    def test_boundary_70_fee_80(self):
        """Test exact boundary at 70km returns 80 EGP"""
        with patch('delivery_service.osrm_distance_km') as mock_distance:
            mock_distance.return_value = 70.0
            
            result = quote_delivery('30.0', '31.0')
            
            assert result['ok'] is True
            assert result['out_of_range'] is False
            assert result['delivery_fee'] == 80
            assert result['distance_km'] == 70.0

    def test_boundary_70_01_out_of_range(self):
        """Test just over 70km boundary returns out of range"""
        with patch('delivery_service.osrm_distance_km') as mock_distance:
            mock_distance.return_value = 70.01
            
            result = quote_delivery('30.0', '31.0')
            
            assert result['ok'] is True
            assert result['out_of_range'] is True
            assert result['distance_km'] == 70.01
            assert 'delivery_fee' not in result

    def test_invalid_coordinates(self):
        """Test service with invalid coordinates"""
        result = quote_delivery('', '')
        assert result['ok'] is False
        assert 'error' in result

        result = quote_delivery('invalid', '31.0')
        assert result['ok'] is False
        assert 'error' in result


class TestCaching:
    """Test delivery distance caching functionality"""

    def test_cache_hit_avoids_recompute(self):
        """Test that cache hit avoids OSRM recomputation"""
        with patch('delivery_service.requests.get') as mock_get:
            # Mock successful OSRM response
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'code': 'Ok',
                'routes': [{'distance': 15000}]  # 15km in meters
            }
            mock_get.return_value = mock_response
            
            # Clear cache
            _distance_cache.clear()
            
            # First call should hit OSRM for each hub (2 hubs = 2 calls)
            result1 = quote_delivery('30.0', '31.0')
            assert mock_get.call_count == 2
            
            # Second call with same coordinates should use cache
            result2 = quote_delivery('30.0', '31.0')
            assert mock_get.call_count == 2  # Still only called once per hub
            
            # Results should be identical
            assert result1 == result2

    def test_cache_key_precision(self):
        """Test cache key uses 5 decimal precision"""
        from delivery_service import _get_cache_key
        
        # Different precision should map to same cache key
        key1 = _get_cache_key(30.0, 31.0, 30.123456, 31.654321)
        key2 = _get_cache_key(30.0, 31.0, 30.12346, 31.65432)  # Both round to 30.12346, 31.65432
        
        assert key1 == key2
        
        # Different coordinates should have different keys
        key3 = _get_cache_key(30.0, 31.0, 30.12345, 31.65432)  # This rounds to 30.12345, 31.65432
        assert key3 != key1
