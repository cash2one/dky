from flask import Blueprint,redirect,request,flash,render_template,url_for,abort,jsonify
from flask_login import login_required,current_user
from zoo.utils.imghelper import allowed_file,upload_file,delete_file
from zoo.configs.default import DefaultConfig

from zoo.group.models import Group
from zoo.group.forms import NewGroupForm


group = Blueprint("group", __name__)


@group.route("/<int:group_id>")
@login_required
def show(group_id):
    group = Group.query.get(group_id)
    return render_template("group/show.html", group=group)


@group.route("/admin/<int:group_id>")
@login_required
def admin(group_id):
    group = Group.query.get(group_id)
    if not group:
        abort(404)
    return render_template("group/admin.html", group=group)


@group.route("/new", methods=["POST"])
@login_required
def new():
    form = NewGroupForm()

    if form.validate_on_submit():
        group = Group(name=form.name.data, description=form.description.data, creator_id=current_user.id)
        group.admins.append(current_user)
        group.members.append(current_user)
        group.set_logo_auto()
        group.save()
        flash("小组创建成功")
    else:
        for field,errors in form.errors.items():
            for error in errors:
                flash(u"信息填写有误 '%s'项 - %s" % (getattr(form, field).label.text, error), "error")

    return redirect(url_for('user.group_dashboard'))

@group.route("/join/<int:group_id>", methods=["POST"])
@login_required
def join(group_id):
    group = Group.query.get(group_id)
    if not group:
        abort(404)



@group.route("/set/logo/<int:group_id>", methods=["POST"])
@login_required
def set_logo(group_id):
    file = request.files['logo']
    group = Group.query.get(group_id)
    if group:
        if file and allowed_file(file.filename):
            if group.set_logo:
                delete_file(group.logo, DefaultConfig.LOCAL_GROUPLOGO_DIR_1)
                upload_file(file, DefaultConfig.LOCAL_GROUPLOGO_DIR_1)
                group.logo = file.filename
                group.save()
            else:
                upload_file(file, DefaultConfig.LOCAL_GROUPLOGO_DIR_1)
                group.logo = file.filename
                group.set_logo = True
                group.save()

        else:
            flash("图标图片只能是jpg/jpeg/png/gif格式，且大小不能超过2M")
    else:
        abort(404)
    flash("小组图标上传成功", "success")
    return redirect(url_for('group.admin', group_id=group_id))


@group.route("/set/description/<int:group_id>", methods=["POST"])
@login_required
def set_description(group_id):
    group = Group.query.get(group_id)
    if not group:
        abort(404)
    group.description = request.form["description"]
    group.save()
    flash("小组介绍修改成功", "success")
    return redirect(url_for('group.admin', group_id=group_id))

"""  AJAX  """
@group.route("/set/private/<int:group_id>", methods=['POST'])
@login_required
def set_private(group_id):
    group = Group.query.get(group_id)
    if not group:
        abort(404)
    group.private = request.form["private"]
    group.save()
    return jsonify(data=group.private, msg="设置成功")

