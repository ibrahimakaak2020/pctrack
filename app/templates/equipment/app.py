from datetime import datetime
from flask import Flask, flash, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, TextAreaField,DateTimeField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
import datetime as dt
app = Flask(__name__)
app.config["SECRET_KEY"] = "secret_key_here"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///equipment.db"
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy



class Equipment(db.Model):
    __tablename__ = "equipment"
    sn = db.Column(db.String(100), primary_key=True)  # Set sn as the primary key
    equipmentname = db.Column(db.String(100), nullable=False)
    equipmenttype = db.Column(db.String(100), nullable=False)
    isundermaintenance = db.Column(db.Boolean, default=False)
    # Establish relationship with maintenance records
    maintenance_records = db.relationship(
        "MaintenanceRecord", 
        back_populates="equipment", 
        lazy="dynamic"
    )


class MaintenanceRecord(db.Model):
    __tablename__ = "maintenancerecords"
    id = db.Column(db.Integer, primary_key=True)
    equipment_sn = db.Column(
        db.String(100), 
        db.ForeignKey("equipment.sn"), 
        nullable=False
    )
    problem_note = db.Column(db.Text, nullable=False)
    isactive = db.Column(db.Boolean, default=True)

    # Set up reverse relationship
    equipment = db.relationship("Equipment", back_populates="maintenance_records")
    
    # Establish relationship with maintenance statuses
    statuses = db.relationship(
        "MaintenanceStatus",
        back_populates="maintenance_record",
        lazy="dynamic"
    )


class MaintenanceStatus(db.Model):
    __tablename__ = "maintenancestatus"
    id = db.Column(db.Integer, primary_key=True)
    maintenance_record_id = db.Column(
        db.Integer, db.ForeignKey("maintenancerecords.id"), nullable=False
    )
    status = db.Column(db.String(100), nullable=False)
    status_note = db.Column(db.Text, nullable=False)
    status_date = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    # Set up reverse relationship
    maintenance_record = db.relationship(
        "MaintenanceRecord", 
        back_populates="statuses"
    )



class MaintenanceStatusForm(FlaskForm):
    status = StringField('Status', validators=[DataRequired()])
    status_note = TextAreaField('Status Note', validators=[DataRequired()])
    maintenance_record_id  = db.Column(db.Integer, db.ForeignKey("maintenancerecords.id"), nullable=False)
    submit = SubmitField("Submit")
with app.app_context():
    db.create_all()

class EquipmentForm(FlaskForm):
    sn = StringField("SN", validators=[DataRequired()])
    equipmentname = StringField("Equipment Name", validators=[DataRequired()])
    equipmenttype = StringField("Equipment Type", validators=[DataRequired()])

class MaintenanceForm(FlaskForm):
    status = SelectField("Status", choices=[("completed", "Completed"), ("in_progress", "In Progress")])
    problem_note = TextAreaField("Problem Note", validators=[DataRequired()])

@app.route("/")
def index():
    total_equipment = Equipment.query.count()
    under_maintenance_count = Equipment.query.filter_by(isundermaintenance=True).count()
    active_maintenance_count = MaintenanceRecord.query.filter_by(isactive=True).count()
    closed_maintenance_count = MaintenanceRecord.query.filter_by(isactive=False).count()

    statuses = db.session.query(MaintenanceStatus.status, db.func.count(MaintenanceStatus.status)).group_by(MaintenanceStatus.status).all()
    
    equipment_by_type = db.session.query(Equipment.equipmenttype, db.func.count(Equipment.sn)).group_by(Equipment.equipmenttype).all()

    return render_template("index.html",total_equipment=total_equipment,
        under_maintenance_count=under_maintenance_count,
        active_maintenance_count=active_maintenance_count,
        closed_maintenance_count=closed_maintenance_count,
        statuses=statuses,
        equipment_by_type=equipment_by_type)

@app.route("/equipment/register", methods=["GET", "POST"])
def register_equipment():
    form = EquipmentForm()
    if form.validate_on_submit():
        equipment = Equipment(sn=form.sn.data, equipmentname=form.equipmentname.data, equipmenttype=form.equipmenttype.data)
        db.session.add(equipment)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("register_equipment.html", form=form)

@app.route("/maintenance/register/<int:equipment_id>", methods=["GET", "POST"])
def register_maintenance(equipment_id):
    equipment = Equipment.query.get(equipment_id)
    if equipment is None:
        return redirect(url_for("index"))
    form = MaintenanceForm()
    if form.validate_on_submit():
        maintenance_record = MaintenanceRecord(equipment_sn=equipment_id, problem_note=form.problem_note.data)
        equipment.isundermaintenance = True
        db.session.add(maintenance_record)
        db.session.commit()
        return redirect(url_for("list_maintenance"))
    return render_template("register_maintenance.html", form=form, equipment=equipment)

@app.route("/equipment/list")
def list_equipment():
    equipments = Equipment.query.all()
    for equipment in equipments:
        for maintenance_record in equipment.maintenance_records:
            for status in maintenance_record.statuses:
                print(status.status_date, status.status, status.status_note)
    return render_template("list_equipment.html", equipment=equipments)

@app.route("/maintenance/list")
def list_maintenance():
  formstatus = MaintenanceStatusForm()
  formmaintenance = MaintenanceForm()
  equipments = Equipment.query.all()
  for equipment in equipments:
      print(equipment.maintenance_records.count())
  return render_template("list_maintenance.html", equipments=equipments,form=formstatus,formmaintenance=formmaintenance)
@app.route("/maintenance-status/create/<int:maintenance_record_id>", methods=["GET", "POST"])
def create_maintenance_status(maintenance_record_id):
    form = MaintenanceStatusForm()
     
    if form.validate_on_submit():
        maintenance_status = MaintenanceStatus(
            maintenance_record_id =maintenance_record_id, 
            status=form.status.data,
            status_note=form.status_note.data
        )
        db.session.add(maintenance_status)
        if form.status.data == "completed":
            maintenance_record = MaintenanceRecord.query.get(maintenance_record_id)
            equipment=Equipment.query.get(maintenance_record.equipment_sn)
            equipment.isundermaintenance = False
            maintenance_record.isactive = False

        db.session.commit()
        flash("Maintenance status created successfully", "success")
        return redirect(url_for("list_maintenance"))
    print("-----",form.errors)
    flash("Maintenance status creation failed", "danger")
    return redirect(url_for("list_maintenance"))
@app.route("/maintenance-status/list")
def list_maintenance_status():
    maintenance_status_list = MaintenanceStatus.query.all()
    return render_template("list_maintenance_status.html", maintenance_status_list=maintenance_status_list)
@app.route("/maintenance-status/update/<int:maintenance_status_id>", methods=["GET", "POST"])
def update_maintenance_status(maintenance_status_id):
    maintenance_status = MaintenanceStatus.query.get(maintenance_status_id)
    if maintenance_status is None:
        flash("Maintenance status not found", "error")
        return redirect(url_for("list_maintenance_status"))
    form = MaintenanceStatusForm(obj=maintenance_status)
    if form.validate_on_submit():
        form.populate_obj(maintenance_status)
        db.session.commit()
        flash("Maintenance status updated successfully", "success")
        return redirect(url_for("list_maintenance_status"))
    return render_template("update_maintenance_status.html", form=form)
@app.route("/maintenance-status/delete/<int:maintenance_status_id>", methods=["GET", "POST"])
def delete_maintenance_status(maintenance_status_id):
    maintenance_status = MaintenanceStatus.query.get(maintenance_status_id)
    if maintenance_status is None:
        flash("Maintenance status not found", "error")
        print("Maintenance status not found")
        return redirect(url_for("list_maintenance"))
    db.session.delete(maintenance_status)
    db.session.commit()
    print("Maintenance status deleted successfully")
    flash("Maintenance status deleted successfully", "success")
    return redirect(url_for("list_maintenance"))
@app.route('/statistics')
def statistics():
    total_equipment = Equipment.query.count()
    under_maintenance_count = Equipment.query.filter_by(isundermaintenance=True).count()
    active_maintenance_count = MaintenanceRecord.query.filter_by(isactive=True).count()
    closed_maintenance_count = MaintenanceRecord.query.filter_by(isactive=False).count()

    statuses = db.session.query(MaintenanceStatus.status, db.func.count(MaintenanceStatus.status)).group_by(MaintenanceStatus.status).all()
    
    equipment_by_type = db.session.query(Equipment.equipmenttype, db.func.count(Equipment.sn)).group_by(Equipment.equipmenttype).all()

    return render_template(
        'statistics.html',
        total_equipment=total_equipment,
        under_maintenance_count=under_maintenance_count,
        active_maintenance_count=active_maintenance_count,
        closed_maintenance_count=closed_maintenance_count,
        statuses=statuses,
        equipment_by_type=equipment_by_type
    )
if __name__ == "__main__":
    app.run(debug=True)