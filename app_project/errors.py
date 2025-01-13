from flask import flash, render_template, Blueprint
errors_bp = Blueprint('errors', __name__)
@errors_bp.errorhandler(404)
def not_found_error(error):
    flash('Page not found', 'danger')
    return render_template('errors/404.html'), 404

@errors_bp.errorhandler(500)
def internal_error(error):
    flash('Internal server error', 'danger')
    return render_template('errors/500.html'), 500

@errors_bp.errorhandler(403)
def forbidden_error(error):
    flash('Access forbidden', 'danger')
    return render_template('errors/403.html'), 403 