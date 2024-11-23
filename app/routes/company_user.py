from flask import Blueprint, render_template, request, flash, redirect, url_for
from app.models.tables import CompanyUser
from app import db

bp = Blueprint('company_user', __name__, url_prefix='/company-users')

@bp.route('/')
def index():
    companies = CompanyUser.query.all()
    return render_template('company_user/list.html', companies=companies)

@bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        company = CompanyUser(
            staffname=request.form['staffname'],
            companyname_en=request.form['companyname_en'],
            companyname_ar=request.form['companyname_ar'],
            contactnumber=request.form['contactnumber']
        )
        
        try:
            db.session.add(company)
            db.session.commit()
            flash('Company user created successfully', 'success')
            return redirect(url_for('company_user.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating company user: {str(e)}', 'danger')
    
    return render_template('company_user/create.html')

@bp.route('/<int:cid>/edit', methods=['GET', 'POST'])
def edit(cid):
    company = CompanyUser.query.get_or_404(cid)
    
    if request.method == 'POST':
        company.staffname = request.form['staffname']
        company.companyname_en = request.form['companyname_en']
        company.companyname_ar = request.form['companyname_ar']
        company.contactnumber = request.form['contactnumber']
        
        try:
            db.session.commit()
            flash('Company user updated successfully', 'success')
            return redirect(url_for('company_user.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating company user: {str(e)}', 'danger')
    
    return render_template('company_user/edit.html', company=company)

@bp.route('/<int:cid>/delete', methods=['POST'])
def delete(cid):
    company = CompanyUser.query.get_or_404(cid)
    try:
        db.session.delete(company)
        db.session.commit()
        flash('Company user deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting company user: {str(e)}', 'danger')
    
    return redirect(url_for('company_user.index')) 