from zoo.extensions import db
from zoo.mmrelation.mm_relations import groups_members
from zoo.configs.default import DefaultConfig
from sqlalchemy import update,delete,create_engine
import os, datetime, random


class Group(db.Model):

    __tablename__ = "groups"

    id = db.Column(db.Integer(), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.now(), nullable=True)

    active = db.Column(db.Boolean, default=False, nullable=False)

    name = db.Column(db.String(40), unique=True, nullable=False)
    description = db.Column(db.String(200), nullable=True)
    logo = db.Column(db.String(200), nullable=False)
    #banner = db.Column(db.String(200), nullable=False)
    set_logo = db.Column(db.Boolean, default=False, nullable=False)

    creator_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    creator = db.relationship("User", backref=db.backref('owned_group',uselist=False, lazy='joined'), lazy='joined')

    members = db.relationship("User", secondary=groups_members,primaryjoin=id==groups_members.c.group_id, secondaryjoin="and_(groups_members.c.user_id == User.id, groups_members.c.verify==True)", backref=db.backref("groups", lazy='dynamic'), lazy='dynamic')
    unverify_members = db.relationship("User", secondary=groups_members, primaryjoin=id==groups_members.c.group_id, secondaryjoin="and_(groups_members.c.user_id == User.id, groups_members.c.verify==False)",lazy='dynamic')




    """ 设置随机小组图标 """
    def set_logo_auto(self):
        files = [x for x in os.listdir(DefaultConfig.LOCAL_GROUPLOGO_DIR) if os.path.isfile(x) ]
        self.logo = random.choice(files)

    """ 创建小组 """
    def save(self):
        db.session.add(self)
        db.session.commit()
        return self


    """加入成员"""
    def join(self, user_id):
        u = update(groups_members).where(groups_members.c.group_id == self.id).where(groups_members.c.user_id == user_id).values(verify=True)
        engine = create_engine(DefaultConfig.SQLALCHEMY_DATABASE_URI)
        connection = engine.connect()
        connection.execute(u)
        connection.close()

    """删除成员"""
    def delete(self, user_id):
        groups_members.delete(groups_members.c.group_id==self.id, groups_members.c.user_id==user_id)

    """ 序列化 """
    @property
    def serialize(self):
        return {
            'id': self.id,
            'private': self.private,
            'name': self.name
        }
