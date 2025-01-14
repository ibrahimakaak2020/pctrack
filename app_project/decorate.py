from functools import wraps
from flask import abort
from flask_login import login_required, current_user

def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.isadmin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function