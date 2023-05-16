import datetime
from config.server_conf import db


class TopicModel(db.Model):
    __tablename__ = "Topic"

    # Attributes
    id = db.Column("id_topic", db.Integer, primary_key=True)
    name = db.Column("name", db.String(45), nullable=False, unique=True)
    administrator_id = db.Column(
        "Administrator_User_id_user",
        db.Integer,
        db.ForeignKey("Administrator.User_id_user"),
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
    def __init__(self, name, administrator_id):
        self.name = name
        self.administrator_id = administrator_id

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "administrator_id": self.administrator_id,
        }

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id, is_active=True).one_or_none()
