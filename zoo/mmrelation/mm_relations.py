from zoo.extensions import db
import datetime

groups_members = db.Table(
    'groups_members',
    db.Column('user_id',db.Integer(),db.ForeignKey('users.id')),
    db.Column('group_id',db.Integer(),db.ForeignKey('groups.id')),
)

groups_admin = db.Table(
    'groups_admin',
    db.Column('admin_id',db.Integer(),db.ForeignKey('users.id')),
    db.Column('group_id',db.Integer(),db.ForeignKey('groups.id')),
)

user_followers = db.Table(
    'followers',
    db.Column('follower_id',db.Integer(),db.ForeignKey('users.id')),
    db.Column('followed_id',db.Integer(),db.ForeignKey('users.id')),
    db.Column('created_at', db.DateTime, default=datetime.datetime.now(), nullable=False)
)
