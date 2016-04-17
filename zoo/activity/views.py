from flask import Blueprint, abort,render_template,flash,redirect,url_for
from flask_login import login_required,current_user
from zoo.activity.models import Activity

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