from app.extentions import db
from flask import request,jsonify
from app.models.product import Product
from app.models.stock import Stock
from app.logger import Logger

logger = Logger().get_logger()

def add_product_controller():
    logger.info("trying to create product...")
    try:        
        data = request.get_json()
        logger.info(f"create product data: {data}")
        new_product = Product(name=data['name'], price=data['price'],category=data['category'],
        manufacturer=data['manufacturer'])
        new_stock = Stock(quantity=0,product_id=new_product.id)
        new_product.stock = new_stock
        new_product.save()
        logger.info("product created successfully!")
        prodcut_data={'product_id': new_product.id,'name':new_product.name}
        logger.info(f"prodcut data created: {prodcut_data}")
        return jsonify({'success':True,'data': prodcut_data}), 201
    except Exception as e:
        logger.error(f"create product failed with an error: {e}")
        return jsonify({'success':False,'error': str(e)}), 500

def get_all_products_controller():
    logger.info("trying to retrieve all the products...")
    try:
        products=  Product.get_all()
        logger.info(f"product data: {products}")
        return jsonify({'success':True,'data': products}), 200
    except Exception as e:
         logger.error("get all products failed with an error: {e}")
         return jsonify({'success':False,'error': str(e)}), 500
      

def get_product_controller(id):
    logger.info(f"trying to get product id : {id}")
    try:
        product = Product.get_by_id(id)
        if product:
            logger.info(f"product data: {product.data}")
            return jsonify({'success':True,'data': product.data}), 200
        else:
            logger.error("product not found")
            return jsonify({'success':False,'error': "product not found"}), 404
    except Exception as e:
        logger.error(f"get product failed with error: {e}")
        return jsonify({'success':False,'error': str(e)}), 500
     
def update_product_controller(id):
    try:
        product = Product.get_by_id(id)
        new_data = request.get_json()
        product.category= new_data.get("category",product.category)
        product.price= new_data.get("price",product.price)
        product.manufacturer= new_data.get("manufacturer",product.manufacturer)

        db.session.commit()
        logger.info("product updated successfully!")
        return jsonify({'success':True,'data': product.data}), 200
    except Exception as e:
        logger.error(f"update product failed with error: {e}")
        return jsonify({'success':False,'error': str(e)}), 500
    
      
    
def delete_product_controller(id):
    try:
        product = Product.get_by_id(id)
        if product:
            db.session.delete(product)
            db.session.commit()
            logger.info("product deleted successfully!")
            return jsonify({'success':True,'message': "product deleted"}), 204
        else:
            logger.error("product not found")
            return jsonify({'success':False,'error': "product not found"}), 404
    except Exception as e:
        logger.error(f"delete product failed with error: {e}")
        return jsonify({'success':False,'error': str(e)}), 500
          