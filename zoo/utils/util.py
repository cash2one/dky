from flask import flash
from flask_login import current_user
from zoo.message.models import Message
from zoo.user.models import User

def checkMessage(user):
    if len(user.messages.all()) > 0:
        for message in user.messages.all():
            flash(message.content, "info")
            message.delete()