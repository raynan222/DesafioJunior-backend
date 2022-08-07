import os
from datetime import timedelta

DEBUG = (os.getenv('ENV', "dev") == "dev")

SQLALCHEMY_HOST = os.getenv('DB_HOST', "localhost")
SQLALCHEMY_USER = os.getenv('DB_USER', "postgres")
SQLALCHEMY_PWD = os.getenv('DB_PASSWORD', "postgres")
SQLALCHEMY_DB_NAME = os.getenv('DB_NAME', "web_app")
SQLALCHEMY_PORT = os.getenv('DB_PORT', ":5432")
SQLALCHEMY_DRIVER = os.getenv('DB_DRIVER', "postgresql+psycopg2")
SQLALCHEMY_DB_TEST_NAME = os.getenv('DB_TEST_NAME', "web_app_pytest")

SQLALCHEMY_DATABASE_URI = f'{SQLALCHEMY_DRIVER}://{SQLALCHEMY_USER}:{SQLALCHEMY_PWD}@{SQLALCHEMY_HOST}{SQLALCHEMY_PORT}/{SQLALCHEMY_DB_NAME}'

JWT_SECRET_KEY = 'DG2yKyvb9HRUSrysF'
ROWS_PER_PAGE = 10
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
