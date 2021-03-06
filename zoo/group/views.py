from flask import Blueprint,redirect,request,flash,render_template,url_for,abort,jsonify
from flask_login import login_required,current_user
from zoo.utils.imghelper import allowed_file,upload_file,delete_file
from zoo.configs.default import DefaultConfig
from zoo.user.models import User
from zoo.group.models import Group
from zoo.group.forms import NewGroupForm
from zoo.category.models import Category
from zoo.utils.access_control import check_message


group = Blueprint("group", __name__)


@group.route("/<int:group_id>")
@login_required
@check_message
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
    form.category.choices = [(c.id, c.name) for c in Category.query.all()]
    if form.validate_on_submit():
        group = Group(name=form.name.data, description=form.description.data, creator=current_user, category_id=form.category.data)
        group.members.append(current_user)
        group.set_logo_auto()
        group.save()
        flash("社团创建成功，等待管理员审核")
    else:
        for field,errors in form.errors.items():
            for error in errors:
                flash(u"信息填写有误 '%s'项 - %s" % (getattr(form, field).label.text, error), "error")

    return redirect(url_for('site.index'))


@group.route("/set/logo/<int:group_id>", methods=["POST"])
@login_required
def set_logo(group_id):
    file = request.files['logo']
    group = Group.query.get(group_id)
    if group:
        if file and allowed_file(file.filename):
            if group.set_logo:
                #delete_file(group.logo, DefaultConfig.LOCAL_GROUPLOGO_DIR_1)
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
    flash("社团图标上传成功", "success")
    return redirect(url_for('president.info'))


@group.route("/set/description/<int:group_id>", methods=["POST"])
@login_required
def set_description(group_id):
    group = Group.query.get(group_id)
    if not group:
        abort(404)
    group.description = request.form["description"]
    group.save()
    flash("社团介绍修改成功", "success")
    return redirect(url_for('president.info'))

@group.route("/join/<int:group_id>", methods=['GET'])
@login_required
def join(group_id):

    group = Group.query.get(group_id)
    if not group:
        abort(404)
    group.members.append(current_user)
    group.save()
    flash("已申请加入("+ group.name +"),等待社长审核")
    return redirect(url_for('group.show',group_id=group_id))

@group.route("/leave/<int:group_id>", methods=['GET'])
@login_required
def leave(group_id):
    group = Group.query.get(group_id)
    if not group:
        abort(404)
    group.members.remove(current_user)
    group.save()
    flash("已退出("+ group.name +")")
    return redirect(url_for('group.show',group_id=group_id))

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

@group.route("/admin/m2a/<int:group_id>/<int:user_id>", methods=['POST'])
@login_required
def m2a(group_id, user_id):
    group = Group.query.get(group_id)
    if not group:
        abort(404)
    user = User.query.get(user_id)
    if not user:
        abort(404)
    if not current_user in group.admins and user in group.members.all():
        abort(401)
    if user in group.admins:
        abort(403)
    group.admins.append(user)
    group.save()
    flash("已成功添加 "+user.username+" 为管理员")
    return jsonify(msg="success")

@group.route("/admin/a2m/<int:group_id>/<int:user_id>", methods=['POST'])
@login_required
def a2m(group_id, user_id):
    group = Group.query.get(group_id)
    if not group:
        abort(404)
    user = User.query.get(user_id)
    if not user:
        abort(404)
    if not user in group.admins:
        abort(403)
    if not current_user.id == group.creator_id:
        abort(403)
    group.admins.remove(user)
    group.save()
    flash("管理员删除成功")
    return jsonify(msg="success")

@group.route("/admin/dm/<int:group_id>/<int:user_id>", methods=['POST'])
@login_required
def dm(group_id, user_id):
    group = Group.query.get(group_id)
    if not group:
        abort(404)
    user = User.query.get(user_id)
    if not user:
        abort(404)
    if not current_user in group.admins:
        abort(403)
    group.members.remove(user)
    group.save()
    flash("小组成员删除成功")
    return jsonify(msg="success")

@group.route("/cate/<int:cate_id>")
@login_required
def cate(cate_id):
    if cate_id == 0:
        categories = Category.query.all()
        groups = Group.query.filter(Group.active == 1)
        return render_template("group/groupbycate.html", groups=groups,categories=categories,cate_id=cate_id)
    else:
        categories = Category.query.all()
        groups = Group.query.filter(Group.category_id == cate_id, Group.active == 1)
        return render_template("group/groupbycate.html", groups=groups,categories=categories,cate_id=cate_id)


