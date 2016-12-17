import os
from flask import Flask
from flask import render_template
from flask import session
from flask import redirect
from flask import url_for
from flask import request
from flask import flash
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, SelectField, SelectMultipleField, SubmitField
from wtforms.validators import Required
from datetime import datetime


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'e-aitisi_scraper/talaiporosanaplirotis.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = '#@SCJ239asbAS<KCsdfhg7757'

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)

# talaiporosanaplirotis.sqlite Model
#
db.Model.metadata.reflect(db.engine)

class Eidikothta(db.Model):
    __table__ = db.Model.metadata.tables['eidikothta']

    def __repr__(self):
        return '\nΕιδικότητα id %r\nκωδικός %r\nreal %r' %\
            (self.eidikothta_id, self.kodikos_eidikothtas, self.real_eidikothta_id)

class Hmeromhnia(db.Model):
    __table__ = db.Model.metadata.tables['hmeromhnia']

    def __repr__(self):
        return '\nΗμερομηνία id %r\nλεκτικό %r\nπρ. ημ/νία %r' %\
            (self.hmeromhnia_id, self.lektiko_hmeromhnias, self.real_hmeromhnia)

class Kathgoria(db.Model):
    __table__ = db.Model.metadata.tables['kathgoria']

    def __repr__(self):
        return '\nΚατηγορία id %r\nλεκτικό %r' %\
            (self.kathgoria_id, self.lektiko_kathgorias)

class Klados(db.Model):
    __table__ = db.Model.metadata.tables['klados']

    def __repr__(self):
        return '\nΚλάδος id %r\nκωδικός %r\nλεκτικό %r\nreal %r' %\
            (self.klados_id, self.kodikos_kladoy, self.lektiko_kladoy, self.real_eidikothta_id)

class Pinakas(db.Model):
    __table__ = db.Model.metadata.tables['pinakas']

    def __repr__(self):
        return '\nΠίνακας id %r\nλεκτικό %r\nσχ.έτος %r\nκατηγορία %r\nειδικότητα %r\nημ/νια %r\npath %r\nurl %r' %\
            (self.pinakas_id, self.lektiko_pinaka, self.sxoliko_etos_id, self.kathgoria_id, \
             self.eidikothta_id, self.hmeromhnia_id, self.path_pinaka, self.url_pinaka)

class Real_eidikothta(db.Model):
    __table__ = db.Model.metadata.tables['real_eidikothta']

    def __repr__(self):
        return '\nΠραγματική ειδικότητα\nid %r\nκωδικός %r\nλεκτικό %r' %\
            (self.real_eidikothta_id, self.kodikos_real_eidikothtas, self.lektiko_real_eidikothtas)

class Sxoliko_etos(db.Model):
    __table__ = db.Model.metadata.tables['sxoliko_etos']

    def __repr__(self):
        return '\nΣχολικό έτος\nid %r\nλεκτικό %r' %\
            (self.sxoliko_etos_id, self.lektiko_sxolikoy_etoys)
#
# Model end


# main page form
#
## gather choices
choices_sxolika_eth = []
choices_kathgories = []
choices_kladoi = []
choices_hmeromhnies = []

sxolika_eth = Sxoliko_etos.query.all()
kathgories = Kathgoria.query.all()
kladoi = Klados.query.all()
hmeromhnies = Hmeromhnia.query.all()

for sxoliko_etos in sxolika_eth:
    choice = (sxoliko_etos.sxoliko_etos_id, sxoliko_etos.lektiko_sxolikoy_etoys)
    choices_sxolika_eth.append(choice)
choices_sxolika_eth = sorted(choices_sxolika_eth, reverse=True)

for kathgoria in kathgories:
    choice = (kathgoria.kathgoria_id, kathgoria.lektiko_kathgorias)
    choices_kathgories.append(choice)
choices_kathgories = sorted(choices_kathgories)

for klados in kladoi:
    choice = (klados.klados_id, klados.kodikos_kladoy+' '+klados.lektiko_kladoy)
    choices_kladoi.append(choice)
choices_kladoi = sorted(choices_kladoi, key=lambda x: x[1])

for hmeromhnia in hmeromhnies:
    choice = (hmeromhnia.hmeromhnia_id, hmeromhnia.real_hmeromhnia)
    choices_hmeromhnies.append(choice)
choices_hmeromhnies = sorted(choices_hmeromhnies)

# form class
class Form(FlaskForm):
    sxoliko_etos = SelectField('Σχολικό έτος', choices=choices_sxolika_eth, validators=[Required()])
    kathgoria = SelectField('Κατηγορία', choices=choices_kathgories, validators=[Required()])
    klados = SelectField('Κλάδος', choices=choices_kladoi, validators=[Required()])
    hmeromhnia = SelectField('Ημερομηνία', choices=choices_hmeromhnies, validators=[Required()])
    submit = SubmitField('Yποβολή')
#
# form end


# view functions
#
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500



@app.route('/', methods=['GET', 'POST'])
def index():
    form = Form()

    if form.submit.data:
        session['sxoliko_etos']  = form.sxoliko_etos.data
        session['kathgoria'] = form.kathgoria.data
        session['klados'] = form.klados.data
        session['hmeromhnia'] = form.hmeromhnia.data

        return redirect(url_for('result'))

    return render_template('index.html', form=form, current_time=datetime.utcnow())


@app.route('/result', methods=['GET', 'POST'])
def result():
    return render_template('result.html', sxoliko_etos=session.get('sxoliko_etos'),
                           kathgoria=session.get('kathgoria'),
                           klados=session.get('klados'),
                           hmeromhnia=session.get('hmeromhnia'))


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)
#
# view functions end


if __name__ == '__main__':
    manager.run()