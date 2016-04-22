from flask import Blueprint, abort,render_template,flash,redirect,url_for,request
from flask_login import login_required,current_user
from zoo.activity.models import Activity
from zoo.reply.models import Reply
import datetime

reply = Blueprint("reply", __name__)

@reply.route("/new/<int:activity_id>", methods=['POST'])
@login_required
def new(activity_id):
    activity = Activity.query.get(activity_id)
    if not activity:
        abort(404)
    else:
        reply = Reply(created_at=datetime.datetime.now(),content=request.form['content'],user=current_user,activity=activity )
        reply.save()
        return redirect(url_for('activity.show', activity_id=activity_id))




