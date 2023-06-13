import datetime
from config.server_conf import db


class LabelHasCommunityModel(db.Model):
    __tablename__ = "Label_has_Community"

    # Attributes
    label_id = db.Column(
        "Label_id_label", db.Integer, db.ForeignKey("Label.id_label"), primary_key=True
    )
    community_id = db.Column(
        "Community_id_community",
        db.Integer,
        db.ForeignKey("Community.id_community"),
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
    def __init__(self, label_id, community_id):
        self.label_id = label_id
        self.community_id = community_id
    
    def json(self):
        return {
            "id_label": self.label_id,
            "id_community": self.community_id,
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
    def num_of_communities_per_label(cls, label_id):
        return cls.query.filter_by(label_id=label_id, is_active=True).count()