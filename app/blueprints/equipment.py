from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models.tables import Equipment, User
from app.forms.equipment_forms import EquipmentForm, EquipmentSearchForm
from app.db.database import db, load_user

equipment_bp = Blueprint('equipment', __name__)

@equipment_bp.route('/equipment', methods=['GET', 'POST'])
@login_required
def index():
    search_form = EquipmentSearchForm()
    print("^^^^^^^",search_form.search.data)
    query = Equipment.query
    
    if search_form.search.data:
        search_term = f"%{search_form.search.data}%"
        query = query.filter(
            db.or_(
                Equipment.sn.ilike(search_term),
                Equipment.model_name.ilike(search_term),
                Equipment.equipment_type.ilike(search_term),
                Equipment.manufacturer.ilike(search_term)
            )
        )
    
    equipment_list = query.all()
    return render_template('equipment/index.html', 
                         equipment=equipment_list, 
                         search_form=search_form)

@equipment_bp.route('/equipment/create', methods=['GET', 'POST'])
@login_required
def create():
    form = EquipmentForm()
    equipment_types = ['CPU', 'LAPTOP', 'MONITOR', 'PRINTER', 'SCANNER', 'OTHER']  # Get this from your database or configuration
    
    if form.validate_on_submit():
        try:
            equipment = Equipment(
                sn=form.sn.data,
                model_name=form.model_name.data,
                equipment_type=form.equipment_type.data,
                manufacturer=form.manufacturer.data,
                locname=form.locname.data,
                building=form.building.data,
                note=form.note.data,
                created_by=current_user.staffno
            )
            db.session.add(equipment)
            db.session.commit()
            flash('Equipment added successfully', 'success')
            return redirect(url_for('equipment.index'))
        except Exception as e:
            flash(f'Error adding equipment: {str(e)}', 'error')
            db.session.rollback()
    
    return render_template('equipment/add.html', form=form, equipment_types=equipment_types)

@equipment_bp.route('/equipment/<string:sn>/edit', methods=['GET', 'POST'])
@login_required
def edit(sn):
    equipment = Equipment.query.get_or_404(sn)
    form = EquipmentForm(obj=equipment, equipment=equipment)
    
    if form.validate_on_submit():
        try:
            form.populate_obj(equipment)
            db.session.commit()
            flash('Equipment updated successfully', 'success')
            return redirect(url_for('equipment.view', sn=sn))
        except Exception as e:
            flash(f'Error updating equipment: {str(e)}', 'error')
            db.session.rollback()
    
    return render_template('equipment/edit.html', form=form, equipment=equipment) 




@equipment_bp.route('/equipment/maintenance/<sn>')  # Add this route
@login_required
def viewequipmentmaintenance(sn):
    equipment = Equipment.query.filter_by(sn=sn).first_or_404()
    created_by=load_user(equipment.created_by).staffname
    return render_template('equipment/equipment.html', equipments=equipment,created_by=created_by)


@equipment_bp.route('/equipment/<sn>')  # Add this route
@login_required
def view(sn):
    equipment = Equipment.query.filter_by(sn=sn).first_or_404()
    return render_template('equipment/view.html', equipment=equipment)

