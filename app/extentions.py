from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api

api= Api(
    title='Warehouse Management System API',
    version='1.0',
    description='API for managing products and their stock levels in a warehouse',
    doc='/docs',
)
db=SQLAlchemy()