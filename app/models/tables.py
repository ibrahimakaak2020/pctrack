from app.db.database import db
from datetime import datetime
from flask_login import UserMixin
from app.db.database import login_manager
from werkzeug.security import generate_password_hash, check_password_hash

class CompanyUser(db.Model):
    __tablename__ = "companyuser"

    cid = db.Column(db.Integer, primary_key=True, index=True)
    staffname = db.Column(db.String(100), nullable=False)
    companyname_en = db.Column(db.String(100), nullable=False)
    companyname_ar = db.Column(db.String(100), nullable=False)
    contactnumber = db.Column(db.String(30), nullable=False, index=True)
 
class User(db.Model, UserMixin):
    __tablename__ = "user"

    staffno = db.Column(db.Integer, primary_key=True, index=True)
    staffname = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(128))
    isadmin = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def get_id(self):
        return str(self.staffno)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Workshop(db.Model):
    __tablename__ = "workshop"

    id = db.Column(db.Integer, primary_key=True)
    workshopname = db.Column(db.String(100), nullable=False)
    building = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(100))
 


class Equipment(db.Model):
    __tablename__ = "equipment"

    # Primary Key
    sn = db.Column(db.String(50), primary_key=True, index=True)
    
    # Equipment Details
    model_name = db.Column(db.String(100), nullable=False)
    equipment_type = db.Column(db.String(50), nullable=False)  # CPU, Printer, etc.
    manufacturer = db.Column(db.String(100), nullable=False)
    locname = db.Column(db.String(100), nullable=False)
    building = db.Column(db.String(100), nullable=False)
    note = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(datetime.UTC))

    def __repr__(self):
        return f'<Equipment {self.model_name} (SN: {self.sn})>'

class MaintenanceStatus(db.Model):
    __tablename__ = "maintenance_status"

    id = db.Column(db.Integer, primary_key=True)
    maintenance_id = db.Column(db.Integer, db.ForeignKey('maintenance_record.id'), nullable=False)
    status_date = db.Column(db.DateTime, default=lambda: datetime.now(datetime.UTC))
    status = db.Column(db.String(20), nullable=False)  # 'received', 'diagnosed', 'in_progress', 'completed', 'cancelled'
    notes = db.Column(db.Text)
    updated_by = db.Column(db.Integer, db.ForeignKey('user.staffno'), nullable=False)

    # Relationships
    maintenance = db.relationship('MaintenanceRecord', backref=db.backref('status_updates', lazy=True))
    user = db.relationship('User', backref=db.backref('status_updates', lazy=True))

class MaintenanceRecord(db.Model):
    __tablename__ = "maintenance_record"

    id = db.Column(db.Integer, primary_key=True)
    equipment_sn = db.Column(db.String(50), db.ForeignKey('equipment.sn'), nullable=False)
    registered_by = db.Column(db.Integer, db.ForeignKey('user.staffno'), nullable=False)
    maintenance_date = db.Column(db.DateTime, default=lambda: datetime.now(datetime.UTC))
    is_external = db.Column(db.Boolean, nullable=False)
    
    # Workshop or Company reference
    workshop_id = db.Column(db.Integer, db.ForeignKey('workshop.id'))
    company_id = db.Column(db.Integer, db.ForeignKey('companyuser.cid'))
    
    # Initial request details
    problem_description = db.Column(db.Text, nullable=False)
    # Completion details
    completion_date = db.Column(db.DateTime)
    final_cost = db.Column(db.Float)
    resolution_notes = db.Column(db.Text)
 
    
    # Current status (computed from latest status update)
    current_status = db.Column(db.String(20), nullable=False, default='pending')
    
    # Relationships
    equipment = db.relationship('Equipment', backref=db.backref('maintenance_records', lazy=True))
    workshop = db.relationship('Workshop', backref=db.backref('maintenance_records', lazy=True))
    registered_user = db.relationship('User', backref=db.backref('maintenance_requests', lazy=True))
    company = db.relationship('CompanyUser', backref=db.backref('maintenance_records', lazy=True))

    def __repr__(self):
        location = f"Company: {self.company.companyname_en}" if self.is_external else f"Workshop: {self.workshop.workshopname}"
        return f'<MaintenanceRecord {self.id} ({self.current_status}) by {self.registered_user.staffname} at {location}>'

    @property
    def latest_status(self):
        return self.status_updates.order_by(MaintenanceStatus.status_date.desc()).first()

# Add other models similarly...
