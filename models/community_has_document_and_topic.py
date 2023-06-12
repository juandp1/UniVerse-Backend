import datetime
from config.server_conf import db


class CommunityHasDocumentAndTopicModel(db.Model):
    __tablename__ = "Community_has_Document_and_Topic"

    # Attributes
    community_id = db.Column(
        "Community_id_community",
        db.Integer,
        db.ForeignKey("Community.id_community"),
        primary_key=True,
    )
    document_id = db.Column(
        "Document_id_document",
        db.Integer,
        db.ForeignKey("Document.id_document"),
        primary_key=True,
    )
    topic_id = db.Column(
        "Topic_id_topic",
        db.Integer,
        db.ForeignKey("Topic.id_topic"),
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
    def __init__(self, community_id, document_id, topic_id):
        self.community_id = community_id
        self.document_id = document_id
        self.topic_id = topic_id

    def json(self):
        return {
            "community_id": self.community_id,
            "document_id": self.document_id,
            "topic_id": self.topic_id,
        }

    def save_to_db(self):
        self.updated_at = datetime.datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        self.is_active = False
        self.updated_at = datetime.datetime.utcnow()
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_community_id(cls, community_id):
        return cls.query.filter_by(community_id=community_id, is_active=True).first()

    @classmethod
    def delete_documents_by_community_id(cls, community_id):
        cls.query.filter_by(community_id=community_id, is_active=True).delete()
        db.session.commit()

    @classmethod
    def delete_documents_by_topic_id(cls, topic_id):
        cls.query.filter_by(topic_id=topic_id, is_active=True).delete()
        db.session.commit()
