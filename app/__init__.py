from flask import Flask, render_template, request, redirect, url_for
from flask_migrate import Migrate
from db.base import db
from config import Config
from flask_login import LoginManager
from app.models.tables import User
from app.routes import equipment_type
from app.routes import workshop

migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    # Import blueprints
    from app.routes.main import bp as main_bp
    from app.routes.auth import bp as auth_bp
    from app.routes.equipment import bp as equipment_bp
    from app.routes.equipment_model import bp as equipment_model_bp
    from app.routes.equipment_type import bp as equipment_type_bp
    from app.routes.equipment_activity import bp as equipment_activity_bp
    from app.routes.company_user import bp as company_user_bp
    from app.routes.user import bp as user_bp
    from app.routes.workshop import bp as workshop_bp
    from app.routes.location import bp as location_bp

    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(equipment_bp)
    app.register_blueprint(equipment_model_bp)
    app.register_blueprint(equipment_type_bp)
    app.register_blueprint(equipment_activity_bp)
    app.register_blueprint(company_user_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(workshop_bp)
    app.register_blueprint(location_bp)

    

    # Register error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html', 
                             return_url=request.referrer or url_for('main.index')), 404

    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('errors/403.html',
                             return_url=request.referrer or url_for('main.index')), 403

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html',
                             return_url=request.referrer or url_for('main.index')), 500

    return app 