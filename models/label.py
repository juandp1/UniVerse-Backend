import datetime
from config.server_conf import db


class LabelModel(db.Model):
    __tablename__ = "Label"

    # Attributes
    id = db.Column("id_label", db.Integer, primary_key=True)
    name = db.Column("name", db.String(60), nullable=False)
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
    label_has_community = db.relationship(
        "LabelHasCommunityModel", back_populates="label"
    )
    user_follows_label = db.relationship(
        "UserFollowsLabelModel", back_populates="label"
    )

    # Methods
    def __init__(self, name):
        self.name = name
