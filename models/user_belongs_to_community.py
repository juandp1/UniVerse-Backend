import datetime
from config.server_conf import db


class UserBelongsToCommunityModel(db.Model):
    __tablename__ = "User_belongs_to_Community"

    # Attributes
    user_id = db.Column(
        "User_id_user",
        db.Integer,
        db.ForeignKey("User.id_user", ondelete="CASCADE"),
        primary_key=True,
    )
    community_id = db.Column(
        "Community_id_community",
        db.Integer,
        db.ForeignKey("Community.id_community", ondelete="CASCADE"),
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
    def __init__(self, user_id, community_id):
        self.user_id = user_id
        self.community_id = community_id

    def json(self):
        return {
            "user_id": self.user_id,
            "community_id": self.community_id,
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
    def find_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id, is_active=True).all()

    @classmethod
    def find_by_community_id(cls, community_id):
        return cls.query.filter_by(community_id=community_id, is_active=True).all()

    @classmethod
    def find_by_user_id_and_community_id(cls, user_id, community_id):
        return cls.query.filter_by(
            user_id=user_id, community_id=community_id, is_active=True
        ).one_or_none()

    @classmethod
    def num_of_users_per_community(
        cls,
    ):
        res_query = cls.query.filter_by(is_active=True).all()
        res = {}
        for each in res_query:
            id_com = each.community_id
            if id_com not in res:
                res[id_com] = 1
            else:
                res[id_com] += 1
        return res

    @classmethod
    def num_of_users_per_community_id(cls, community_id):
        return cls.query.filter_by(community_id=community_id, is_active=True).count()
