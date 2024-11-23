from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app.forms.workshop import WorkshopForm
from app.models.tables import Workshop
from app.utils.decorators import admin_required
from db.base import db

bp = Blueprint('workshop_bp', __name__, url_prefix='/workshops')

@bp.route('/')
@login_required
def index():
    workshops = Workshop.query.order_by(Workshop.workshopname).all()
    return render_template('workshop/list.html', workshops=workshops)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create():
    form = WorkshopForm()
    if form.validate_on_submit():
        workshop = Workshop(
            workshopname=form.workshopname.data,
            locid=form.locid.data,
            contact=form.contact.data
        )
        try:
            db.session.add(workshop)
            db.session.commit()
            flash('Workshop created successfully.', 'success')
            return redirect(url_for('workshop_bp.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating workshop: {str(e)}', 'danger')
    
    return render_template('workshop/create.html', form=form)

@bp.route('/<int:wid>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit(wid):
    workshop = Workshop.query.get_or_404(wid)
    form = WorkshopForm(obj=workshop)
    
    if form.validate_on_submit():
        workshop.workshopname = form.workshopname.data
        workshop.locid = form.locid.data
        workshop.contact = form.contact.data
        
        try:
            db.session.commit()
            flash('Workshop updated successfully.', 'success')
            return redirect(url_for('workshop_bp.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating workshop: {str(e)}', 'danger')
    
    return render_template('workshop/edit.html', form=form, workshop=workshop)

@bp.route('/<int:wid>/delete', methods=['POST'])
@login_required
@admin_required
def delete(wid):
    workshop = Workshop.query.get_or_404(wid)
    
    if workshop.equipment:  # If workshop has associated equipment
        flash('Cannot delete workshop with assigned equipment.', 'danger')
        return redirect(url_for('workshop_bp.index'))
    
    try:
        db.session.delete(workshop)
        db.session.commit()
        flash('Workshop deleted successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting workshop: {str(e)}', 'danger')
    
    return redirect(url_for('workshop_bp.index')) 