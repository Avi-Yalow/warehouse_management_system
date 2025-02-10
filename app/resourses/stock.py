from flask_restx import Resource, Namespace
from app.controllers.stock import *
from flask_restx import  Resource, fields, Namespace

# Create a namespace for products
stocks_ns = Namespace('api/stocks', description='stock operations')
stock_model = stocks_ns.model('Stock', {
    'quantity': fields.Integer(required=True, description='quantity')
})

@stocks_ns.route('/')
class StockList(Resource):
    @stocks_ns.doc('list_stocks',
        responses={
            200: 'Success',
            500: 'Internal Server Error'
        })
    def get(self):
        """Get stock levels for all products"""
        return get_all_stock_controller()
    
@stocks_ns.route('/below-threshold')
class StockMinThreshold(Resource):
    @stocks_ns.doc('list_stocks',
        responses={
            200: 'Success',
            500: 'Internal Server Error'
        })
    def get(self):
        """List products below minimum threshold"""
        return get_below_threshold_controller()
    
@stocks_ns.route('/add/<int:product_id>')
@stocks_ns.param('product_id', 'The product identifier')
@stocks_ns.response(404, 'Product not found')
class StockAdd(Resource):
    @stocks_ns.doc('add_stock',
        responses={
            200: 'success',
            404:'Product not found',
            400: 'Invalid input',
            500: 'Internal Server Error'
        })
    @stocks_ns.expect(stock_model)
    def post(self,product_id):
        """add a quantity to product in the warehouse"""
        return add_stock_controller(product_id)
    
@stocks_ns.route('/remove/<int:product_id>')
@stocks_ns.param('product_id', 'The product identifier')
@stocks_ns.response(404, 'Product not found')
class StockRemove(Resource):
    @stocks_ns.doc('remove_stock',
        responses={
            200: 'success',
            404:'Product not found',
            400: 'Invalid input',
            500: 'Internal Server Error'
        })
    @stocks_ns.expect(stock_model)
    def post(self,product_id):
        """reduce a quantity to product in the warehouse"""
        return remove_stock_controller(product_id)
    
@stocks_ns.route('/<int:id>')
@stocks_ns.param('id', 'The product identifier')
@stocks_ns.response(404, 'Product not found')
class Product(Resource):
    @stocks_ns.doc('get_stock',
        responses={
            200: 'Success',
            404: 'Product not found',
            500: 'Internal Server Error'
        })
    def get(self, id):
        """Fetch a product by ID including its stock information"""
        return get_stock_level_controller(id)
  


