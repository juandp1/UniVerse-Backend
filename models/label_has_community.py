import datetime
from config.server_conf import db


class LabelHasCommunity(db.Model):
    __tablename__ = "Label_has_Community"

    # Attributes
    user_id = db.Column(
        "Label_id_label", db.Integer, db.ForeignKey("Label.id_label"), primary_key=True
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

    # Relationships
    label = db.relationship("LabelModel", back_populates="label_has_community")
    community = db.relationship(
        "CommunityModel", back_populates="user_belongs_to_community"
    )

    # Methods
    def __init__(self, user_id, community_id):
        self.user_id = user_id
        self.community_id = community_id
