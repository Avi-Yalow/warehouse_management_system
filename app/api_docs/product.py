from flask_restx import Resource, Namespace
from app.controllers.product import *
from flask_restx import  Resource, fields, Namespace


# Create a namespace for products
product_ns = Namespace('api/products', description='Product operations')


product_model = product_ns.model('Product', {
    'name': fields.String(required=True, description='Product name'),
    'price': fields.Float(required=True, description='Product price'),
    'category': fields.String(required=True, description='Product category'),
    'manufacturer': fields.String(required=True, description='Product manufacturer')
})

product_update_model = product_ns.model('ProducUpdate', {
    'price': fields.Float(required=False, description='Product price'),
    'category': fields.String(required=False, description='Product category'),
    'manufacturer': fields.String(required=False, description='Product manufacturer')
})

@product_ns.route('/')
class ProductList(Resource):
    @product_ns.doc('list_products',
        responses={
            200: 'Success',
            500: 'Internal Server Error'
        })
    def get(self):
        """List all products with their stock information"""
        return get_all_products_controller()
    
@product_ns.route('/add')
class ProductAdd(Resource):
    @product_ns.doc('create_product',
        responses={
            201: 'Product created',
            400: 'Invalid input',
            500: 'Internal Server Error'
        })
    @product_ns.expect(product_model)
    def post(self):
        """Create a new product with initial stock"""
        return add_product_controller()

@product_ns.route('/<int:id>')
@product_ns.param('id', 'The product identifier')
@product_ns.response(404, 'Product not found')
class Product(Resource):
    @product_ns.doc('get_product',
        responses={
            200: 'Success',
            404: 'Product not found',
            500: 'Internal Server Error'
        })
    def get(self, id):
        """Fetch a product by ID including its stock information"""
        return get_product_controller(id)
    
    @product_ns.doc('update_product',
        responses={
            200: 'Product updated',
            400: 'Invalid input',
            404: 'Product not found',
            500: 'Internal Server Error'
        })
    
    @product_ns.expect(product_update_model)
    def put(self, id):
        """Update price, category or manufacturer in product"""
        return update_product_controller(id)
    
    @product_ns.doc('delete_product',
        responses={
            204: 'Product deleted',
            404: 'Product not found',
            500: 'Internal Server Error'
        })
    def delete(self, id):
        """Delete a product and its associated stock"""
        return delete_product_controller(id)


