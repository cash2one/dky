from zoo.extensions import db
from zoo.user.models import User
from zoo.mmrelation.mm_relations import activity_users
import datetime


class Activity(db.Model):

    __tablename__ = "activities"

    id = db.Column(db.Integer(), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.now(), nullable=True)

    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)

    address = db.Column(db.String(200), nullable=False)

    title = db.Column(db.String(100), nullable=False)
    count = db.Column(db.Integer(), default=20, nullable=False)
    content = db.Column(db.String(255), nullable=True)


    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", backref=db.backref("c_activities", lazy='dynamic'), lazy='joined')

    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"))
    group = db.relationship("Group", backref=db.backref("activities", lazy='dynamic'), lazy='joined')

    users = db.relationship("User", secondary=activity_users, backref=db.backref("activities", lazy='dynamic'), lazy='dynamic')

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self