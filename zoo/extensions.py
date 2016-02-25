from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from zoo.configs.default import DefaultConfig

#database
db = SQLAlchemy()

#Login
login_manager = LoginManager()



