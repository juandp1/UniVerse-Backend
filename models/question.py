import datetime
from config.server_conf import db


class QuestionModel(db.Model):
    __tablename__ = "Question"

    # Attributes
    id = db.Column("id_question", db.Integer, primary_key=True)
    title = db.Column("title", db.String(60), nullable=False)
    description = db.Column("description", db.String(120), nullable=True)
    score = db.Column("score", db.Integer, nullable=False, default=0)
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
    topic_id = db.Column(
        "Topic_id_topic",
        db.Integer,
        db.ForeignKey("Topic.id_topic"),
        nullable=False,
    )
    community_id = db.Column(
        "Community_id_community",
        db.Integer,
        db.ForeignKey("Community.id_community"),
        nullable=False,
    )
    user_id = db.Column(
        "User_id_user", db.Integer, db.ForeignKey("User.id_user"), nullable=False
    )

    # Methods
    def __init__(self, title, description, topic_id, community_id, user_id):
        self.title = title
        self.description = description
        self.topic_id = topic_id
        self.community_id = community_id
        self.user_id = user_id
