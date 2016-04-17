from flask import Blueprint,abort,render_template,redirect,url_for,flash,request
from flask_login import login_required,current_user
from zoo.utils.access_control import president_required
from zoo.activity.models import Activity
from zoo.user.models import User
import datetime


president = Blueprint("president", __name__)

@president.route("/verify")
@login_required
@president_required
def verify():
    group = current_user.owned_group
    members = group.unverify_members.all()

    return render_template("president/verify.html", members=members)

@president.route("/members")
@login_required
@president_required
def member_manage():
    group = current_user.owned_group
    members = group.members.filter().all()

    return render_template("president/members.html", members=members)

@president.route("/join/agree/<int:user_id>")
@login_required
@president_required
def join_agree(user_id):
    group = current_user.owned_group
    group.join(user_id)
    flash("小组成员审核通过", "success")
    return redirect(url_for("president.verify"))

@president.route("/join/<int:user_id>")
@login_required
@president_required
def join_deny(user_id):
    group = current_user.owned_group
    group.delete(user_id)
    return redirect(url_for("president.verify"))

@president.route("/activities")
@login_required
@president_required
def activities():
    activities = current_user.owned_group.activities.all()
    return render_template("president/activities.html", activities=activities)

@president.route("/activity/new", methods=['GET','POST'])
@login_required
@president_required
def new_activity():
    title = request.form['title']
    address = request.form['address']
    start_time = datetime.datetime.strptime(request.form['start-time'], "%Y-%m-%d %H:%M")
    end_time = datetime.datetime.strptime(request.form['end-time'], "%Y-%m-%d %H:%M")
    count = int(request.form['count'])
    content = request.form['content']
    activity = Activity(title=title, address=address, start_time=start_time, end_time=end_time,count=count,content=content)
    activity.group = current_user.owned_group
    activity.user = current_user
    activity.save()
    flash("活动发布成功", "success")
    return redirect(url_for("president.activities"))

@president.route("/info", methods=['GET', 'POST'])
@login_required
@president_required
def info():
    group = current_user.owned_group
    return render_template("president/info.html", group=group)

@president.route("/kickout/<int:user_id>", methods=['GET'])
@login_required
@president_required
def kickout(user_id):
    user = User.query.get(user_id)
    if not user:
        abort(404)
    else:
        current_user.owned_group.members.remove(user)
        current_user.save()
        return redirect(url_for("president.member_manage"))
