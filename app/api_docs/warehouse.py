from flask_restx import Resource, Namespace
from app.controllers.warehouse import *
from flask_restx import  Resource, fields, Namespace

# Create a namespace for products
warehouse_ns = Namespace('api/warehouse', description='warehouse operations')


@warehouse_ns.route('/statistics')
class WarehouseStatics(Resource):
    @warehouse_ns.doc('statistics',
        responses={
            200: 'Success',
            500: 'Internal Server Error'
        })
    def get(self):
        """Get comprehensive warehouse statistics"""
        return get_statistics_controller()


@warehouse_ns.route('/reports/inventory')
class WarehouseInventoryReport(Resource):
    @warehouse_ns.doc('inventory_report',
        responses={
            200: 'Success',
            500: 'Internal Server Error'
        })
    def get(self):
        """Get comprehensive warehouse report"""
        return generate_inventory_report_controller()

@warehouse_ns.route('/reports/low-stock')
class WarehouseLowStockReport(Resource):
    @warehouse_ns.doc('low-stock-report',
        responses={
            200: 'Success',
            500: 'Internal Server Error'
        })
    def get(self):
        """Get comprehensive warehouse low-stock-report"""
        return generate_low_stock_report_controller()