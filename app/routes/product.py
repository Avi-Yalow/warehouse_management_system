from flask import Blueprint
from app.controllers.product import *
product_bp = Blueprint('product', __name__,url_prefix="/api/products")

@product_bp.route('/add', methods=['POST'])
def add_product():
    return add_product_controller()

@product_bp.route('/', methods=['GET'])
def get_all_products():
    return get_all_products_controller()

@product_bp.route('/<int:id>', methods=['GET'])
def get_product(id):
    return get_product_controller(id)

@product_bp.route('/<int:id>', methods=['PUT'])
def edit_product(id):
    return update_product_controller(id)

@product_bp.route('/<int:id>', methods=['DELETE'])
def delete_product(id):
    return delete_product_controller(id)
