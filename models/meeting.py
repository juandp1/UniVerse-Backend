import datetime
from config.server_conf import db


class MeetingModel(db.Model):
    __tablename__ = "Meeting"

    # Attributes
    id = db.Column("id_meeting", db.Integer, primary_key=True)
    name = db.Column("name", db.String(60), nullable=False)
    description = db.Column("description", db.String(120), nullable=True)
    place = db.Column("place", db.String(100), nullable=False)
    date = db.Column("date", db.DateTime, nullable=False)
    community_id = db.Column(
        "Community_id_community",
        db.Integer,
        db.ForeignKey("Community.id_community"),
    )
    user_id = db.Column(
        "User_id_user",
        db.Integer,
        db.ForeignKey("User.id_user"),
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
    def __init__(self, name, description, place, date):
        self.name = name
        self.description = description
        self.place = place
        self.date = date
