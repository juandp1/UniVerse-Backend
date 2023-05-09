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
    administrator_manage_community = db.relationship(
        "AdministratorManageCommunityModel",
        backref="administrator",
    )
    community_has_document_and_topic = db.relationship(
        "CommunityHasDocumentAndTopicModel",
        backref="community",
    )
    label_has_community = db.relationship(
        "LabelHasCommunityModel",
        back_populates="community",
    )
    meeting = db.relationship("MeetingModel", back_populates="community")
    question = db.relationship("QuestionModel", back_populates="community")
    user_belongs_to_community = db.relationship(
        "UserBelongsToCommunityModel", back_populates="user"
    )

    # Methods
    def __init__(self, name, description):
        self.name = name
        self.description = description
