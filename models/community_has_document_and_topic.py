import datetime
from config.server_conf import db


class CommunityHasDocumentAndTopicModel(db.Model):
    __tablename__ = "Community_has_Document_and_Topic"

    # Attributes
    table_id = db.Column(
        "id_community_has_document_and_topic",
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )

    community_id = db.Column(
        "Community_id_community",
        db.Integer,
        db.ForeignKey("Community.id_community", ondelete="CASCADE"),
        primary_key=True,
        nullable=True,
    )
    document_id = db.Column(
        "Document_id_document",
        db.Integer,
        db.ForeignKey("Document.id_document", ondelete="CASCADE"),
        nullable=True,
    )
    topic_id = db.Column(
        "Topic_id_topic",
        db.Integer,
        db.ForeignKey("Topic.id_topic", ondelete="CASCADE"),
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
    def __init__(self, community_id, topic_id, document_id=None):
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

    @classmethod
    def find_topics_of_community(cls, community_id):
        return cls.query.filter_by(community_id=community_id, is_active=True).group_by(
            cls.topic_id
        )

    @classmethod
    def num_of_topics_per_community(cls, community_id):
        return cls.query.filter_by(community_id=community_id, is_active=True).count()

    @classmethod
    def get_propose_relations_by_comm_id(cls, community_id):
        return cls.query.filter_by(community_id=community_id, is_active=False).all()

    @classmethod
    def accept_document(cls, document_id):
        cls.query.filter_by(document_id=document_id, is_active=False).update(
            {"is_active": True}
        )
        db.session.commit()

    @classmethod
    def reject_document(cls, document_id):
        cls.query.filter_by(document_id=document_id, is_active=False).delete()
        db.session.commit()
