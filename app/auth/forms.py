from flask_wtf import Form
from wtforms import StringField
from wtforms import PasswordField
from wtforms import BooleanField
from wtforms import SubmitField
from wtforms.validators import Required
from wtforms.validators import Email
from wtforms import ValidationError


class LoginForm(Form):
    email = StringField('Email', validators=[Required(), Email()])
    password = PasswordField('Κωδικός', validators=[Required()])
    remember_me = BooleanField('Διατήρηση σύνδεσης')
    submit = SubmitField('Είσοδος')


class RegistrationForm(Form):
    onoma = StringField('Όνομα', validators=[Required()])
    email = StringField('Email', validators=[Required(), Email()])
    submit = SubmitField('Εγγραφή')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Το e-mail αυτό υπάρχει ήδη')