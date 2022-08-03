import os
from datetime import timedelta

DEBUG = True

SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost/web_app'

JWT_SECRET_KEY = 'DG2yKyvb9HRUSrysF'
ROWS_PER_PAGE = 10
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))