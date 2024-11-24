from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class WorkshopForm(FlaskForm):
    workshopname = StringField('Workshop Name', validators=[DataRequired()])
    building = StringField('Building', validators=[DataRequired()])
    contact = StringField('Contact') 