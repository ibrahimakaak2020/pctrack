from flask import Blueprint, render_template, request, flash, redirect, url_for
from app.models.tables import Equipment, EquipmentModel, EquipmentType
from app import db
from flask_login import login_required
from app.utils.decorators import admin_required

bp = Blueprint('equipment', __name__, url_prefix='/equipment')

@bp.route('/')
@login_required
def index():
    equipment_list = Equipment.query.all()
    return render_template('equipment/list.html', equipment=equipment_list)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create():
    if request.method == 'POST':
        sn = request.form.get('sn')
        emid = request.form.get('emid')
        locid = request.form.get('locid')
        
        equipment = Equipment(
            sn=sn,
            emid=emid,
            locid=locid,
            standby='N'
        )
        
        try:
            db.session.add(equipment)
            db.session.commit()
            flash('Equipment created successfully', 'success')
            return redirect(url_for('equipment.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating equipment: {str(e)}', 'danger')
    
    equipment_models = EquipmentModel.query.all()
    return render_template('equipment/create.html', equipment_models=equipment_models)

@bp.route('/<string:sn>/edit', methods=['GET', 'POST'])
def edit(sn):
    equipment = Equipment.query.get_or_404(sn)
    
    if request.method == 'POST':
        equipment.emid = request.form.get('emid')
        equipment.locid = request.form.get('locid')
        
        try:
            db.session.commit()
            flash('Equipment updated successfully', 'success')
            return redirect(url_for('equipment.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating equipment: {str(e)}', 'danger')
    
    equipment_models = EquipmentModel.query.all()
    return render_template('equipment/edit.html', equipment=equipment, equipment_models=equipment_models)

@bp.route('/<string:sn>/delete', methods=['POST'])
def delete(sn):
    equipment = Equipment.query.get_or_404(sn)
    try:
        db.session.delete(equipment)
        db.session.commit()
        flash('Equipment deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting equipment: {str(e)}', 'danger')
    
    return redirect(url_for('equipment.index')) 