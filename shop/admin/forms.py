from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators
from wtforms.validators import ValidationError
from wtforms.fields import EmailField
from .models import User


class RegistrationForm(FlaskForm):
    name = StringField(_l('Name'), [validators.Length(min=1, max=25)])
    username = StringField(_l('Username'), [validators.Length(min=1, max=30)])
    email = EmailField(_l('Email Address'), [validators.Length(min=6, max=35)])
    password = PasswordField(_l('New Password'), [validators.DataRequired(), validators.EqualTo('password', message='Passwords must match')])
    confirm = PasswordField(_l('Repeat Password'))

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(_l('Username already in use.'))
    
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(_l('Email already registered.'))


class LoginForm(FlaskForm):
    email = StringField(_l('Email'), [validators.Length(min=6, max=35)])
    password = PasswordField(_l('Password'), [validators.DataRequired()])