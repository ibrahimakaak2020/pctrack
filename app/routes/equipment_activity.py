from flask import Blueprint, render_template, request, flash, redirect, url_for
from app.models.tables import (
    EquipmentActivity, 
    EquipmentRegister, 
    User, 
    Workshop, 
    CompanyUser
)
from app import db
from datetime import datetime

bp = Blueprint('equipment_activity', __name__, url_prefix='/activities')

@bp.route('/')
def index():
    activities = EquipmentActivity.query.all()
    return render_template('equipment_activity/list.html', activities=activities)

@bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        activity = EquipmentActivity(
            registerid=request.form['registerid'],
            activitydate=datetime.strptime(request.form['activitydate'], '%Y-%m-%d'),
            createby=request.form['createby'],
            nextactivity=request.form['nextactivity'],
            activitydesc=request.form['activitydesc'],
            activitystatus=request.form['activitystatus'],
            maintaincestatus=request.form['maintaincestatus'],
            placeofmaintaince=request.form['placeofmaintaince'],
            workshopid=request.form.get('workshopid'),
            companyid=request.form.get('companyid')
        )
        
        if request.form.get('dateofmaintaince'):
            activity.dateofmaintaince = datetime.strptime(
                request.form['dateofmaintaince'], 
                '%Y-%m-%d'
            )
        
        try:
            db.session.add(activity)
            db.session.commit()
            flash('Activity created successfully', 'success')
            return redirect(url_for('equipment_activity.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating activity: {str(e)}', 'danger')
    
    equipment_registers = EquipmentRegister.query.all()
    users = User.query.all()
    workshops = Workshop.query.all()
    companies = CompanyUser.query.all()
    
    return render_template('equipment_activity/create.html',
        equipment_registers=equipment_registers,
        users=users,
        workshops=workshops,
        companies=companies
    ) 