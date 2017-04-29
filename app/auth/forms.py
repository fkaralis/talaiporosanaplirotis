from flask_wtf import FlaskForm
from flask_wtf import RecaptchaField
from wtforms import StringField
from wtforms import PasswordField
from wtforms import BooleanField
from wtforms import SubmitField
from wtforms.validators import Required
from wtforms.validators import Email
from wtforms import ValidationError
from ..models import User


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Email()])
    onoma = StringField('Όνομα', validators=[Required()])
    submit = SubmitField('Εγγραφή')
    recaptcha = RecaptchaField()


    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Το e-mail αυτό υπάρχει ήδη')
