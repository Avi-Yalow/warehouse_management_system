import os
from flask import Flask
from app.config import Config
from app.extentions import db,api
from flask_migrate import Migrate
from app.routes.product import product_bp
from app.routes.stock import stock_bp
from app.routes.warehouse import warehouse_bp
from app.resourses.product import product_ns
from app.resourses.stock import stocks_ns
from app.resourses.warehouse import warehouse_ns


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    api.init_app(app)
    migrate = Migrate(app,db)
    with app.app_context():
        db.create_all()

    # app.config['TIMEOUT'] = 5 
    
    # Register blueprints
    app.register_blueprint(product_bp)
    app.register_blueprint(stock_bp)
    app.register_blueprint(warehouse_bp)

    # add name spaces
    api.add_namespace(product_ns)
    api.add_namespace(stocks_ns)
    api.add_namespace(warehouse_ns)

    return app


    
    
    