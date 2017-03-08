from flask import render_template
from flask import redirect
from flask import url_for
from flask import flash
from . import auth
from .. import db
from ..models import User
from .forms import RegistrationForm

@auth.route('/login')
def login():
    return render_template('auth/login.html')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    onoma=form.onoma.data)
        db.session.add(user)
        flash('Επιτυχής εγγραφή')
    return render_template('auth/register.html', form=form)