from flask import Blueprint, abort,render_template,flash,redirect,url_for,request
from flask_login import login_required,current_user
from zoo.activity.models import Activity
import datetime

activity = Blueprint("activity", __name__)

@activity.route("/show/<int:activity_id>")
@login_required
def show(activity_id):
    activity = Activity.query.get(activity_id)
    if not activity:
        abort(404)
    else:
        return render_template("activity/show.html", activity=activity)

@activity.route("/join/<int:activity_id>")
@login_required
def join(activity_id):
    activity = Activity.query.get(activity_id)
    if not activity:
        abort(404)
    else:
        if current_user in activity.group.members:
            activity.users.append(current_user)
            activity.save()
            flash("成功参加"+activity.title+"活动", "success")
            return redirect(url_for('activity.show', activity_id=activity.id))
        else:
            flash("你还未加入"+ activity.group.name +"小组，请加入小组后再参加该活动", "error")
            return redirect(url_for('activity.show', activity_id=activity.id))

@activity.route("/update/<int:activity_id>", methods=["GET", "POST"])
@login_required
def update(activity_id):
    if request.method == "GET":
        activity = Activity.query.get(activity_id)
        if not activity:
            abort(404)
        else:
            return render_template("activity/form.html", activity=activity)
    elif request.method == "POST":
        activity = Activity.query.get(activity_id)
        title = request.form['title']
        address = request.form['address']
        start_time = datetime.datetime.strptime(request.form['start-time'], "%Y-%m-%d %H:%M")
        end_time = datetime.datetime.strptime(request.form['end-time'], "%Y-%m-%d %H:%M")
        if start_time < datetime.datetime.now():
            flash("活动开始时间已经过期，活动发布失败", "error")
            return redirect(url_for("president.activities"))
        if start_time >= end_time:
            flash("活动结束时间小于活动开始时间，活动发布失败", "error")
            return redirect(url_for('president.activities'))
        count = int(request.form['count'])
        content = request.form['content']
        activity.title=title
        activity.address = address
        activity.start_time = start_time
        activity.end_time = end_time
        activity.count = count
        activity.content = content
        activity.save()
        flash("活动修改成功", "success")
        return redirect(url_for("president.activities"))

@activity.route("/delete/<int:activity_id>")
@login_required
def delete(activity_id):
    activity = Activity.query.get(activity_id)
    if not activity:
        abort(404)
    else:
        if not current_user == activity.user:
            abort(403)
        else:
            activity.delete()
            flash("活动删除成功", "success")
            return redirect(url_for("president.activities"))
