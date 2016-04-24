from flask import Blueprint, abort,render_template,flash,redirect,url_for,request
from flask_login import login_required,current_user
from zoo.activity.models import Activity


search = Blueprint("search", __name__)

@search.route("/", methods=['GET','POST'])
@login_required
def find():
    keyword = request.form['keyword']
    activities = Activity.query.filter(Activity.title.like('%'+ keyword + '%')).all()
    return render_template("search/result.html", activities=activities)

