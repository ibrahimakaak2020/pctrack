from flask import Blueprint, request, jsonify, abort, render_template, redirect, url_for
from flask_login import login_required, current_user
from ..decorate import admin_required
from ..models import db, User
main = Blueprint('main', __name__)


# main CRUD
@main.route('/', methods=['GET'])
#@login_required
#@admin_required
def index():
    user = User.query.all()
    return render_template('maintt/index.html', user=user)

