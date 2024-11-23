from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app.forms.equipment_type import EquipmentTypeForm
from app.models.tables import EquipmentType
from app.utils.decorators import admin_required
from db.base import db

bp = Blueprint('equipment_type_bp', __name__, url_prefix='/equipment-types')

@bp.route('/')
@login_required
def index():
    types = EquipmentType.query.order_by(EquipmentType.equipmenttype).all()
    return render_template('equipment_type/list.html', types=types)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create():
    form = EquipmentTypeForm()
    if form.validate_on_submit():
        equipment_type = EquipmentType(
            equipmenttype=form.equipmenttype.data,
            description=form.description.data
        )
        try:
            db.session.add(equipment_type)
            db.session.commit()
            flash('Equipment type created successfully.', 'success')
            return redirect(url_for('equipment_type_bp.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating equipment type: {str(e)}', 'danger')
    
    return render_template('equipment_type/create.html', form=form)

@bp.route('/<int:etid>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit(etid):
    equipment_type = EquipmentType.query.get_or_404(etid)
    form = EquipmentTypeForm(obj=equipment_type)
    
    if form.validate_on_submit():
        equipment_type.equipmenttype = form.equipmenttype.data
        equipment_type.description = form.description.data
        
        try:
            db.session.commit()
            flash('Equipment type updated successfully.', 'success')
            return redirect(url_for('equipment_type_bp.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating equipment type: {str(e)}', 'danger')
    
    return render_template('equipment_type/edit.html', form=form, type=equipment_type)

@bp.route('/<int:etid>/delete', methods=['POST'])
@login_required
@admin_required
def delete(etid):
    equipment_type = EquipmentType.query.get_or_404(etid)
    
    if equipment_type.equipment_models:
        flash('Cannot delete type with associated models.', 'danger')
        return redirect(url_for('equipment_type_bp.index'))
    
    try:
        db.session.delete(equipment_type)
        db.session.commit()
        flash('Equipment type deleted successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting equipment type: {str(e)}', 'danger')
    
    return redirect(url_for('equipment_type_bp.index')) 