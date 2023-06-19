import datetime
from config.server_conf import db
from models.user_belongs_to_community import UserBelongsToCommunityModel


class CommunityModel(db.Model):
    __tablename__ = "Community"

    # Attributes
    id = db.Column("id_community", db.Integer, primary_key=True)
    name = db.Column("name", db.String(60), nullable=False, unique=True)
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

    # Methods
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
        }

    def delete_from_db(self):
        self.is_active = False
        self.updated_at = datetime.datetime.utcnow()
        db.session.delete(self)
        db.session.commit()

    def save_to_db(self):
        self.updated_at = datetime.datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id, is_active=True).first()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name, is_active=True).first()

    @classmethod
    def find_by_similar_name(cls, name):
        return cls.query.filter(
            cls.name.like("%" + name + "%"), cls.is_active == True
        ).all()

    @classmethod
    def is_member(cls, id_user, id_community):
        return (
            UserBelongsToCommunityModel.query.filter_by(
                user_id=id_user, community_id=id_community, is_active=True
            ).one_or_none()
            is not None
        )

    @classmethod
    def number_of_users(id_community):
        users = UserBelongsToCommunityModel.find_by_community_id(
            community_id=id_community
        )
        users_as_list = []
        for user in users:
            users_as_list.append(user.json())
        return len(users_as_list)
