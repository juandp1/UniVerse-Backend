import datetime
from config.server_conf import db


class UserModel(db.Model):
    __tablename__ = "User"

    # Attributes
    id = db.Column("id_user", db.Integer, primary_key=True)
    email = db.Column("email", db.String(100), nullable=False, unique=True)
    name = db.Column("name", db.String(100), nullable=False)
    password = db.Column("password", db.String(100), nullable=False)
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

    # Relationships
    administrator = db.relationship(
        "AdministratorModel", uselist=False, back_populates="user"
    )

    user_follows_label = db.relationship("UserFollowsLabelModel", back_populates="user")

    user_belongs_to_community = db.relationship(
        "UserBelongsToCommunityModel", back_populates="user"
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
            "is_active": self.is_active,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email, is_active=True).first()

    def save_to_db(self):
        self.updated_at = datetime.datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def delete_to_db(self):
        self.is_active = False
        self.updated_at = datetime.datetime.utcnow()
        db.session.add(self)
        db.session.commit()
