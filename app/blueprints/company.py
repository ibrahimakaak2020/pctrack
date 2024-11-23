from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.tables import CompanyUser
from app.forms.company_forms import CompanyUserForm, CompanySearchForm
from app.db.database import db
from app.utils.decorators import admin_required

company_bp = Blueprint('company', __name__)

@company_bp.route('/companies')
@login_required
def company_list():
    search_form = CompanySearchForm()
    query = CompanyUser.query
    
    if search_form.search.data:
        search_term = f"%{search_form.search.data}%"
        query = query.filter(
            db.or_(
                CompanyUser.staffname.ilike(search_term),
                CompanyUser.companyname_en.ilike(search_term),
                CompanyUser.companyname_ar.ilike(search_term),
                CompanyUser.contactnumber.ilike(search_term)
            )
        )
    
    companies = query.order_by(CompanyUser.companyname_en).all()
    return render_template('company/list.html', 
                         companies=companies, 
                         search_form=search_form)

@company_bp.route('/companies/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_company():
    form = CompanyUserForm()
    if form.validate_on_submit():
        company = CompanyUser(
            staffname=form.staffname.data,
            companyname_en=form.companyname_en.data,
            companyname_ar=form.companyname_ar.data,
            contactnumber=form.contactnumber.data
        )
        db.session.add(company)
        try:
            db.session.commit()
            flash('Company added successfully', 'success')
            return redirect(url_for('company.company_list'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while adding the company. Please try again.', 'danger')
    
    return render_template('company/form.html', form=form, title='Add New Company')

@company_bp.route('/companies/<int:cid>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_company(cid):
    company = CompanyUser.query.get_or_404(cid)
    form = CompanyUserForm(obj=company)
    
    if form.validate_on_submit():
        company.staffname = form.staffname.data
        company.companyname_en = form.companyname_en.data
        company.companyname_ar = form.companyname_ar.data
        company.contactnumber = form.contactnumber.data
        db.session.commit()
        flash('Company updated successfully', 'success')
        return redirect(url_for('company.company_list'))
    
    return render_template('company/form.html', form=form, company=company, title='Edit Company')

@company_bp.route('/companies/<int:cid>/delete', methods=['POST'])
@login_required
@admin_required
def delete_company(cid):
    company = CompanyUser.query.get_or_404(cid)
    db.session.delete(company)
    db.session.commit()
    flash('Company deleted successfully', 'success')
    return redirect(url_for('company.company_list')) 