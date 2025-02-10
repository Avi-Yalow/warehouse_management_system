import pytest
from utils.api_client import APIClient

class TestProducts:
    """Test suite for Product endpoints"""

    @pytest.fixture(scope="module")
    def api_client(self):
        return APIClient()
    
    @pytest.fixture
    def sample_product_data(self):
        """Fixture to provide sample product data"""
        return {
            "name": "Test Product",
            "category": "Test Category",
            "price": 99.99,
            "manufacturer":"Test Manufacturer"
        }
    
    @pytest.fixture
    def created_product(self, api_client, sample_product_data):
        """Fixture to create a test product and clean up after"""
        response = api_client.post(
            "api/products/add",
            data=sample_product_data
        )
        product = response.json()
        print(product)
        yield product
        # Cleanup
        product_id = product.get('data', {}).get('product_id')
        api_client.delete(f"/api/products/{product_id}")

    def test_create_product(self, api_client, sample_product_data):
        """Test creating a new product"""
        response = api_client.post(
            f"/api/products/add",
            data=sample_product_data
        )
        assert response.status_code == 201
        respose_name = response.json().get('data', {}).get('name')
        current_name= sample_product_data.get('name')
        assert respose_name == current_name
        
        # Cleanup
        product_id = response.json()['data']['product_id']
        api_client.delete(f"/api/products/{product_id}")

    def test_get_all_products(self, api_client):
        """Test retrieving all products"""
        response = api_client.get(f"/api/products")
        assert response.status_code == 200
        assert isinstance(response.json()['data'], list)

    def test_get_single_product(self, api_client, created_product):
        """Test retrieving a single product"""
        response = api_client.get(
            f"/api/products/{created_product['data']['product_id']}"
        )
        assert response.status_code == 200
        assert response.json()['data']['name'] == created_product['data']['name']
        # Cleanup
        product_id = created_product['data']['product_id']
        api_client.delete(f"/api/products/{product_id}")

    def test_update_product(self, api_client, created_product):
        """Test updating an existing product"""
        updated_data = {
            "category": "Updated Category",
            "price": 1099.99,
            "manufacturer":"Updated Manufacturer"
        }
        response = api_client.put(
            f"/api/products/{created_product['data']['product_id']}",
            data=updated_data
        )
        assert response.status_code == 200

        response = api_client.get(
            f"/api/products/{created_product['data']['product_id']}"
        )
        assert response.status_code == 200
        assert response.json()['data']['price'] == updated_data['price']
        assert response.json()['data']['manufacturer'] == updated_data['manufacturer']

    def test_delete_product(self, api_client, created_product):
        """Test deleting a product"""
        response = api_client.delete(
            f"/api/products/{created_product['data']['product_id']}"
        )
        assert response.status_code == 204

        # Verify product is deleted
        get_response = api_client.get(
            f"/api/products/{created_product['data']['product_id']}"
        )
        assert get_response.status_code == 404
