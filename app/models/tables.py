from db.base import db
from datetime import datetime
from flask_login import UserMixin

class CompanyUser(db.Model):
    __tablename__ = "companyuser"

    cid = db.Column(db.Integer, primary_key=True, index=True)
    staffname = db.Column(db.String(100), nullable=False)
    companyname_en = db.Column(db.String(100), nullable=False)
    companyname_ar = db.Column(db.String(100), nullable=False)
    contactnumber = db.Column(db.String(30), nullable=False, index=True)
    
    equipment_activities = db.relationship("EquipmentActivity", back_populates="company_user")

class EquipmentActivity(db.Model):
    __tablename__ = "equipmentactivity"
    
    activityid = db.Column(db.Integer, primary_key=True, index=True)
    registerid = db.Column(db.Integer, db.ForeignKey('equipmentregister.registerid'), nullable=False)
    activitydate = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    createby = db.Column(db.Integer, db.ForeignKey('user.staffno'), nullable=False)
    nextactivity = db.Column(db.String(3), nullable=False)
    activitydesc = db.Column(db.String(300), nullable=False)
    activitystatus = db.Column(db.String(3), nullable=False)
    maintaincestatus = db.Column(db.String(3), nullable=False)
    dateofmaintaince = db.Column(db.DateTime)
    placeofmaintaince = db.Column(db.String(1), nullable=False)
    workshopid = db.Column(db.Integer, db.ForeignKey('workshop.wid'))
    billid = db.Column(db.String(30))
    billamount = db.Column(db.Integer)
    companyid = db.Column(db.Integer, db.ForeignKey('companyuser.cid'))
    dateofsend = db.Column(db.DateTime)
    dateofreturnback = db.Column(db.DateTime)
    dateofrecievefrom = db.Column(db.DateTime)

    equipment_register = db.relationship("EquipmentRegister", back_populates="equipment_activities")
    user = db.relationship("User", back_populates="activities")
    workshop = db.relationship("Workshop", back_populates="equipment_activities")
    company_user = db.relationship("CompanyUser", back_populates="equipment_activities")

class User(UserMixin, db.Model):
    __tablename__ = "user"

    staffno = db.Column(db.Integer, primary_key=True, index=True)
    staffname = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(300), nullable=False)
    isadmin = db.Column(db.Boolean, nullable=False, default=False)
    
    equipment_registers = db.relationship("EquipmentRegister", back_populates="user")
    activities = db.relationship("EquipmentActivity", back_populates="user")

    def get_id(self):
        return str(self.staffno)

class Workshop(db.Model):
    __tablename__ = "workshop"

    wid = db.Column(db.Integer, primary_key=True)
    workshopname = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(100))
    locid = db.Column(db.Integer, db.ForeignKey('location.locid'), nullable=False)
    
    location = db.relationship('Location', backref=db.backref('workshops', lazy=True))
   
    equipment_activities = db.relationship("EquipmentActivity", back_populates="workshop")

class Equipment(db.Model):
    __tablename__ = "equipment"

    sn = db.Column(db.String(50), primary_key=True, index=True)
    emid = db.Column(db.Integer, db.ForeignKey('equipmentmodel.emid'), nullable=False)
    locid = db.Column(db.Integer, db.ForeignKey('location.locid'))
    standby = db.Column(db.String(1), nullable=False, default='N')
    
    # Relationships
    equipment_model = db.relationship("EquipmentModel", back_populates="equipment")
    location = db.relationship("Location", back_populates="equipment")
    equipment_registers = db.relationship("EquipmentRegister", back_populates="equipment")

class EquipmentModel(db.Model):
    __tablename__ = "equipmentmodel"

    emid = db.Column(db.Integer, primary_key=True, index=True)
    equipmentmodel = db.Column(db.String(100), nullable=False)
    etid = db.Column(db.Integer, db.ForeignKey('equipmenttype.etid'), nullable=False)
    description = db.Column(db.String(200))
    
    # Relationships
    equipment_type = db.relationship("EquipmentType", back_populates="equipment_models")
    equipment = db.relationship("Equipment", back_populates="equipment_model")

class EquipmentType(db.Model):
    __tablename__ = "equipmenttype"

    etid = db.Column(db.Integer, primary_key=True, index=True)
    equipmenttype = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    
    # Relationships
    equipment_models = db.relationship("EquipmentModel", back_populates="equipment_type")

class EquipmentRegister(db.Model):
    __tablename__ = "equipmentregister"

    registerid = db.Column(db.Integer, primary_key=True, index=True)
    sn = db.Column(db.String(50), db.ForeignKey('equipment.sn'), nullable=False)
    registerdate = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    createby = db.Column(db.Integer, db.ForeignKey('user.staffno'), nullable=False)
    
    # Relationships
    equipment = db.relationship("Equipment", back_populates="equipment_registers")
    user = db.relationship("User", back_populates="equipment_registers")
    equipment_activities = db.relationship("EquipmentActivity", back_populates="equipment_register")

class Location(db.Model):
    __tablename__ = "location"

    locid = db.Column(db.Integer, primary_key=True, index=True)
    locname = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    
    # Relationships
    equipment = db.relationship("Equipment", back_populates="location")

# Add other models similarly...
