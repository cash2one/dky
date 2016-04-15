from flask import Blueprint,abort,render_template,redirect,url_for
from flask_login import login_required
from zoo.utils.access_control import admin_required
from zoo.group.models import Group
from zoo.extensions import db


admin = Blueprint("admin", __name__)

@admin.route("/verify")
@login_required
@admin_required
def admin_verify():
    groups = Group.query.filter(Group.active == False).all()
    return render_template("admin/verify.html", groups=groups)

@admin.route("/group/agree/<int:group_id>")
@login_required
@admin_required
def group_agree(group_id):
    group = Group.query.get(group_id)
    if group:
        group.active = True
        group.creator.role = 2
        group.save()
        return redirect(url_for('admin.admin_verify'))
    else:
        abort(404)

@admin.route("/group/deny/<int:group_id>")
@login_required
@admin_required
def group_deny(group_id):
    group = Group.query.get(group_id)
    if group and not group.active:
        db.session.delete(group)
        db.session.commit()
        return redirect(url_for('admin.admin_verify'))
    else:
        abort(404)

@admin.route("/group/manage", methods=['GET'])
@login_required
@admin_required
def group_manage():
    groups = Group.query.order_by(Group.created_at).all()
    return render_template('admin/group.html', groups=groups)


