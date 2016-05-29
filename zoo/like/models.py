from zoo.extensions import db

class Like(db.Model):
    __tablename__ = "like"
    id = db.Column(db.Integer(), primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", backref=db.backref("likes", lazy='dynamic'), lazy='joined')

    activity_id = db.Column(db.Integer, db.ForeignKey("activities.id"))
    activity = db.relationship("Activity", backref=db.backref("likes", lazy='dynamic'), lazy='joined')

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()