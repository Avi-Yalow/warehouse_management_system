from flask import Blueprint
from app.controllers.warehouse import *

warehouse_bp = Blueprint('warehouse', __name__,url_prefix="/api/warehouse")


@warehouse_bp.route('/statistics', methods=['GET'])
def get_warehouse_statistics():
    """Get comprehensive warehouse statistics"""
    return get_statistics_controller()

@warehouse_bp.route('/reports/inventory', methods=['GET'])
def generate_inventory_report():
    return generate_inventory_report_controller()

@warehouse_bp.route('/reports/low-stock', methods=['GET'])
def generate_low_stock_report():
   return generate_low_stock_report_controller()