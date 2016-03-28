from flask import Blueprint
from flask_login import login_required
from zoo.activity.models import Activity

activity = Blueprint("activity", __name__)