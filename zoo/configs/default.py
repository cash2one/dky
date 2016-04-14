class DefaultConfig(object):
    DEBUG = True
    SECRET_KEY = "youcannotseeme"

    ADMIN_USERNAME = "admin"
    ADMIN_PASSWORD = "123456"
    ADMIN_EMAIL = "admin@163.com"

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@localhost/dky"
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True


    TITLE = "DKY社团活动"
    SITE_NAME = "DKY社团活动发布系统"
    LOCAL_AVATAR_DIR = "./zoo/static/assets/avatar/"
    LOCAL_AVATAR_DIR_1 = "./zoo/static/assets/avatar/upload/"
    LOCAL_AVATAR_URL = "/static/assets/avatar/"
    LOCAL_AVATAR_URL_1 = "/static/assets/avatar/upload/"
    LOCAL_GROUPLOGO_URL = "/static/assets/grouplogo/"
    LOCAL_GROUPLOGO_URL_1 = "/static/assets/grouplogo/upload/"
    LOCAL_GROUPLOGO_DIR = "./zoo/static/assets/grouplogo/"
    LOCAL_GROUPLOGO_DIR_1 = "./zoo/static/assets/grouplogo/upload/"
    UPLOAD_FOLDER = "/static/assets/upload/"
    ALLOWED_EXTENSIONS = set(['png','jpg','jpeg','gif'])

    FOLLOWS_PER_PAGE = 10;
    

    SITE_URL_PREFIX = ""
    USER_URL_PREFIX = "/user"
    GROUP_URL_PREFIX = "/group"
    ACTIVITY_URL_PREFIX = "/activity"
    REPLY_URL_PREFIX = "/reply"
    ADMIN_URL_PREFIX = "/admin"



