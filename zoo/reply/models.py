from zoo.extensions import db
import datetime


class Reply(db.Model):

    __tablename__ = "replies"

    id = db.Column(db.Integer(), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=False)

    content = db.Column(db.String(255), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", backref=db.backref("replies", lazy='dynamic'), lazy='joined')

    activity_id = db.Column(db.Integer, db.ForeignKey("activities.id",ondelete='CASCADE'), nullable=False)
    activity = db.relationship("Activity", backref=db.backref("replies", lazy='dynamic',cascade="all, delete, delete-orphan", passive_deletes=True), lazy='joined')


    """ 创建小组 """
    def save(self):
        db.session.add(self)
        db.session.commit()
        return self