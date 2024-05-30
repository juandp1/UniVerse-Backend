from dotenv import load_dotenv
from os import environ

load_dotenv()

# Flask Environment Variables
SERVER_HOST = environ.get("HOST")
SERVER_PORT = environ.get("PORT")
SERVER_ENV = environ.get("ENV")
SECRET_KEY = environ.get("SECRET_KEY")
JWT_SECRET_KEY = environ.get("JWT_SECRET_KEY")

# MySQL Environment Variables
MYSQL_USER = environ.get("MYSQL_USER")
MYSQL_PASSWORD = environ.get("MYSQL_PASSWORD")
MYSQL_HOST = environ.get("MYSQL_HOST")
MYSQL_PORT = environ.get("MYSQL_PORT")
MYSQL_DB = environ.get("MYSQL_DB_NAME")
# MYSQL_SECRET_KEY = environ.get("MYSQL_SECRET_KEY")
DATABASE_CONNECTION_URI = f"mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"

# For production environment only
SSL_NAME = environ.get("SSL_NAME")
if SSL_NAME:
  DATABASE_CONNECTION_URI += f"?ssl_ca={SSL_NAME}.crt.pem"


