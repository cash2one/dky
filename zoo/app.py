from flask import Flask
from sqlalchemy import event
from zoo.extensions import db, login_manager

from zoo.site.views import site
from zoo.user.views import user
from zoo.group.views import group
from zoo.activity.views import activity
from zoo.reply.views import reply

from zoo.user.models import User



def create_app(config=None):
    """ create the app """
    app = Flask("zoo")

    app.config.from_object('zoo.configs.default.DefaultConfig')
    app.config.from_object(config)

    configure_blueprints(app)
    configure_extensions(app)
    configure_context_processors(app)

    return app

def configure_blueprints(app):
    app.register_blueprint(site, url_prefix=app.config["SITE_URL_PREFIX"])
    app.register_blueprint(user, url_prefix=app.config["USER_URL_PREFIX"])
    app.register_blueprint(group, url_prefix=app.config["GROUP_URL_PREFIX"])
    app.register_blueprint(activity, url_prefix=app.config["ACTIVITY_URL_PREFIX"])
    app.register_blueprint(reply, url_prefix=app.config["REPLY_URL_PREFIX"])

def configure_extensions(app):

    db.init_app(app)
    #绑定orm事件

    with app.app_context():
        db.create_all()

    @login_manager.user_loader
    def load_user(user_id):
        user_instance = User.query.filter_by(id=user_id).first()
        if user_instance:
            print(user_instance)
            return user_instance
        else:
            return None
    login_manager.init_app(app)
    login_manager.login_view = "site.login"
    login_manager.login_message = u"检测到您还没有登录账户，请先登录。"




def configure_context_processors(app):

    @app.context_processor
    def user_avatar_processor():
        def render_user_avatar(user):
            if user.set_avatar:
                return app.config["LOCAL_AVATAR_URL_1"] + user.avatar
            else:
                return app.config["LOCAL_AVATAR_URL"] + user.avatar
        return dict(render_user_avatar = render_user_avatar)

    @app.context_processor
    def group_logo_processor():
        def render_group_logo(group):
            if group.set_logo:
                return app.config["LOCAL_GROUPLOGO_URL_1"] + group.logo
            else:
                return app.config["LOCAL_GROUPLOGO_URL"] + group.logo
        return dict(render_group_logo = render_group_logo)
