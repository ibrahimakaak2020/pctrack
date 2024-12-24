from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_wtf import FlaskForm
from wtforms import SelectField, TextAreaField, FloatField, SubmitField
from wtforms.validators import DataRequired
from flask_login import login_required, current_user
from app.forms.maintenancerecordform import MaintenanceRecordForm
from app.models.tables import Equipment, MaintenanceRecord, MaintenanceStatus, Workshop, CompanyUser
from app.db.database import db
from datetime import datetime, timezone

# Create Blueprint
maintenance = Blueprint('maintenance', __name__, 
                       template_folder='templates',
                       url_prefix='/maintenance')

# Constants
status_colors = {
    'pending': 'secondary',
    'received': 'info',
    'diagnosed': 'warning',
    'in_progress': 'primary',
    'completed': 'success',
    'cancelled': 'danger'
}

# Forms
class StatusUpdateForm(FlaskForm):
    status = SelectField('Status', validators=[DataRequired()],
                        choices=[
                            ('received', 'Mark as Received'),
                            ('diagnosed', 'Mark as Diagnosed'),
                            ('in_progress', 'Start Repair'),
                            ('completed', 'Mark as Completed'),
                            ('cancelled', 'Cancel Maintenance')
                        ])
    notes = TextAreaField('Status Notes', validators=[DataRequired()])
    final_cost = FloatField('Final Cost')
    resolution_notes = TextAreaField('Resolution Notes')
    submit = SubmitField('Update Status')

    def set_status_choices(self, current_status):
        if current_status == 'pending':
            self.status.choices = [('received', 'Mark as Received')]
        elif current_status == 'received':
            self.status.choices = [('diagnosed', 'Mark as Diagnosed')]
        elif current_status == 'diagnosed':
            self.status.choices = [('in_progress', 'Start Repair')]
        elif current_status == 'in_progress':
            self.status.choices = [('completed', 'Mark as Completed')]
        
        # Always allow cancellation
        self.status.choices.append(('cancelled', 'Cancel Maintenance'))

# Context Processors
@maintenance.context_processor
def utility_processor():
    return dict(status_colors=status_colors)

# Routes
@maintenance.route('/equipment/<string:sn>')
@login_required
def equipment_history(sn):
    equipment = Equipment.query.get_or_404(sn)
    maintenance_records = MaintenanceRecord.query.filter_by(equipment_sn=sn)\
        .order_by(MaintenanceRecord.maintenance_date.desc()).all()
    return render_template('maintenance/history.html', 
                         equipment=equipment, 
                         records=maintenance_records)

@maintenance.route('/record/<int:record_id>')
@login_required
def record_detail(record_id):
    record = MaintenanceRecord.query.get_or_404(record_id)
    status_updates = MaintenanceStatus.query\
        .filter_by(maintenance_id=record_id)\
        .order_by(MaintenanceStatus.status_date.desc()).all()
    
    form = StatusUpdateForm()
    form.set_status_choices(record.current_status)
    
    return render_template('maintenance/detail.html',
                         record=record,
                         status_updates=status_updates,
                         form=form)

@maintenance.route('/record/<int:record_id>/update-status', methods=['POST'])
@login_required
def update_status(record_id):
    record = MaintenanceRecord.query.get_or_404(record_id)
    form = StatusUpdateForm()
    form.set_status_choices(record.current_status)
    
    if form.validate_on_submit():
        status_update = MaintenanceStatus(
            maintenance_id=record_id,
            status=form.status.data,
            notes=form.notes.data,
            updated_by=current_user.staffno
        )
        
        # Update the main record
        record.current_status = form.status.data
        if form.status.data == 'completed':
            record.completion_date = datetime.now(timezone.utc)
            record.final_cost = form.final_cost.data
            record.resolution_notes = form.resolution_notes.data
        
        db.session.add(status_update)
        db.session.commit()
        
        flash('Maintenance status updated successfully', 'success')
        return redirect(url_for('maintenance.record_detail', record_id=record_id))
    
    flash('Error updating status', 'error')
    return redirect(url_for('maintenance.record_detail', record_id=record_id))

@maintenance.route('/new/<string:sn>', methods=['GET', 'POST'])
@login_required
def new_record(sn):
    equipment = Equipment.query.get_or_404(sn)
    form = MaintenanceRecordForm()
    if request.method == 'POST':
        print("*********** from POST")
        try:
            print("*********** from try")
            print(sn,request.form.get('is_external') == '1' )
            record = MaintenanceRecord(
                equipment_sn=sn,
                registered_by=current_user.staffno,
                is_external=request.form.get('is_external') == '1' ,
                problem_description=request.form.get('problem_description'),
                current_status='pending'
            )
          
            
            if record.is_external:
                record.company_id = form.company_id.data
                if form.is_external.data:
                    company_id = form.company_id.data
                    if company_id is None:
                        # Handle the case where company_id is required for external maintenance
                        flash("Company ID is required for external maintenance.", "error")
                        return redirect(url_for('maintenance_record'))
                    else:
                        print(company_id)
                
            else:
                record.workshop_id = request.form.get('workshop_id', type=int)
            print("******************",record)
            db.session.add(record)
            db.session.commit()
            equipment.isundermaintenance=True
            db.session.commit()

            

            
            # Create initial status
            initial_status = MaintenanceStatus(maintenance_id=record.id,status='pending',notes='Maintenance request registered',updated_by=current_user.staffno)
            db.session.add(initial_status)
            
            db.session.commit()
            flash('New maintenance record created successfully', 'success')
            return redirect(url_for('main.dashboard', record_id=record.id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating maintenance record: {str(e)}', 'error')
    
    # Get available workshops and companies for the form
    workshops = Workshop.query.all()
    companies = CompanyUser.query.all()
    return render_template('maintenance/new.html', form=form,
                         equipment=equipment,
                         workshops=workshops,
                         companies=companies)

@maintenance.route('/record/<int:record_id>/delete', methods=['POST'])
@login_required
def delete_record(record_id):
    record = MaintenanceRecord.query.get_or_404(record_id)
    
    # Check if user has permission to delete
    if not current_user.isadmin and record.registered_by != current_user.staffno:
        flash('You do not have permission to delete this record', 'error')
        return redirect(url_for('maintenance.record_detail', record_id=record_id))
    
    try:
        # Delete associated status updates first
        MaintenanceStatus.query.filter_by(maintenance_id=record_id).delete()
        db.session.delete(record)
        db.session.commit()
        flash('Maintenance record deleted successfully', 'success')
        return redirect(url_for('maintenance.equipment_history', sn=record.equipment_sn))
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting maintenance record: {str(e)}', 'error')
        return redirect(url_for('maintenance.record_detail', record_id=record_id))

# API Routes for AJAX updates
@maintenance.route('/api/record/<int:record_id>/status', methods=['GET'])
@login_required
def get_status_history(record_id):
    status_updates = MaintenanceStatus.query\
        .filter_by(maintenance_id=record_id)\
        .order_by(MaintenanceStatus.status_date.desc())\
        .all()
    
    return jsonify([{
        'status': status.status,
        'notes': status.notes,
        'date': status.status_date.isoformat(),
        'updated_by': status.user.staffname
    } for status in status_updates])

# Equipment List Route
@maintenance.route('/equipment')
@login_required
def equipment_list():
    equipment = Equipment.query.all()
    # Get all active maintenance records for each equipment
    maintenance_records = {}
    for eq in equipment:
        maintenance_records[eq.sn] = MaintenanceRecord.query.filter_by(equipment_sn=eq.sn)\
            .filter(MaintenanceRecord.current_status.in_(['pending', 'received', 'diagnosed', 'in_progress']))\
            .order_by(MaintenanceRecord.maintenance_date.desc())\
            .all()
    
    return render_template('maintenance/equipment_list.html', 
                         equipment=equipment,
                         maintenance_records=maintenance_records)

# Active Maintenance Records
@maintenance.route('/active')
@login_required
def active_records():
    active_maintenance = MaintenanceRecord.query.filter(
        MaintenanceRecord.current_status.in_(['pending', 'received', 'diagnosed', 'in_progress'])
    ).order_by(MaintenanceRecord.maintenance_date.desc()).all()
    return render_template('maintenance/active_records.html', records=active_maintenance)

# Equipment Registration (Admin Only)
@maintenance.route('/equipment/register', methods=['GET', 'POST'])
@login_required
def equipment_register():
    if not current_user.isadmin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('maintenance.equipment_list'))
    
    form = EquipmentRegistrationForm()  # Create an instance of your form class

    if request.method == 'POST':
        if form.validate_on_submit():  # Validate the form
            try:
                equipment = Equipment(
                    sn=form.sn.data,
                    model_name=form.model_name.data,
                    # Add other fields as needed
                )
                db.session.add(equipment)
                db.session.commit()
                flash('Equipment registered successfully', 'success')
                return redirect(url_for('maintenance.equipment_list'))
            except Exception as e:
                db.session.rollback()
                flash(f'Error registering equipment: {str(e)}', 'danger')
    
    return render_template('maintenance/equipment_register.html', form=form)  # Pass the form to the template

# Search Route
@maintenance.route('/search')
@login_required
def search():
    query = request.args.get('q', '')
    if not query:
        return redirect(url_for('maintenance.equipment_list'))
    
    equipment = Equipment.query.filter(
        (Equipment.sn.ilike(f'%{query}%')) |
        (Equipment.model_name.ilike(f'%{query}%'))
    ).all()
    
    maintenance_records = MaintenanceRecord.query.filter(
        MaintenanceRecord.problem_description.ilike(f'%{query}%')
    ).all()
    
    return render_template('maintenance/search_results.html',
                         query=query,
                         equipment=equipment,
                         maintenance_records=maintenance_records) 