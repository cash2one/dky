from flask import Blueprint,abort,render_template,redirect,url_for
from flask_login import login_required
from zoo.utils.access_control import president_required
from zoo.group.models import Group
from zoo.extensions import db


president = Blueprint("president", __name__)

@president.route("/verify")
@login_required
@president_required
def president_verify():

    return render_template("president/verify.html")
