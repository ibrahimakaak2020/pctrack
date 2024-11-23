from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField, SubmitField, SelectMultipleField
from wtforms.validators import Optional
from app.utils.constants import FILTER_OPTIONS, CHART_TYPES

class AdvancedFilterForm(FlaskForm):
    # Basic filters
    search = StringField('Search Term')
    type = SelectMultipleField('Equipment Type', choices=[])
    status = SelectMultipleField('Status', choices=[])
    
    # Date range
    date_from = DateField('From Date', validators=[Optional()])
    date_to = DateField('To Date', validators=[Optional()])
    date_preset = SelectField('Date Range', choices=[
        ('', 'Custom'),
        ('today', 'Today'),
        ('week', 'This Week'),
        ('month', 'This Month'),
        ('year', 'This Year')
    ])
    
    # Sorting
    sort_by = SelectField('Sort By')
    sort_order = SelectField('Order', choices=[
        ('asc', 'Ascending'),
        ('desc', 'Descending')
    ])
    
    # Visualization
    chart_type = SelectField('Chart Type', choices=[(k, v) for k, v in CHART_TYPES.items()])
    
    # Items per page
    per_page = SelectField('Items per page', choices=[
        ('10', '10'),
        ('25', '25'),
        ('50', '50'),
        ('100', '100')
    ])
    
    apply = SubmitField('Apply Filters')
    reset = SubmitField('Reset')

    def __init__(self, model_type, *args, **kwargs):
        super(AdvancedFilterForm, self).__init__(*args, **kwargs)
        self.type.choices = [(t, t) for t in FILTER_OPTIONS[model_type]['type']]
        self.status.choices = [(s, s) for s in FILTER_OPTIONS[model_type]['status']] 