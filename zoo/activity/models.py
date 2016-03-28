from zoo.extensions import db
import datetime


class Activity(db.Model):

    __tablename__ = "activities"

    id = db.Column(db.Integer(), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.now(), nullable=True)

    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)

    address = db.Column(db.String(200), nullable=False)

    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", backref=db.backref("c_activities", lazy='dynamic'), lazy='joined')

    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"), nullable=False)
    group = db.relationship("Group", backref=db.backref("activities", lazy='dynamic'), lazy='joined')