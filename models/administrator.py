import datetime
from config.server_conf import db


class AdministratorModel(db.Model):
    __tablename__ = "Administrator"

    # Attributes
    id = db.Column(
        "User_id_user", db.Integer, db.ForeignKey("User.id_user"), primary_key=True
    )
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
    def __init__(self, id):
        self.id = id

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id, is_active=True).first()
