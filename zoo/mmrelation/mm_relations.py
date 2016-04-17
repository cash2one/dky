from zoo.extensions import db
import datetime

groups_members = db.Table(
    'groups_members',
    db.Column('user_id',db.Integer(),db.ForeignKey('users.id')),
    db.Column('group_id',db.Integer(),db.ForeignKey('groups.id')),
    db.Column('verify', db.Boolean, default=False, nullable=False)
)

user_followers = db.Table(
    'followers',
    db.Column('follower_id',db.Integer(),db.ForeignKey('users.id')),
    db.Column('followed_id',db.Integer(),db.ForeignKey('users.id'))
)

activity_users = db.Table(
    'activity_users',
    db.Column('activity_id',db.Integer(),db.ForeignKey('activities.id')),
    db.Column('user_id',db.Integer(),db.ForeignKey('users.id'))
)
