from sqlalchemy import Integer, String, ForeignKey, Column, DateTime
from sqlalchemy.orm import relationship
from flask_restless import APIManager
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import bcrypt
import datetime

db = SQLAlchemy()


class BaseModel:
    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def update():
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Category(BaseModel, db.Model):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    parent_id = Column(Integer, ForeignKey('category.id'), default=-1)
    parent = relationship("Category")
    image = Column(String)

    def __init__(self, name, parent, image=''):
        self.name = name
        self.parent = parent
        self.parent_id = parent.id
        self.image = image

    @staticmethod
    def get_all():
        return Category.metadata.all()


class User(BaseModel, db.Model):
    __tablename__ = "users"

    USER_ADMIN = 1
    USER_CUSTOMER = 2

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), unique=True)
    email = Column(String(1024), unique=True)
    password = Column(String(300))
    role = Column(Integer)
    profile_picture = Column(String(300))
    remember_token = Column(String(100))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    def __init__(self, username, email, password, profile_picture="", role=USER_CUSTOMER):
        self.username = username
        self.email = email
        self.profile_picture = profile_picture
        self.password = bcrypt.encrypt(password)
        self.role = role

    @staticmethod
    def get_all():
        return User.metadata.all()

    def valid_password(self, password):
        return bcrypt.verify(password, self.password)


class RevokedToken(BaseModel, db.Model):
    __tablename__ = "revoked_tokens"

    id = Column(Integer, primary_key=True, autoincrement=True)
    token = Column(String(500))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, token):
        self.token = token

    @staticmethod
    def is_blacklisted(token):
        return RevokedToken.query.filter_by(token=token).first() is not None


def create_models(app, url_prefix="/api"):
    manager = APIManager(app, flask_sqlalchemy_db=db)
    with app.app_context():
        db.create_all()

        manager.create_api(
            Category,
            methods=['GET', 'POST', 'DELETE', 'PUT'],
            url_prefix=url_prefix
        )
