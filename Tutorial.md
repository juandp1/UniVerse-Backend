# Tutorial Login

1. Crear un archivo con el nombre `requirements.txt` y agregar las dependencias que se necesitan para el proyecto:

```txt
# Contenido de requirements.txt
aniso8601==9.0.1
blinker==1.6.2
click==8.1.3
Flask==2.3.2
Flask-Cors==3.0.10
Flask-JWT-Extended==4.4.4
Flask-RESTful==0.3.9
Flask-SQLAlchemy==3.0.3
greenlet==2.0.2
install==1.3.5
itsdangerous==2.1.2
Jinja2==3.1.2
MarkupSafe==2.1.2
mysqlclient==2.1.1
PyJWT==2.6.0
python-dotenv==1.0.0
pytz==2023.3
six==1.16.0
SQLAlchemy==2.0.12
typing_extensions==4.5.0
Werkzeug==2.3.3
```

2. Para instalar estas dependencias se debe ejecutar el siguiente comando en el terminal:

```bash
pip install -r requirements.txt
```

3. Crear un archivo con el nombre `.env` y agregar las variables de entorno que se necesitan para el proyecto:

```txt
# Server
HOST=localhost
PORT=3333
ENV=development
SECRET_KEY=
# MySQL
MYSQL_USER=root
MYSQL_PASSWORD=1234567890
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DB_NAME=universe
# JWT
JWT_SECRET_KEY=
```

**NOTA:** Es necesario una base de datos MySQL/MariaDB para poder ejecutar el proyecto. Adicionalmente debe crear un SCHEMA con el nombre de `universe`

4. Crear la carpeta `config` y dentro crear el archivo `database_conf.py`, en dicho archivo se debe agregar el siguiente código:

```python
from flask_sqlalchemy import SQLAlchemy

# Configuring the Flask-SQLAlchemy
db = SQLAlchemy()
```

5. Crear el archivo `server_variables.py` dentro de la carpeta `config` y agregar el siguiente código:

```python
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


DATABASE_CONNECTION_URI = (
    f"mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
)
```

6. Crear el archivo `routes_conf.py` dentro de la carpeta `config` y agregar el siguiente código:

```python
from routes.auth import add_resources as add_auth_resources

def start_routes(api):
    add_auth_resources(api)
```

7. Dentro de la carpeta config crear un archivo con el nombre `server_conf.py` y agregar el siguiente código:

```python
from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from datetime import timedelta
from flask_jwt_extended import JWTManager
from config.database_conf import db
from config.server_variables import *
from config.routes_conf import start_routes

# Import models
from config.load_models import *

# Configuring the Flask app
app = Flask(__name__)
cors = CORS(app)

app.secret_key = SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_CONNECTION_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

# Configuring the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

# Start the Flask-JWT-Extended and the Flask-ReSTful extension
jwt = JWTManager(app)
api = Api(app)

with app.app_context():
    db.init_app(app)
    db.create_all()


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    token = TokenBlockListModel.query.filter_by(jti=jti).one_or_none()

    return token is not None


# Start the routes
start_routes(api)


def run_server():
    is_dev_env = False if SERVER_ENV == "production" else True
    app.run(host=SERVER_HOST, port=SERVER_PORT, debug=is_dev_env)

```

8. Antes de iniciar, es necesario crear el modelo de usuario para ello se debe crear la carpeta `models` y dentro de ella crear el archivo `User.py` y agregar el siguiente código:

```python
import re
import datetime
from config.server_conf import db
from werkzeug.security import check_password_hash


class UserModel(db.Model):
    __tablename__ = "User"

    # Attributes
    id = db.Column("id_user", db.Integer, primary_key=True)
    email = db.Column("email", db.String(100), nullable=False, unique=True)
    name = db.Column("name", db.String(100), nullable=False, unique=True)
    password = db.Column("password", db.String(255), nullable=False)
    is_active = db.Column("is_active", db.Boolean, nullable=False, default=True)
    created_at = db.Column(
        "created_at", db.DateTime, nullable=False, default=datetime.datetime.utcnow
    )
    updated_at = db.Column(
        "updated_at",
        db.DateTime,
        nullable=False,
        default=datetime.datetime.utcnow,
    )

    # Methods
    def __init__(self, email, name, password):
        self.email = email
        self.name = name
        self.password = password

    def json(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
        }

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def save_to_db(self):
        self.updated_at = datetime.datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def is_valid_email(email):
        regex = re.compile(
            r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
        )

        return re.fullmatch(regex, email)
```

9. Adicionalmente creamos un modelo para el manejo de token, para ello se debe crear la carpeta `models` y dentro de ella crear el archivo `TokenBlockList.py` y agregar el siguiente código:

```python
from datetime import datetime, timezone
from config.server_conf import db
from flask_jwt_extended import get_jwt_identity, jwt_required


class TokenBlockListModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)
    type = db.Column(db.String(16), nullable=False)
    user_id = db.Column(
        db.ForeignKey("User.id_user"),
        nullable=False,
        default=lambda: TokenBlockListModel.get_current_user().id_user,
    )
    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.now(timezone.utc)
    )

    def __init__(self, jti, type, created_at, user_id):
        self.jti = jti
        self.type = type
        self.created_at = created_at
        self.user_id = user_id

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    @jwt_required()
    def get_current_user():
        return get_jwt_identity()
```

10. Siguiendo la estructura MVC, se debe crear la carpeta `controllers` y dentro de ella crear el archivo `User.py` y agregar el siguiente código:

```python
from models.user import UserModel
from datetime import datetime, timezone
from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash
from models.token_blocklist import TokenBlockListModel
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
    create_refresh_token,
    get_jwt,
)

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "name", type=str, required=True, help="This field cannot be blank."
    )
    parser.add_argument(
        "email", type=str, required=True, help="This field cannot be blank."
    )
    parser.add_argument(
        "password", type=str, required=True, help="This field cannot be blank."
    )

    def post(self):
        data = UserRegister.parser.parse_args()
        existing_user = UserModel.query.filter_by(
            email=data["email"], is_active=True
        ).one_or_none()
        if existing_user:
            return {"message": "A user with that email already exists"}, 400

        if not UserModel.is_valid_email(data["email"]):
            return {"message": "Invalid email format"}, 400

        existing_user = UserModel.query.filter_by(
            email=data["email"], is_active=False
        ).one_or_none()
        if existing_user is not None:
            user = UserModel.query.filter_by(
                email=data["email"], is_active=False
            ).one_or_none()
            user.recover_user()
            return user.json(), 201

        user = UserModel(**data)
        user.password = generate_password_hash(data["password"], method="pbkdf2")
        try:
            user.save_to_db()
            return user.json(), 201
        except:
            return {"message": "An error occurred creating the user."}, 500


class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "email", type=str, required=True, help="This field cannot be blank."
    )
    parser.add_argument(
        "password", type=str, required=True, help="This field cannot be blank."
    )

    def post(self):
        data = UserLogin.parser.parse_args()
        email = data["email"]
        password = data["password"]

        user = UserModel.query.filter_by(email=email).one_or_none()
        if not user or not user.check_password(password):
            return {"message": "Invalid credentials"}, 401

        access_token = create_access_token(identity=user.json())
        refresh_token = create_refresh_token(identity=user.json())
        return {
            "user": user.json(),
            "access_token": access_token,
            "refresh_token": refresh_token,
        }, 200


class UserLogout(Resource):
    @jwt_required(verify_type=False)
    def delete(self):
        token = get_jwt()
        jti = token["jti"]
        ttype = token["type"]
        now = datetime.now(timezone.utc)

        token = TokenBlockListModel(
            jti,
            type=ttype,
            created_at=now,
            user_id=get_jwt_identity()["id"] if ttype == "access" else None,
        )

        try:
            token.save_to_db()
            return {"message": "Successfully logged out"}, 200
        except:
            return {"message": "An error occurred logging out"}, 500
```

11. Es necesario crear las rutas para el login, para ello se debe crear la carpeta `routes` y dentro de ella crear el archivo `auth.py` y agregar el siguiente código:

```python
# Import resources
from controllers.User import UserRegister, UserLogin, UserLogout


# Add resources to the API
def add_resources(api):
    api.add_resource(UserLogin, "/api/login")
    api.add_resource(UserRegister, "/api/register")
    api.add_resource(UserLogout, "/api/logout")
```

12. Para finalizar, se debe crear el archivo `server.py` y agregar el siguiente código:

```python
from config.server_conf import run_server

if __name__ == "__main__":
    run_server()
```
