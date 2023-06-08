import datetime
from config.server_conf import db


class DocumentModel(db.Model):
    __tablename__ = "Document"

    # Attributes
    id = db.Column("id_document", db.Integer, primary_key=True)
    name = db.Column("name", db.String(60), nullable=False)
    description = db.Column("description", db.String(120), nullable=True)
    file = db.Column("file", db.LargeBinary, nullable=False)
    type = db.Column("type", db.String(45), nullable=False)
    user_id = db.Column("user_id", db.Integer, db.ForeignKey("User.id_user"))
    administrator_id = db.Column(
        "administrator_id",
        db.Integer,
        db.ForeignKey("Administrator.User_id_user"),
        nullable=True,
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
    def __init__(self, name, description, file, type, user_id, administrator_id):
        self.name = name
        self.description = description
        self.file = file
        self.type = type
        self.user_id = user_id
        self.administrator_id = administrator_id

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "file": self.file,
            "type": self.type,
            "user_id": self.user_id,
            "administrator_id": self.administrator_id,
        }

    def save_to_db(self):
        DocumentModel.remove_non_accepted_documents()
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
        return cls.query.filter_by(id=id, is_active=True).first()

    @classmethod
    def find_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id, is_active=True).all()

    @classmethod
    def find_by_administrator_id(cls, administrator_id):
        return cls.query.filter_by(
            administrator_id=administrator_id, is_active=True
        ).all()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name, is_active=True).first()

    @classmethod
    def remove_non_accepted_documents(cls):
        cls.query.filter(
            cls.is_active == False,
            cls.created_at < datetime.datetime.utcnow() - datetime.timedelta(days=15),
        ).delete()
        db.session.commit()
