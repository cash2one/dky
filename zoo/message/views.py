from flask import Blueprint,redirect,request,flash,render_template,url_for,abort,jsonify
from flask_login import login_required,current_user
from zoo.user.models import User




message = Blueprint("message", __name__)


@message.route("/brief")
@login_required
def brief():
    messages = current_user.get_brief_messages()
    return render_template("message/brief.html", messages=messages)

@message.route("/lookup/<int:type>")
@login_required
def look_up(type):
    if type == 1:
        current_user.read_message_by_type(1)
        follower_messages = current_user.get_messages()
        return render_template("message/message_list.html", follower_messages=follower_messages)

