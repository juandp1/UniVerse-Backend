import re
import datetime
from config.server_conf import db
from os import urandom 
from base64 import b32encode
from onetimepass import valid_totp
import utils.encryption as encryption


class UserModel(db.Model):
    __tablename__ = "User"

    # Attributes
    id = db.Column("id_user", db.Integer, primary_key=True)
    email = db.Column("email", db.String(100), nullable=False, unique=True)
    email_hash = db.Column("email_hash", db.String(100), nullable=False, unique=True)
    name = db.Column("name", db.String(100), nullable=False, unique=True)
    name_hash = db.Column("name_hash", db.String(100), nullable=False, unique=True)
    password = db.Column("password", db.String(255), nullable=False)
    salt = db.Column("salt", db.String(255), nullable=False)
    otp_secret = db.Column("otp_secret", db.String(16), nullable=False)
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
        self.otp_secret = b32encode(urandom(10)).decode("utf-8")

    def jsonP(self):
        self.name = encryption.decrypt_data(self.name)
        self.email = encryption.decrypt_data(self.email)
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
        }

    def json(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
        }
    
    def get_totp_uri(self):
        return f"otpauth://totp/{self.email}?secret={self.otp_secret}&issuer=Flask"
    
    def verify_totp(self, token):
        return valid_totp(token, self.otp_secret)

    def check_password(self, password):
        password = encryption.hash_password(password, self.salt)
        if self.password != password:
            return False
        return True

    def save_to_db(self):
        self.updated_at = datetime.datetime.utcnow()
        self.name_hash = encryption.hash_data(self.name)
        self.name = encryption.encrypt_data(self.name)
        self.email_hash = encryption.hash_data(self.email)
        self.email = encryption.encrypt_data(self.email)
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
        user = cls.query.filter_by(id=id, is_active=True).first()        
        user.name = encryption.decrypt_data(str(user.name))
        user.email = encryption.decrypt_data(str(user.email))
        return user

    @staticmethod
    def is_valid_email(email):
        regex = re.compile(
            r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
        )

        return re.fullmatch(regex, email)
