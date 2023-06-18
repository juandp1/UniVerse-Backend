from datetime import datetime, timezone
from config.server_conf import db
from flask_jwt_extended import get_jwt_identity, jwt_required


class TokenBlockListModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)
    type = db.Column(db.String(16), nullable=False)
    user_id = db.Column(
        db.ForeignKey("User.id_user", ondelete="CASCADE"),
        nullable=False,
        default=lambda: TokenBlockListModel.get_current_user().id_user,
    )
    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.now(timezone.utc)
    )

    def __init__(self, jti, type, created_at, user_id):
        self.jti = jti
        self.type = type
        self.created_at = created_at
        self.user_id = user_id

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    @jwt_required()
    def get_current_user():
        return get_jwt_identity()
