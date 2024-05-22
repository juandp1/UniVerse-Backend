from dotenv import load_dotenv
import os

load_dotenv()

# Flask Environment Variables
SERVER_HOST = os.environ["HOST"]
SERVER_PORT = os.environ["PORT"]
SERVER_ENV = os.environ["ENV"]
SECRET_KEY = os.environ["SECRET_KEY"]
JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]

# MySQL Environment Variables
MYSQL_USER = os.environ["MYSQL_USER"]
MYSQL_PASSWORD = os.environ["MYSQL_PASSWORD"]
MYSQL_HOST = os.environ["MYSQL_HOST"]
MYSQL_PORT = os.environ["MYSQL_PORT"]
MYSQL_DB = os.environ["MYSQL_DB_NAME"]

#SSL_NAME = os.environ["SSL_NAME"]


DATABASE_CONNECTION_URI = f"mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
