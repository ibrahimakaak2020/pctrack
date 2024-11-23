from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from app.forms.user import UserForm
from app.models.tables import User
from app.utils.decorators import admin_required
from db.base import db

bp = Blueprint('user', __name__, url_prefix='/users')

@bp.route('/')
@login_required
@admin_required
def index():
    users = User.query.order_by(User.staffno).all()
    return render_template('user/list.html', users=users)

@bp.route('/create', methods=['GET', 'POST'])
#@login_required
#@admin_required
def create():
    form = UserForm()
    if form.validate_on_submit():
        user = User(
            staffno=form.staffno.data,
            staffname=form.staffname.data,
            password=generate_password_hash(form.password.data),
            isadmin=form.isadmin.data
        )
        try:
            db.session.add(user)
            db.session.commit()
            flash('User created successfully.', 'success')
            return redirect(url_for('user.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating user: {str(e)}', 'danger')
    
    return render_template('user/create.html', form=form)

@bp.route('/<int:staffno>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit(staffno):
    user = User.query.get_or_404(staffno)
    form = UserForm(original_staffno=user.staffno)
    
    if form.validate_on_submit():
        user.staffname = form.staffname.data
        user.isadmin = form.isadmin.data
        if form.password.data:
            user.password = generate_password_hash(form.password.data)
        
        try:
            db.session.commit()
            flash('User updated successfully.', 'success')
            return redirect(url_for('user.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating user: {str(e)}', 'danger')
    
    elif request.method == 'GET':
        form.staffno.data = user.staffno
        form.staffname.data = user.staffname
        form.isadmin.data = user.isadmin
    
    return render_template('user/edit.html', form=form, user=user)

@bp.route('/<int:staffno>/delete', methods=['POST'])
@login_required
@admin_required
def delete(staffno):
    if current_user.staffno == staffno:
        flash('You cannot delete your own account.', 'danger')
        return redirect(url_for('user.index'))
    
    user = User.query.get_or_404(staffno)
    try:
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting user: {str(e)}', 'danger')
    
    return redirect(url_for('user.index'))

@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UserForm(obj=current_user)
    
    if form.validate_on_submit():
        current_user.staffname = form.staffname.data
        if form.password.data:
            current_user.password = generate_password_hash(form.password.data)
            
        try:
            db.session.commit()
            flash('Profile updated successfully.', 'success')
            return redirect(url_for('user.profile'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating profile: {str(e)}', 'danger')
    
    return render_template('user/profile.html', form=form) 