from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from app.models.tables import User

class UserForm(FlaskForm):
    staffno = IntegerField('Staff Number', validators=[DataRequired()])
    staffname = StringField('Staff Name', validators=[DataRequired(), Length(min=2, max=100)])
    password = PasswordField('Password', validators=[Length(min=6)])
    password2 = PasswordField('Repeat Password', validators=[EqualTo('password')])
    isadmin = BooleanField('Administrator Access')
    submit = SubmitField('Submit')

    def __init__(self, original_staffno=None, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.original_staffno = original_staffno

    def validate_staffno(self, staffno):
        if self.original_staffno is None or staffno.data != self.original_staffno:
            user = User.query.filter_by(staffno=staffno.data).first()
            if user is not None:
                raise ValidationError('Please use a different staff number.') 