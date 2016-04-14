from flask import Blueprint
from flask import render_template
from flask_login import login_required
from zoo.utils.access_control import admin_required
from zoo.group.models import Group


admin = Blueprint("admin", __name__)

@admin.route("/group")
@login_required
@admin_required
def admin_verify():
    groups = Group.query.all()
    return render_template("admin/verify.html", groups=groups)


