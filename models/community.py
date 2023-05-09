import datetime
from config.server_conf import db


class CommunityModel(db.Model):
    __tablename__ = "Community"

    # Attributes
    id = db.Column("id_community", db.Integer, primary_key=True)
    name = db.Column("name", db.String(60), nullable=False)
    description = db.Column("description", db.String(120), nullable=True)
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
    user_belongs_to_community = db.relationship(
        "UserBelongsToCommunityModel", back_populates="community"
    )

    # Methods
    def __init__(self, name, description):
        self.name = name
        self.description = description
