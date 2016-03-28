from flask import Blueprint
from zoo.reply.models import Reply
from flask_login import login_required

reply = Blueprint("reply", __name__)