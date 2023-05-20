import datetime
from config.server_conf import db


class LabelModel(db.Model):
    __tablename__ = "Label"

    # Attributes
    id = db.Column("id_label", db.Integer, primary_key=True)
    name = db.Column("name", db.String(60), nullable=False, unique=True)
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
    def __init__(self, name):
        self.name = name
