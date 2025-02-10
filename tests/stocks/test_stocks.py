import pytest
from utils.api_client import APIClient

class TestStocks:
    """Test suite for Stock endpoints"""
    
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
        if response.json()['success']:
            product = response.json()['data']
            yield product
        else:
            return None
        # Cleanup
        product_id = product.get('product_id')
        api_client.delete(f"/api/products/{product_id}")

    @pytest.fixture
    def sample_stock_data(self):
        """Fixture to provide sample stock data"""
        return {"quantity": 20}
    
    @pytest.fixture
    def created_stock(self, api_client,created_product, sample_stock_data):
        """Fixture to create a test stock and clean up after"""
        product_id = created_product.get('product_id',None)
        response = api_client.post(
            f"/api/stocks/add/{product_id}",
            data=sample_stock_data
        )
        stock = response.json()
        yield stock
        # Cleanup
        api_client.post(f"/api/stocks/remove/{product_id}",data=sample_stock_data)

    def test_get_all_stocks(self, api_client):
        """Test retrieving all stocks"""
        response = api_client.get(f"/api/stocks")
        assert response.status_code == 200
        assert isinstance(response.json()['data'], list)

    def test_get_single_stock(self, api_client,created_product):
        """Test retrieving a single stock"""
        response = api_client.get(
            f"/api/stocks/{created_product['product_id']}"
        )
        assert response.status_code == 200
        assert response.json()['data']['quantity'] == 0

    def test_add_stock(self, api_client, created_product,sample_stock_data):
        """Test creating a new stock entry"""
        response = api_client.get(
            f"/api/stocks/{created_product['product_id']}"
        )
        assert response.status_code == 200
        stock_before= response.json()['data']['quantity']

        #adding stock
        response = api_client.post(
            f"api/stocks/add/{created_product['product_id']}",
            data=sample_stock_data
        )
        assert response.status_code == 200
        assert response.json()['data']['quantity'] == stock_before+sample_stock_data['quantity']
        
        # Cleanup
        product_id = response.json()['data']['product_id']
        api_client.post(f"/api/stocks/remove/{product_id}",data=sample_stock_data)

   
    def test_remove_stock(self, api_client,created_product,sample_stock_data):
        
        product_id=created_product['product_id']
        #get stock before
        response = api_client.get(
            f"/api/stocks/{created_product['product_id']}"
        )
        assert response.status_code == 200
        stock_before= response.json()['data']['quantity']

        #adding quantity
        response = api_client.post(
            f"api/stocks/add/{product_id}",
            data=sample_stock_data
        )
        assert response.status_code == 200
        after_adding= stock_before + sample_stock_data['quantity']

        # remove quantity
        response=api_client.post(f"/api/stocks/remove/{product_id}",data=sample_stock_data)
        assert response.status_code == 200
        assert response.json()['data']['quantity']==after_adding-sample_stock_data['quantity']