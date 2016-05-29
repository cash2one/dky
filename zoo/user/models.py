from zoo.extensions import db
from zoo.configs.default import DefaultConfig
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.hybrid import hybrid_property
from zoo.mmrelation.mm_relations import user_followers


import os,random,datetime

class User(db.Model, UserMixin):

    __tablename__ = "users"

    id = db.Column(db.Integer(), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.now(), nullable=True)

    username = db.Column(db.String(32), unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    avatar = db.Column(db.String(200), nullable=False)
    set_avatar = db.Column(db.Boolean, default=False, nullable=False)
    #description = db.Column(db.String(255),nullable=True)
    _password = db.Column('password', db.String(160), nullable=False)

    role = db.Column(db.Integer(),default=3, nullable=False)

    new_followers = db.Column(db.Integer(), default=0, nullable=False)
    last_check_follower = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=False)
    followed = db.relationship('User',
                                secondary=user_followers,
                                primaryjoin=(id==user_followers.c.follower_id),
                                secondaryjoin=(id==user_followers.c.followed_id),
                                backref=db.backref('followers', lazy='dynamic'),
                                lazy='dynamic')


    rank = db.Column(db.Integer(), default=0)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        if not password:
            return
        self._password = generate_password_hash(password)


    def check_password(self, password):
        if self.password is None:
            return False
        return check_password_hash(self.password, password)

    """ 随机获得系统头像 """
    def set_avatar_auto(self):
        files = [x for x in os.listdir(DefaultConfig.LOCAL_AVATAR_DIR) if os.path.isfile(os.path.join(DefaultConfig.LOCAL_AVATAR_DIR,x))]
        self.avatar = random.choice(files)


    @classmethod
    def authenticate(cls, login, password, role):
        user = cls.query.filter(db.or_(User.username == login, User.email == login)).first()
        if user:
            authenticated = user.check_password(password)
        else:
            authenticated = False
        return user, authenticated


    """ 创建用户 """
    def save(self):
        db.session.add(self)
        db.session.commit()
        return self


    """ 获得用户小组"""
    def get_groups(self):
        return self.groups.all()

    """ 关注用户 """
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            user.new_followers += 1
            user.save()
            return self

    """ 取消关注用户 """
    def unfollow(self, user):
        if self.is_following(user):
            link = db.session.query(user_followers).filter(user_followers.c.followed_id==user.id, user_followers.c.follower_id == self.id).one()
            print(link.created_at)
            #判断是否为新增粉丝,如果是则用户新增粉丝数-1
            if link.created_at > user.last_check_follower:
                user.new_followers -= 1
            self.followed.remove(user)
            user.save()
            return self

    """ 是否关注用户 """
    def is_following(self, user):
        return self.followed.filter(user_followers.c.followed_id == user.id).count() > 0

   # """ 获取用户所有消息 """
   # def get_messages(self):
   #     messages = self.messages.all()
   #     return messages

   # """ 获取未阅读消息分类片段(用于页头消息提醒显示) """
   # def get_brief_messages(self):
   #     messages = self.messages.filter(Message.readed == False).all()
   #     return messages


    """ 检查粉丝 """
    def check_follower(self):
        self.last_check_follower = datetime.datetime.now()
        self.new_followers = 0
        self.save()