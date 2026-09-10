import os

from dotenv import load_dotenv

load_dotenv()

DB_DRIVER = os.getenv('DB_DRIVER')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
