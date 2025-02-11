import queue
from app.extentions import db
from app.models.product import Product
from app.models.stock import Stock
from app.models.operation import Operation
from datetime import datetime
import time
from app.logger import Logger

logger = Logger().get_logger()

task_queue = queue.Queue()
task_results = {}

# Background worker
def process_task(app):
    logger.info("start background worker")
    while True:
        try:
            task = task_queue.get()
            if task is None:
                break
                
            task_id, operation_type, product_id, quantity = task
            logger.info(f"start task: task_id: {task_id}, operation_type: {operation_type}, product_id: {product_id}, quantity: {quantity}")
            
            # Simulate long-running operation
            operation_time = min(quantity // 100, 30)  # Scale with quantity, max 10 seconds
            time.sleep(operation_time)
            logger.info(f"estemation time: {operation_time}")
           
            with app.app_context():
                product = Product.query.get(product_id)
                stock = Stock.get_by_product_id(product_id)
                if product and stock:
                    if operation_type == 'add':
                        stock.quantity += quantity
                    elif operation_type == 'remove':
                        stock.quantity = max(0, stock.quantity - quantity)
                    
                    operation = Operation.query.get(task_id)
                    operation.status = 'completed'
                    operation.completed_at = datetime.now()
                    
                    db.session.commit()
                    
                    task_results[task_id] = {
                        'status': 'completed',
                        'product_id': product_id,
                        'new_quantity': stock.quantity
                    }
                    logger.info("task completed")    
            task_queue.task_done()
            
        except Exception as e:
            logger.error(f'Error processing task: {str(e)}')
            if 'task_id' in locals():
                task_results[task_id] = {'status': 'failed', 'error': str(e)}

