from app.extentions import db
from flask import request,jsonify
from app.models.product import Product
from app.models.stock import Stock
from app.logger import Logger

logger = Logger().get_logger()

def add_stock_controller(product_id):
    logger.info("trying to add stock")
    try:
        data = request.get_json()
        if not data.get("quantity",None):
            logger.debug("Missing required field")
            return jsonify({'success':False,'error': 'Missing required field'}), 400
        product = Product.get_by_id(product_id)
        if not product:
            return jsonify({'success':False,'error': 'Product not found'}),404
        stock = Stock.get_by_product_id(product_id)
        if stock:
            # Update existing stock
            stock.quantity += data['quantity']
        else:
            # Create new stock entry
            stock = Stock(product_id=product_id, quantity=data['quantity'])
        stock.save()
        message=f"successfully added quantity: {stock.quantity} for product id: {product_id}"
        logger.info(message)
        return jsonify({'success':True,'data':stock.data}), 200
    except Exception as e:
        logger.error(f"add stock to product id- {product_id} failed with error: {e}")
        return jsonify({'success':False,'error': str(e)}), 500
    
def remove_stock_controller(product_id):
    logger.info("trying to reduce quantity")
    data = request.get_json()
    
    if not data.get("quantity",None):
        logger.info("Missing required field")
        return jsonify({'success':False,'error': 'Missing required field'}), 400
    
    product = Product.get_by_id(product_id)
    if not product:
        logger.info("Product not found")
        return jsonify({'success':False,'error': 'Product not found'}),404
      
    stock = Stock.get_by_product_id(product_id)
    if not stock:
        logger.info("Stock not found")
        return jsonify({'success':False,'error': 'Stock not found'}), 400
    
    if stock.quantity < data['quantity']:
        logger.info("can not reduce quantity. Insufficient stock.")
        return jsonify({'success':False,'error': 'Insufficient stock'}), 400
    
    try:
        stock.quantity -= data['quantity']
        stock.save()
        logger.info("successfully reduce a quantity")
        return jsonify({'success':True, 'data':stock.data}), 200
    except Exception as e:
        logger.info(f"error while reducing a quantity: {e}")
        return jsonify({'success':False,'error': str(e)}), 500
    

def get_stock_level_controller(product_id):
    """Get current stock level for a specific product"""
    product = Product.get_by_id(product_id)
    if not product:
        return jsonify({'success':False,'error': 'Product not found'}),404
    
    stock = Stock.get_by_product_id(product_id)
    if not stock:
        return jsonify({'success':False,'error': 'Stock not found'}), 404
    
    return jsonify({'success':True, 'data': stock.data}), 200

def get_below_threshold_controller():
    """List products below minimum threshold"""
    try: 
        products_below_threshold=(db.session.query(
            Product.id,
            Product.name,
            Stock.quantity)
        .join(Stock)
        .filter(Stock.quantity < Product.min_stock_threshold)
        .all())

        result = [
        { "product_id":product_id,
         "product_name":product_name,
         "quantity":quantity 
        }
        for product_id,product_name,quantity in products_below_threshold   
        ]
        
        return jsonify({'success':True, 'data':result}), 200
    except Exception as e:
        return jsonify({'success':False,'error': str(e)}), 500
    
def get_all_stock_controller():
    """Get stock levels for all products"""
    try:
        stocks = Stock.get_all()
        return jsonify({'success':True,"data":stocks}), 200
    except Exception as e:
        return jsonify({'success':False,'error': str(e)}), 500