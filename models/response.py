import datetime
from config.server_conf import db


class ResponseModel(db.Model):
    __tablename__ = "Response"

    # Attributes
    num_response = db.Column("num_response", db.Integer, primary_key=True)
    description = db.Column("description", db.String(120), nullable=False)
    score = db.Column("score", db.Integer, nullable=False, default=0)
    question_id = db.Column(
        "Question_id_question",
        db.Integer,
        db.ForeignKey("Question.id_question"),
    )
    user_id = db.Column(
        "User_id_user", db.Integer, db.ForeignKey("User.id_user"), nullable=False
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

    # Methods
    def __init__(self, description, question_id, user_id):
        self.description = description
        self.question_id = question_id
        self.user_id = user_id
