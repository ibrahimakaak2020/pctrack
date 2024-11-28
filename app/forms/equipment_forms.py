from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from app.models.tables import Equipment

class EquipmentForm(FlaskForm):
    sn = StringField('Serial Number', 
        validators=[DataRequired(), Length(max=50)],
        render_kw={
            "placeholder": "Enter serial number",
            "class": "form-control",
            "pattern": "[A-Za-z0-9-]*",
            "title": "Alphanumeric characters and hyphens only"
        },
        description="Unique identifier for the equipment. Format: alphanumeric characters and hyphens.")
    
    model_name = StringField('Model Name', 
        validators=[DataRequired(), Length(max=100)],
        render_kw={
            "placeholder": "Enter model name",
            "class": "form-control"
        },
        description="The specific model name or number of the equipment(e.g. HP PRO ...)")
    
    equipment_type = StringField('Equipment Type',
        validators=[DataRequired(), Length(max=100)],
        render_kw={
            "placeholder": "Enter equipment type",
            "class": "form-control"
        },
        description="Category of the equipment (e.g.CPU , PRINTER, SCANNER ...)")
    
    manufacturer = StringField('Manufacturer',
        validators=[DataRequired(), Length(max=100)],
        render_kw={
            "placeholder": "Enter manufacturer name",
            "class": "form-control"
        },
        description="Name of the equipment manufacturer (e.g. HP,DELL,LENOVO ....)")
    
    locname = StringField('Location Name',
        validators=[DataRequired(), Length(max=100)],
        render_kw={
            "placeholder": "Enter location name (e.g., Room 101, Lab A)",
            "class": "form-control"
        },
        description="Specific location where the equipment is placed ")
    
    building = StringField('Building',
        validators=[DataRequired(), Length(max=100)],
        render_kw={
            "placeholder": "Enter building name",
            "class": "form-control"
        },
        description="Name or number of the building where the equipment is located")
    
    note = TextAreaField('Notes',
        validators=[Length(max=200)],
        render_kw={
            "placeholder": "Enter any additional notes",
            "class": "form-control",
            "rows": "3"
        },
        description="Additional information about the equipment (optional)")
    
    submit = SubmitField('Save Equipment',
        render_kw={"class": "btn btn-primary mt-3"})

    def __init__(self, *args, **kwargs):
        self.equipment = kwargs.pop('equipment', None)
        super(EquipmentForm, self).__init__(*args, **kwargs)

    def validate_sn(self, field):
        if self.equipment and self.equipment.sn == field.data:
            return
        equipment = Equipment.query.filter_by(sn=field.data).first()
        if equipment:
            raise ValidationError('This serial number is already registered.')

class EquipmentSearchForm(FlaskForm):
    search = StringField('Search', validators=[Length(max=100)])
    submit = SubmitField('Search') 