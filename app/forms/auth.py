from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from app.models.tables import User

class LoginForm(FlaskForm):
    staffno = IntegerField('Staff Number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')

class RegistrationForm(FlaskForm):
    staffno = IntegerField('Staff Number', validators=[DataRequired()])
    staffname = StringField('Staff Name', validators=[DataRequired(), Length(min=2, max=100)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    isadmin = BooleanField('Is Admin')

    def validate_staffno(self, staffno):
        user = User.query.filter_by(staffno=staffno.data).first()
        if user:
            raise ValidationError('Staff number already registered.') 