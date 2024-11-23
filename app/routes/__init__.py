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

# Export all blueprints
__all__ = [
    'main_bp',
    'auth_bp',
    'equipment_bp',
    'equipment_model_bp',
    'equipment_type_bp',
    'equipment_activity_bp',
    'company_user_bp',
    'user_bp',
    'workshop_bp',
    'location_bp'
] 