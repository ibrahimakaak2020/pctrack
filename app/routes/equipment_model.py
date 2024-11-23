from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app.forms.equipment_model import EquipmentModelForm
from app.forms.search import SearchForm
from app.models.tables import EquipmentModel, EquipmentType
from app.utils.decorators import admin_required
from db.base import db

bp = Blueprint('equipment_model', __name__, url_prefix='/equipment-models')

@bp.route('/')
@login_required
def index():
    search_form = SearchForm()
    models = EquipmentModel.query.all()
    return render_template('equipment_model/list.html',
                         models=models,
                         search_form=search_form)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create():
    form = EquipmentModelForm()
    
    if form.validate_on_submit():
        model = EquipmentModel(
            equipmentmodel=form.equipmentmodel.data,
            etid=form.etid.data,
            description=form.description.data
        )
        try:
            db.session.add(model)
            db.session.commit()
            flash('Equipment model created successfully.', 'success')
            return redirect(url_for('equipment_model.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating equipment model: {str(e)}', 'danger')
    
    return render_template('equipment_model/create.html', form=form)

@bp.route('/<int:emid>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit(emid):
    model = EquipmentModel.query.get_or_404(emid)
    form = EquipmentModelForm(obj=model)
    
    if form.validate_on_submit():
        model.equipmentmodel = form.equipmentmodel.data
        model.etid = form.etid.data
        model.description = form.description.data
        
        try:
            db.session.commit()
            flash('Equipment model updated successfully.', 'success')
            return redirect(url_for('equipment_model.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating equipment model: {str(e)}', 'danger')
    
    return render_template('equipment_model/edit.html', form=form, model=model)

@bp.route('/<int:emid>/delete', methods=['POST'])
@login_required
@admin_required
def delete(emid):
    model = EquipmentModel.query.get_or_404(emid)
    
    if model.equipment:
        flash('Cannot delete model with assigned equipment.', 'danger')
        return redirect(url_for('equipment_model.index'))
    
    try:
        db.session.delete(model)
        db.session.commit()
        flash('Equipment model deleted successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting equipment model: {str(e)}', 'danger')
    
    return redirect(url_for('equipment_model.index')) 