import datetime
from config.server_conf import db


class UserBelongsToCommunityModel(db.Model):
    __tablename__ = "User_belongs_to_Community"

    # Attributes
    user_id = db.Column(
        "User_id_user", db.Integer, db.ForeignKey("User.id_user"), primary_key=True
    )
    community_id = db.Column(
        "Community_id_community",
        db.Integer,
        db.ForeignKey("Community.id_community"),
        primary_key=True,
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
    def __init__(self, user_id, community_id):
        self.user_id = user_id
        self.community_id = community_id
