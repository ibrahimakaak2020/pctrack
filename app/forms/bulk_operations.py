from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired

class BulkOperationForm(FlaskForm):
    action = SelectField('Action', choices=[
        ('delete', 'Delete Selected'),
        ('export', 'Export Selected')
    ], validators=[DataRequired()])
    format = SelectField('Export Format', choices=[
        ('csv', 'CSV'),
        ('excel', 'Excel'),
        ('pdf', 'PDF')
    ])
    submit = SubmitField('Apply') 