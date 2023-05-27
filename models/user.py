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

    def delete_from_db(self):
        self.is_active = False
        self.updated_at = datetime.datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def recover_user(self):
        self.is_active = True
        self.updated_at = datetime.datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id, is_active=True).first()

    @staticmethod
    def is_valid_email(email):
        regex = re.compile(
            r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
        )

        return re.fullmatch(regex, email)
