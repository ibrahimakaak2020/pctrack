from flask import Blueprint, request, jsonify, abort, render_template, redirect, url_for
from flask_login import login_required, current_user
from ..decorate import admin_required
from ..models import db, User
user = Blueprint('user', __name__)


# User CRUD
@user.route('/', methods=['GET'])
#@login_required
#@admin_required
def get_users():
    users = User.query.all()
    return render_template('usertt/index.html', users=users)

@user.route('/<int:id>', methods=['GET'])
@login_required
@admin_required
def get_user(id):
    user = User.query.get_or_404(id)
    return render_template('usertt/update.html', user=user)

@user.route('/create', methods=['GET', 'POST'])
#@login_required
#@admin_required
def create_user():
    if request.method == 'POST':
        data = request.form
        new_user = User(
            staffname=data['staffname'],
            isadmin='isadmin' in data
        )
        new_user.set_password(data['password'])
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('user.get_users'))
    return render_template('usertt/create.html')

@user.route('/<int:id>', methods=['POST'])
@login_required
@admin_required
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.form
    user.staffname = data['staffname']
    if data['password']:
        user.set_password(data['password'])
    user.isadmin = 'isadmin' in data
    db.session.commit()
    return redirect(url_for('user.get_users'))

@user.route('/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('user.get_users'))