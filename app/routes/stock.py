from flask import Blueprint
from app.controllers.stock import *
stock_bp = Blueprint('stock', __name__,url_prefix="/api/stocks")


@stock_bp.route('/add/<int:product_id>', methods=['POST'])
def add_stock(product_id):
    return add_stock_controller(product_id)

@stock_bp.route('/remove/<int:product_id>', methods=['POST'])
def remove_stock(product_id):
    return remove_stock_controller(product_id)

@stock_bp.route('/<int:product_id>', methods=['GET'])
def get_stock_level(product_id):
    return get_stock_level_controller(product_id)


@stock_bp.route('/min', methods=['GET'])
def get_below_threshold():
    return get_below_threshold_controller()

