from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.fields import EmailField
from wtforms import StringField, IntegerField, TextAreaField, PasswordField, SubmitField, validators, ValidationError
from .models import Register


class CustomerRegisterForm(FlaskForm):
    name = StringField(_l('Name: '))
    username = StringField(_l('Username: '), [validators.DataRequired()])
    email = EmailField(_l('Email: '), [validators.DataRequired()])
    password = PasswordField(_l('Password: '), [validators.DataRequired(), validators.EqualTo('confirm', message='Both password must match')])
    confirm = PasswordField(_l('Repeat Password: '), [validators.DataRequired()])
    country = StringField(_l('Country: '), [validators.DataRequired()])
    city = StringField(_l('City: '), [validators.DataRequired()])
    contact = IntegerField(_l('Contact: '), [validators.DataRequired()])
    address = StringField(_l('Address: '), [validators.DataRequired()])
    zipcode = IntegerField(_l('Zipcode: '), [validators.DataRequired()])

    profile = FileField(_l('Profile: '), validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Image only please')])

    submit = SubmitField(_l('Submit'))

    def validate_username(self, username):
        if Register.query.filter_by(username=username.data).first():
            raise ValidationError(_l('This username is already exist'))
        
    def validate_email(self, email):
        if Register.query.filter_by(email=email.data).first():
            raise ValidationError(_l('This email is already exist'))
        

class CustomerLoginForm(FlaskForm):
    email = EmailField(_l('Email'), [validators.DataRequired()])
    password = PasswordField(_l('Password'), [validators.DataRequired()])