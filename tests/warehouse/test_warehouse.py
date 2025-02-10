import pytest
from utils.api_client import APIClient

class TestWarehouse:
    """Test suite for Warehouse-related endpoints"""

    @pytest.fixture(scope="module")
    def api_client(self):
        return APIClient()
    
    def test_get_warehouse_statistics(self, api_client):
        """Test retrieving warehouse statistics"""
        response = api_client.get(f"/api/warehouse/statistics")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data['success'] is True
        stats = data['data']
        
        # Verify key statistics are present and have expected types
        assert 'total_products' in stats
        assert 'products_with_stock' in stats
        assert 'total_stock_quantity' in stats
        assert 'low_stock_alerts' in stats
        assert 'out_of_stock_count' in stats
        assert 'average_stock_per_product' in stats
        assert 'category_details' in stats
        assert 'generated_at' in stats
        
        # Type checks
        assert isinstance(stats['total_products'], int)
        assert isinstance(stats['products_with_stock'], int)
        assert isinstance(stats['total_stock_quantity'], int)
        assert isinstance(stats['low_stock_alerts'], int)
        assert isinstance(stats['out_of_stock_count'], int)
        assert isinstance(stats['average_stock_per_product'], float)
        assert isinstance(stats['category_details'], list)


    def test_generate_inventory_report(self, api_client):
        """Test generating inventory report"""
        response = api_client.get(f"/api/warehouse/reports/inventory")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data['success'] is True
        report = data['data']
        
        # Verify report structure
        assert report['report_type'] == 'Inventory Report'
        assert 'generated_at' in report
        assert 'items' in report
        
        # Verify report items have correct keys
        if report['items']:
            first_item = report['items'][0]
            expected_keys = [
                'product_id', 'name', 'category', 'manufacturer', 
                'min_threshold', 'current_stock', 'last_updated', 'status'
            ]
            for key in expected_keys:
                assert key in first_item
            
            # Verify status is either 'LOW STOCK' or 'OK'
            assert first_item['status'] in ['LOW STOCK', 'OK']
    
    
    def test_generate_low_stock_report(self, api_client, base_url):
        """Test generating low stock report"""
        response = api_client.get(f"/api/warehouse/reports/low-stock")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data['success'] is True
        report = data['data']
        
        # Verify report structure
        assert report['report_type'] == 'Low Stock Alert Report'
        assert 'generated_at' in report
        assert 'alert_count' in report
        assert 'items' in report
        
        # Verify report items have correct keys and logic
        if report['items']:
            first_item = report['items'][0]
            expected_keys = [
                'product_id', 'name', 'category', 'manufacturer', 
                'min_threshold', 'current_stock', 'last_updated', 'shortage'
            ]
            for key in expected_keys:
                assert key in first_item
            
            # Verify shortage calculation
            assert first_item['shortage'] == first_item['min_threshold'] - first_item['current_stock']
        
        # Verify alert count matches number of items
        assert report['alert_count'] == len(report['items'])