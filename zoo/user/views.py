from flask import Blueprint,flash,request,render_template, redirect,url_for, abort
from flask_login import login_required, current_user
from zoo.utils.imghelper import allowed_file,upload_file,delete_file
from zoo.group.forms import NewGroupForm
from zoo.user.models import User
from flask.json import jsonify
from zoo.configs.default import DefaultConfig




user = Blueprint("user", __name__)


@user.route("/<int:user_id>")
@login_required
def homepage(user_id):
    user = User.query.get(user_id)
    if not user:
        abort(404)
    return render_template("user/homepage.html",user=user)


@user.route("/group/dashboard")
@login_required
def group_dashboard():
    form = NewGroupForm()
    return render_template("user/group_dashboard.html",form=form)


@user.route("/setting/profile")
@login_required
def setting_profile():
    return render_template("user/setting_profile.html")


@user.route("/setting/appearance")
@login_required
def setting_appearance():
    return render_template("user/setting.html")


@user.route("/setting/notice")
@login_required
def setting_notice():
    return render_template("user/setting.html")

@user.route("/setting/password",methods=['POST'])
@login_required
def password_setting():
    old_pwd = request.form["old_password"]
    new_pws = request.form["new_password"]
    if current_user.check_password(old_pwd):
        current_user.password = new_pws
        current_user.save()
        flash("密码修改成功", "success")
    else:
        flash("密码修改失败", "error")
    return redirect(url_for(request.args["next"]))


@user.route("/setting/avatar",methods=['POST'])
@login_required
def avatar_setting():
    file = request.files['avatar']
    if file and allowed_file(file.filename):
        if current_user.set_avatar:
            delete_file(current_user.avatar, DefaultConfig.LOCAL_AVATAR_DIR_1)
            upload_file(file, DefaultConfig.LOCAL_AVATAR_DIR_1)
            current_user.avatar = file.filename
            current_user.save()
        else:
            upload_file(file, DefaultConfig.LOCAL_AVATAR_DIR_1)
            current_user.avatar = file.filename
            current_user.set_avatar = True
            current_user.save()

    else:
        flash("头像图片只能是jpg/jpeg/png/gif格式，且大小不能超过2M")
    flash("头像上传成功", "success")
    return redirect(url_for(request.args["next"]))


@user.route("/follow/<int:user_id>", methods=["GET", "POST"])
@login_required
def follow(user_id):
    user = User.query.get(user_id)
    if not user:
        abort(404)
    if request.method == "GET":
        if user_id == current_user.id:
             user.check_follower()
        return render_template("user/follow.html", user=user, followers=user.followers.all())
    else:
        if user.id == current_user.id:
            return jsonify(status=500, message="关注自己？！别自恋了好伐？")
        current_user.follow(user)
        new_url = url_for('user.unfollow', user_id = user.id)
        return jsonify(data=user.id, status=200, message="取消关注", newurl=new_url)


@user.route("/unfollowed/<int:user_id>", methods=["POST"])
@login_required
def unfollow(user_id):
    user = User.query.get(user_id)
    if not user:
        abort(404)
    current_user.unfollow(user)
    new_url = url_for('user.follow', user_id = user.id)
    return jsonify(data=user.id, status=200, message="关注", newurl=new_url)