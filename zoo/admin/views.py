from flask import Blueprint,abort,render_template,redirect,url_for
from flask_login import login_required
from zoo.utils.access_control import admin_required
from zoo.group.models import Group
from zoo.activity.models import Activity
from zoo.category.models import Category
from zoo.extensions import db
from zoo.message.models import Message
from zoo.user.models import User
from sqlalchemy import or_


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
        group.join(group.creator.id)
        message = Message(user=group.creator, content="你创建的小组"+group.name+"已经通过审核！")
        message.save()
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

@admin.route("/acivity/manage", methods=['GET'])
@login_required
@admin_required
def activities_manage():
    activities = Activity.query.all()
    return render_template('admin/activities.html', activities=activities)

@admin.route("/category/manage", methods=['GET'])
@login_required
@admin_required
def category_manage():
    categories = Category.query.all()
    return render_template('admin/category.html', categories=categories)

@admin.route("/user/manage", methods=['GET'])
@login_required
@admin_required
def user_manage():
    users = User.query.filter(or_(User.role == 2, User.role == 3))
    return render_template('admin/user.html', users=users)


