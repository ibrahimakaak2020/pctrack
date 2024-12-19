from flask import Flask, flash, render_template
from app.config.config import config_dict
from app.db.database import init_db, db, login_manager, migrate
from datetime import datetime
from flask_wtf.csrf import CSRFProtect
from app.blueprints.workshop import workshop
from app.blueprints.equipment import equipment_bp
from app.blueprints.maintenance import maintenance
from app.utils.filters import filters
from app.blueprints.reports import reports_bp
from app.blueprints.notifications import notifications_bp

def create_app(config_name='default'):
    app = Flask(__name__)
    @app.errorhandler(404)
    def not_found_error(error):
     
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template('errors/500.html'), 500

    @app.errorhandler(403)
    def forbidden_error(error):
    
        return render_template('errors/403.html'), 403 
    # Load configuration
    app.config.from_object(config_dict[config_name])
    
    # Initialize database and extensions
    init_db(app)
    
    # Initialize login manager
    login_manager.init_app(app)
    login_manager.login_view = 'users.login'  # Specify the login route
    login_manager.login_message_category = 'info'
    
    # Set a secret key for CSRF protection
    app.config['SECRET_KEY'] = 'your-secret-key-here'  # Replace with a secure secret key
    csrf = CSRFProtect(app)
    
    # Register blueprints
    from app.blueprints.users import users_bp
    from app.blueprints.main import main_bp
    from app.blueprints.company import company_bp
  
    app.register_blueprint(users_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(company_bp)
    app.register_blueprint(workshop)
    app.register_blueprint(equipment_bp)
    app.register_blueprint(maintenance)
    app.register_blueprint(filters)
    app.register_blueprint(reports_bp, url_prefix='/reports')
    app.register_blueprint(notifications_bp, url_prefix='/notifications')
  
    
   
    @app.context_processor
    def utility_processor():
        return {'now': datetime.utcnow()}
    
    return app
