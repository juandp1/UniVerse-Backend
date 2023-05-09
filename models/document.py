import datetime
from config.server_conf import db


class DocumentModel(db.Model):
    __tablename__ = "Document"

    # Attributes
    id = db.Column("id_document", db.Integer, primary_key=True)
    name = db.Column("name", db.String(60), nullable=False)
    description = db.Column("description", db.String(120), nullable=True)
    file = db.Column("file", db.LargeBinary, nullable=False)
    type = db.Column("type", db.String(45), nullable=False)
    user_id = db.Column("user_id", db.Integer, db.ForeignKey("User.id_user"))
    administrator_id = db.Column(
        "administrator_id", db.Integer, db.ForeignKey("Administrator.User_id_user")
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
    community_has_document_and_topic = db.relationship(
        "CommunityHasDocumentAndTopicModel",
        backref="community",
    )

    # Methods
    def __init__(self, name, description, file, type, user_id, administrator_id):
        self.name = name
        self.description = description
        self.file = file
        self.type = type
        self.user_id = user_id
        self.administrator_id = administrator_id
