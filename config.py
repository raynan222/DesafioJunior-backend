import os
from datetime import timedelta
from dotenv import load_dotenv
load_dotenv()

DEBUG = True

default = 'postgresql+psycopg2://postgres:postgres@localhost/web_app'

# db for deployment
#SQLALCHEMY_DATABASE_URI = default #Para execução local
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_TEST_URI', default)
# db for unit test
SQLALCHEMY_TEST_DATABASE_URI = os.getenv('DATABASE_TEST_URI', None)

JWT_SECRET_KEY = 'DG2yKyvb9HRUSrysF'
ROWS_PER_PAGE = 10
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))