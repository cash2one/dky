from sqlalchemy import Integer
from sqlalchemy.dialects import postgresql
from zoo.extensions import db
from zoo.configs.default import DefaultConfig

import datetime


class Message(db.Model):

    __tablename__ = "messages"

    created_at = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=False)

    from_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    to_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)

    ref = db.Column(db.Integer(), nullable=True, primary_key=True)

    type = db.Column(db.SmallInteger, nullable=False, primary_key=True)

    subject = db.Column(db.String(255))

    readed = db.Column(db.Boolean, default=False, nullable=False)


    def save(self):
        db.session.add(self)
        db.session.commit()
        return self




