from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length
from app.models.tables import Location

class WorkshopForm(FlaskForm):
    workshopname = StringField('Workshop Name', validators=[DataRequired(), Length(max=100)])
    locid = SelectField('Location', coerce=int, validators=[DataRequired()])
    contact = StringField('Contact Information', validators=[Length(max=100)])
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(WorkshopForm, self).__init__(*args, **kwargs)
        # Populate location choices
        self.locid.choices = [(loc.locid, loc.locname) 
                             for loc in Location.query.order_by(Location.locname).all()] 