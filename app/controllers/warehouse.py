from datetime import datetime
from app.extentions import db
from flask import request,jsonify
from app.models.product import Product
from app.models.stock import Stock
from app.logger import Logger

logger = Logger().get_logger()

def get_statistics_controller():
    try:
        logger.info("Get the total number of products")
        total_products = Product.query.count()
        
        logger.info("Get total products with stock")
        products_with_stock = Stock.query.filter(Stock.quantity > 0).count()
        
        # Total quantity of all products
        total_stock = db.session.query(db.func.sum(Stock.quantity)).scalar() or 0
        
        # Products below threshold
        low_stock_count = (
            Product.query
            .join(Stock)
            .filter(Stock.quantity < Product.min_stock_threshold)
            .count()
        )
        
        # Out of stock products
        out_of_stock = Stock.query.filter(Stock.quantity == 0).count()
        
        # Average stock level per product
        avg_stock = db.session.query(db.func.avg(Stock.quantity)).scalar() or 0
        
        # Products by category
        category_stats =( db.session.query(
                Product.category,
                db.func.array_agg(Product.id).label('product_ids'),
                db.func.count(Product.id).label('count'),
                db.func.sum(Stock.quantity).label('total_stock')
            ).join(Stock)
            .group_by(Product.category)
            .all())
        
        
        
        category_details = [
            {
                'category': cat,
                "product_ids":product_ids,
                'count': count,
                'total_stock': int(total or 0)
            }
            for cat,product_ids,count, total in category_stats
        ]

        statistics = {
            'total_products': total_products,
            'products_with_stock': products_with_stock,
            'total_stock_quantity': int(total_stock),
            'low_stock_alerts': low_stock_count,
            'out_of_stock_count': out_of_stock,
            'average_stock_per_product': round(float(avg_stock), 2),
            'category_details': category_details,
            'generated_at': datetime.now()
        }
        
        return jsonify({"success":True,"data":statistics}), 200
    
    except Exception as e:
        return jsonify({"success":False,'error': str(e)}), 500

def generate_low_stock_report_controller():
    try:
        low_stock_items = (
            db.session.query(
                Product.id,
                Product.name,
                Product.category,
                Product.manufacturer,
                Product.min_stock_threshold,
                Stock.quantity,
                Stock.last_updated
            )
            .join(Stock)
            .filter(Stock.quantity < Product.min_stock_threshold)
            .all()
        )
        
        report = {
            'report_type': 'Low Stock Alert Report',
            'generated_at': datetime.now(),
            'alert_count': len(low_stock_items),
            'items': [
                {
                    'product_id': id,
                    'name': name,
                    'category': category,
                    'manufacturer': manufacturer,
                    'min_threshold': min_threshold,
                    'current_stock': quantity,
                    'last_updated': last_updated,
                    'shortage': min_threshold - quantity
                }
                for id, name, category, manufacturer, min_threshold, quantity, last_updated in low_stock_items
            ]
        }
        
        return jsonify({"success":True,"data":report}), 200
    
    except Exception as e:
        return jsonify({"success":False,'error': str(e)}), 500


def generate_inventory_report_controller():
    """Generate detailed inventory report"""
    try:
        inventory_report = (
            db.session.query(
                Product.id,
                Product.name,
                Product.category,
                Product.manufacturer,
                Product.min_stock_threshold,
                Stock.quantity,
                Stock.last_updated
            )
            .join(Stock)
            .all()
        )
        
        report = {
            'report_type': 'Inventory Report',
            'generated_at': datetime.now(),
            'items': [
                {
                    'product_id': id,
                    'name': name,
                    'category': category,
                    'manufacturer': manufacturer,
                    'min_threshold': min_threshold,
                    'current_stock': quantity,
                    'last_updated': last_updated,
                    'status': 'LOW STOCK' if quantity < min_threshold else 'OK'
                }
                for id, name, category, manufacturer, min_threshold, quantity, last_updated in inventory_report
            ]
        }
        
        return jsonify({"success":True,"data":report}), 200
    
    except Exception as e:
        return jsonify({"success":False,'error': str(e)}), 500
