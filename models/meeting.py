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
        db.ForeignKey("Community.id_community", ondelete="CASCADE"),
    )
    user_id = db.Column(
        "User_id_user",
        db.Integer,
        db.ForeignKey("User.id_user", ondelete="CASCADE"),
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
    def __init__(self, name, description, place, date, community_id, user_id):
        self.name = name
        self.description = description
        self.place = place
        self.date = date
        self.community_id = community_id
        self.user_id = user_id

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "place": self.place,
            "date": self.date.strftime("%Y-%m-%d %H:%M:%S"),
            "community_id": self.community_id,
            "author_id": self.user_id,
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
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id, is_active=True).one_or_none()

    @classmethod
    def find_by_comm_id(cls, comm_id):
        return cls.query.filter_by(community_id=comm_id, is_active=True).all()

    @classmethod
    def find_by_author_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id, is_active=True).one_or_none()

    @classmethod
    def find_by_dates(cls, comm_id, initial_date, final_date):
        return (
            cls.query.filter_by(community_id=comm_id, is_active=True)
            .filter(
                cls.date.between(
                    datetime.datetime.strptime(initial_date, "%Y-%m-%d %H:%M:%S"),
                    datetime.datetime.strptime(final_date, "%Y-%m-%d %H:%M:%S"),
                )
            )
            .all()
        )

    @classmethod
    def next_meeting_of_community(cls, comm_id):
        return (
            cls.query.filter_by(is_active=True)
            .filter(cls.community_id == comm_id)
            .filter(cls.date >= datetime.datetime.utcnow())
            .order_by(cls.date.asc())
            .first()
        )
