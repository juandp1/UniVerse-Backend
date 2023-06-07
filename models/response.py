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

    # Methods
    def __init__(self, description, question_id, user_id):
        self.description = description
        self.question_id = question_id
        self.user_id = user_id

    def json(self):
        return {
            "num_response": self.num_response,
            "description": self.description,
            "score": self.score,
            "question_id": self.question_id,
            "user_id": self.user_id,
        }

    def save_to_db(self):
        self.updated_at = datetime.datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def update_score(self, increment):
        self.score += increment
        self.save_to_db()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id, is_active=True).first()

    @classmethod
    def find_more_voted(cls):
        return (
            cls.query.filter_by(is_active=True).order_by(cls.score.desc()).first()
        )
