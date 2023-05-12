import datetime
from config.server_conf import db
from models.administrator import AdministratorModel


class AdministratorManageCommunityModel(db.Model):
    __tablename__ = "Administrator_manage_Community"

    # Attributes
    admin_id = db.Column(
        "Administrator_User_id_user",
        db.Integer,
        db.ForeignKey("Administrator.User_id_user"),
        primary_key=True,
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
    def __init__(self, admin_id, community_id):
        self.admin_id = admin_id
        self.community_id = community_id

    def json(self):
        return {
            "admin_id": self.admin_id,
            "community_id": self.community_id,
        }

    @staticmethod
    def user_is_admin_of_community(admin_id, community_id):
        return (
            AdministratorManageCommunityModel.query.filter_by(
                admin_id=admin_id, community_id=community_id, is_active=True
            ).one_or_none()
            is not None
        )

    @staticmethod
    def add_admin_to_community(admin_id, community_id):
        admin = AdministratorModel.query.filter_by(id=admin_id).one_or_none()
        if admin is None:
            # Create admin
            admin = AdministratorModel(admin_id)
            db.session.add(admin)
            db.session.commit()

        if admin.is_active is False:
            # Reactivate admin
            admin.is_active = True
            admin.updated_at = datetime.datetime.utcnow()
            db.session.add(admin)
            db.session.commit()

        # Add admin to community
        admin_manage_community = AdministratorManageCommunityModel(
            admin_id, community_id
        )
        db.session.add(admin_manage_community)
        db.session.commit()
