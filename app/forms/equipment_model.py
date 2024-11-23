from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length
from app.models.tables import EquipmentType

class EquipmentModelForm(FlaskForm):
    equipmentmodel = StringField('Model Name', validators=[DataRequired(), Length(max=100)])
    etid = SelectField('Equipment Type', coerce=int, validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Length(max=200)])
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(EquipmentModelForm, self).__init__(*args, **kwargs)
        self.etid.choices = [(et.etid, et.equipmenttype) 
                            for et in EquipmentType.query.order_by(EquipmentType.equipmenttype).all()] 