from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import Optional

class SearchForm(FlaskForm):
    query = StringField('Search', validators=[Optional()])
    sort_by = SelectField('Sort By', choices=[
        ('name', 'Name'),
        ('type', 'Type')
    ])
    order = SelectField('Order', choices=[
        ('asc', 'Ascending'),
        ('desc', 'Descending')
    ])
    submit = SubmitField('Search') 