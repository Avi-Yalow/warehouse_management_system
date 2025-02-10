import os
from dotenv import load_dotenv

load_dotenv()
 
class Config:
    DEBUD=True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///warehouse.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #SECRET_KEY = os.getenv('SECRET_KEY', 'dev')