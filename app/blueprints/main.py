from flask import Blueprint, render_template,redirect,url_for
from flask_login import login_required, current_user
from app.db.database import db
from app.models.tables import User
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('main/index.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    # Add any dashboard statistics or data you want to display
    notification_count = 0  # Set this to your actual notification count logic
    stats = {
        'total_users': db.session.query(User).count(),
        'notification_count': 0
        # Add more statistics as needed
    }
    return render_template('main/dashboard.html', stats=stats, notification_count=notification_count) 