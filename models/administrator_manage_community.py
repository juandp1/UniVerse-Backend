import datetime
from config.server_conf import db


class AdministratorManageCommunityModel(db.Model):
    __tablename__ = "Administrator_manage_Community"

    # Attributes
    admin_id = db.Column(
        "Administrator_User_id_user",
        db.Integer,
        db.ForeignKey("Administrator.User_id_user"),
        primary_key=True,
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
    def __init__(self, admin_id, community_id):
        self.admin_id = admin_id
        self.community_id = community_id
