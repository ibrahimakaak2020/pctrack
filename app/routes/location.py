from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app.forms.location import LocationForm
from app.models.tables import Location
from app.utils.decorators import admin_required
from db.base import db

bp = Blueprint('location_bp', __name__, url_prefix='/locations')

@bp.route('/')
@login_required
def index():
    locations = Location.query.all()
    return render_template('location/list.html', locations=locations)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create():
    form = LocationForm()
    if form.validate_on_submit():
        location = Location(
            locname=form.locname.data,
            description=form.description.data
        )
        try:
            db.session.add(location)
            db.session.commit()
            flash('Location created successfully.', 'success')
            return redirect(url_for('location_bp.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating location: {str(e)}', 'danger')
    
    return render_template('location/create.html', form=form)

@bp.route('/<int:locid>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit(locid):
    location = Location.query.get_or_404(locid)
    form = LocationForm(obj=location)
    
    if form.validate_on_submit():
        location.locname = form.locname.data
        location.description = form.description.data
        
        try:
            db.session.commit()
            flash('Location updated successfully.', 'success')
            return redirect(url_for('location_bp.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating location: {str(e)}', 'danger')
    
    return render_template('location/edit.html', form=form, location=location)

@bp.route('/<int:locid>/delete', methods=['POST'])
@login_required
@admin_required
def delete(locid):
    location = Location.query.get_or_404(locid)
    
    if location.workshops:
        flash('Cannot delete location with assigned workshops.', 'danger')
        return redirect(url_for('location_bp.index'))
    
    try:
        db.session.delete(location)
        db.session.commit()
        flash('Location deleted successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting location: {str(e)}', 'danger')
    
    return redirect(url_for('location_bp.index')) 