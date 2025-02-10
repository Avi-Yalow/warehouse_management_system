import os
from flask import Flask
from app.config import Config
from app.extentions import db
from flask_migrate import Migrate
from app.routes.product import product_bp
from app.routes.stock import stock_bp
from app.routes.warehouse import warehouse_bp



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate = Migrate(app,db)
    with app.app_context():
        db.create_all()

    # app.config['TIMEOUT'] = 5 
    
    # Register blueprints
    app.register_blueprint(product_bp)
    app.register_blueprint(stock_bp)
    app.register_blueprint(warehouse_bp)

    return app


    
    
    