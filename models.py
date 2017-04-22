import json

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Base(db.Model):

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime,
                             default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,
                              default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())


class User(Base):
    __tablename__ = 'user'
    name = db.Column(db.String(128), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<User %r>' % self.name


class Cookie(Base):
    __tablename__ = 'cookie'
    cookie = db.Column(db.Integer, unique=True, nullable=False)

    def __init__(self, cookie):
        self.cookie = cookie

    def __repr__(self):
        return '<Cookie %r>' % self.cookie


class UserCookie(Base):
    __tablename__ = 'usercookie'
    user = db.Column(db.String(128), unique=True, nullable=False)
    cookie = db.Column(db.Integer, unique=True, nullable=False)
    actions = db.relationship("Action", back_populates="usercookie")

    def __init__(self, user, cookie):
        self.user = user
        self.cookie = cookie

    def __repr__(self):
        return '<User {}, Cookie {}>'.format(self.user, self.cookie)


class Action(Base):
    __tablename__ = 'action'
    action = db.Column(db.String(128), nullable=False)
    details = db.Column(db.String(128), nullable=False)
    usercookie_id = db.Column(db.Integer, db.ForeignKey('usercookie.id'))
    usercookie = db.relationship("UserCookie", back_populates='actions')

    def __init__(self, usercookie_id, action, details):
        self.usercookie_id = usercookie_id
        self.action = action
        self.details = details

    # def __repr__(self):
    #     return '<UCID {}, Action {}, Details {}'.format(self.usercookie_id,
    #                                                     self.action,
    #                                                     self.details)

    # def __repr__(self):
    #     return '{{"id": "{}", "timestamp": "{}", "action": "{}", "details": "{}"}}'.format(
    #         self.id,
    #         self.date_created,
    #         self.action,
    #         self.details)

    def __repr__(self):
        return json.dumps({"id": self.id,
                           "timestamp": self.date_created.strftime('%Y-%m-%d_%H:%M:%S'),
                           "action": self.action,
                           "details": self.details})
