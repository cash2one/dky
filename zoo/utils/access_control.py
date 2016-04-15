from flask_login import current_user
from functools import wraps
from flask import abort


def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.role == 1:
            abort(403)
        return func(*args, **kwargs)
    return decorated_view

def president_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.role == 2:
            abort(403)
        return func(*args, **kwargs)
    return decorated_view