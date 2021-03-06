import json
from sqlalchemy import Column, String, Integer, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from app import db
from passlib.hash import pbkdf2_sha256 as sha256


class UserModel(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(120), unique=True, nullable=True)
    password = Column(String(120), nullable=False)
    phone_number = Column(String(20), unique=True, nullable=False)
    active = Column(Boolean, nullable=False)
    updated_at = Column(DateTime)
    first_name = Column(String(120))
    last_name = Column(String(120))
    birthday = Column(String(120))
    gender = Column(Enum('female', 'male', name='gender_enum', create_type=False))
    birthday_access = Column(Enum('public', 'friends', 'hidden', name='birthday_access', create_type=False))
    avatar = Column(String(1024))

    related_users = relationship('RelatedUserModel', backref='users', lazy=True)
    # related_user = relationship('RelatedUserModel', primaryjoin="related_users.related_user_id == users.id", lazy=True)
    favorites = relationship('FavoriteModel', backref='users', lazy=True)

    # def __repr__(self):
    #     return '<username %r>' % self.phone_number

    def deserialize(self, payload):
        self.__dict__.update(payload)

    def serialize(self):
        # return {c.username: getattr(self, c.username) for c in self.__table__.columns}
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def add(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)

    @staticmethod
    def get_all():
        result = db.session.query(UserModel).all()
        return result

    @staticmethod
    def find_by_username(username):
        result = db.session.query(UserModel).filter(UserModel.username == username).first()
        return result

    @staticmethod
    def find_by_phone_number(mobile):
        result = db.session.query(UserModel).filter(UserModel.phone_number == mobile).first()
        return result

    @staticmethod
    def find_by_id(user_id):
        result = db.session.query(UserModel).filter(UserModel.id == user_id).first()
        return result


class RevokedTokenModel(db.Model):
    __tablename__ = 'revoked_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    jti = db.Column(db.String(120))

    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti=jti).first()
        return bool(query)
