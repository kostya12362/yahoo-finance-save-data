from dotenv import load_dotenv
import os
load_dotenv()

ENV = "development"
PORT = os.environ.get('PORT')
DEBUG = os.environ.get('DEBUG')

SECRET_KEY = 'secretkeyforsessions'

SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{os.environ.get('DB_USER')}:{os.environ.get('DB_PASSWORD')}@{os.environ.get('DB_HOST')}:{os.environ.get('DB_PORT')}/{os.environ.get('DB_NAME')}"
SQLALCHEMY_TRACK_MODIFICATIONS = False

