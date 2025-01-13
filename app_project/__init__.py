from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    
    db.init_app(app)
    login_manager.init_app(app)
    
    with app.app_context():
        from .user import user as user_blueprint
        from .companyuser import companyuser as companyuser_blueprint
        from .workshop import workshop as workshop_blueprint
        from .equipment import equipment as equipment_blueprint
        from .maintenancerecord import maintenancerecord as maintenancerecord_blueprint
        from .maintenancestatus import maintenancestatus as maintenancestatus_blueprint

        app.register_blueprint(user_blueprint, url_prefix='/users')
        app.register_blueprint(companyuser_blueprint, url_prefix='/companyusers')
        app.register_blueprint(workshop_blueprint, url_prefix='/workshops')
        app.register_blueprint(equipment_blueprint, url_prefix='/equipment')
        app.register_blueprint(maintenancerecord_blueprint, url_prefix='/maintenancerecords')
        app.register_blueprint(maintenancestatus_blueprint, url_prefix='/maintenancestatuses')
        
        # Create all tables
        db.create_all()

    return app

@login_manager.user_loader
def load_user(user_id):
    from .models import User
    return User.query.get(int(user_id))