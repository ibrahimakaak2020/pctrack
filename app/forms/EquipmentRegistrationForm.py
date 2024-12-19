from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, FloatField, SubmitField
from wtforms.validators import DataRequired

class EquipmentRegistrationForm(FlaskForm):
    model_name = StringField('Model Name', validators=[DataRequired()])
    equipment_type = SelectField('Equipment Type', choices=[
        ('CPU', 'CPU'),
        ('Printer', 'Printer'),
        ('Monitor', 'Monitor'),
        ('Other', 'Other')
    ], validators=[DataRequired()])
    manufacturer = StringField('Manufacturer', validators=[DataRequired()])
    locname = StringField('Location Name', validators=[DataRequired()])
    building = StringField('Building', validators=[DataRequired()])
    note = TextAreaField('Notes')
    created_by = StringField('Created By', validators=[DataRequired()])  # Assuming this is a user input
    submit = SubmitField('Register Equipment')