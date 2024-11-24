from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models.tables import Workshop
from app.forms.workshop import WorkshopForm
from app.db.database import db
from functools import wraps

workshop = Blueprint('workshop', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.isadmin:
            flash('Admin access required.', 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@workshop.route('/workshops')
@login_required
def list_workshops():
    workshops = Workshop.query.all()
    form = WorkshopForm()
    return render_template('workshop/list.html', workshops=workshops, form=form)

@workshop.route('/workshop/add', methods=['POST'])
@login_required
@admin_required
def add_workshop():
    form = WorkshopForm()
    if form.validate_on_submit():
        workshop = Workshop(
            workshopname=form.workshopname.data,
            building=form.building.data,
            contact=form.contact.data
        )
        db.session.add(workshop)
        db.session.commit()
        flash('Workshop added successfully!', 'success')
    return redirect(url_for('workshop.list_workshops'))

@workshop.route('/workshop/update/<int:id>', methods=['POST'])
@login_required
@admin_required
def update_workshop(id):
    workshop = Workshop.query.get_or_404(id)
    form = WorkshopForm()
    
    if form.validate_on_submit():
        try:
            workshop.workshopname = form.workshopname.data
            workshop.building = form.building.data
            workshop.contact = form.contact.data
            
            db.session.commit()
            flash('Workshop updated successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating workshop: {str(e)}', 'error')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{field}: {error}', 'error')
    
    return redirect(url_for('workshop.list_workshops'))

@workshop.route('/workshop/delete/<int:id>', methods=['DELETE'])
@login_required
@admin_required
def delete_workshop(id):
    workshop = Workshop.query.get_or_404(id)
    try:
        db.session.delete(workshop)
        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'Workshop deleted successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error deleting workshop: {str(e)}'
        }), 400 