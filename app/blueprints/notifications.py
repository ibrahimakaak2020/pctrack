from flask import Blueprint, render_template

notifications_bp = Blueprint('notifications', __name__)

@notifications_bp.route('/')
def index():
    # your route logic here
    return render_template('notifications/index.html') 