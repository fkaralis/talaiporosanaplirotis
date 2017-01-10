import os
import locale
from datetime import datetime
from threading import Thread
from flask import Flask
from flask import render_template
from flask import session
from flask import redirect
from flask import url_for
from flask import request
from flask import flash
from flask import jsonify
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_migrate import MigrateCommand
from flask_mail import Mail
from flask_mail import Message
from wtforms import StringField
from wtforms import SelectField
from wtforms import SelectMultipleField
from wtforms import SubmitField
from wtforms.validators import Required
from wtforms.validators import DataRequired


#loc = locale.getdefaultlocale()
#locale.setlocale(locale.LC_ALL, loc)
locale.setlocale(locale.LC_ALL, 'ell')

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

# app config db
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'e-aitisi_scraper' + os.sep + 'talaiporosanaplirotis.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = '#@SCJ239asbAS<KCsdfhg7757'

# e-mail
#
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['TALAIPANAP_MAIL_SUBJECT_PREFIX'] = '[TalaipAnap] '
app.config['TALAIPANAP_MAIL_SENDER'] = 'TalaipAnap Admin <fivoskaralis@gmail.com>'
app.config['TALAIPANAP_ADMIN'] = os.environ.get('TALAIPANAP_ADMIN')

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(to, subject, body):
    msg = Message(app.config['TALAIPANAP_MAIL_SUBJECT_PREFIX'] + subject,\
                  sender=app.config['TALAIPANAP_MAIL_SENDER'], recipients=[to])
    msg.body = body
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr

''' tutorial send_mail function
def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,\
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr
'''
#
# e-mail end

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)
mail = Mail(app)

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
choices_sxolika_eth = sorted(choices_sxolika_eth)[:5] # up to 2012-13

for kathgoria in kathgories:
    choice = (kathgoria.kathgoria_id, kathgoria.greek_lektiko_kathgorias)
    choices_kathgories.append(choice)
choices_kathgories = sorted(choices_kathgories, key=lambda x: x[1]) # sort alphabetically

for klados in kladoi:
    choice = (klados.klados_id, klados.kodikos_kladoy+' '+klados.lektiko_kladoy)
    choices_kladoi.append(choice)
choices_kladoi = sorted(choices_kladoi, key=lambda x: x[1]) # sort alphabetically

for hmeromhnia in hmeromhnies:
    choice = (hmeromhnia.hmeromhnia_id, hmeromhnia.real_hmeromhnia)
    choices_hmeromhnies.append(choice)
choices_hmeromhnies = sorted(choices_hmeromhnies, key=lambda x: x[1], reverse=True)  # sort alphabetically decr.

# fix hmeromhnia format (e.g. 10-Οκτ-2016)
for i, choice in enumerate(choices_hmeromhnies):
    choice_list = list(choices_hmeromhnies[i])
    choice_list[1] = '{:%d-%b-%Y}'.format(choice_list[1])
    choices_hmeromhnies[i] = tuple(choice_list)
## end choices


# form class
class Form(FlaskForm):
    sxoliko_etos = SelectField('Σχολικό έτος', choices=choices_sxolika_eth, validators=[DataRequired()], coerce=int, id='select_sxoliko_etos')
    kathgoria = SelectField('Κατηγορία', choices=[], validators=[DataRequired()], coerce=int, id='select_kathgoria')
    klados = SelectField('Κλάδος', choices=[], validators=[DataRequired()], coerce=int, id='select_klados')
    hmeromhnia = SelectField('Ημερομηνία', choices=[], validators=[DataRequired()], coerce=int, id='select_hmeromhnia')
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

    if form.is_submitted():
        sxoliko_etos_id = form.sxoliko_etos.data
        kathgoria_id = form.kathgoria.data
        klados_id = form.klados.data
        hmeromhnia_id = form.hmeromhnia.data
        real_eidikothta_id = Klados.query.filter_by(klados_id=klados_id).first().real_eidikothta_id

        session['sxoliko_etos_id']  = sxoliko_etos_id
        session['kathgoria_id'] = kathgoria_id
        session['klados_id'] = klados_id
        session['hmeromhnia_id'] = hmeromhnia_id
        session['real_eidikothta_id'] = real_eidikothta_id

        if app.config['TALAIPANAP_ADMIN']:
            msg_body = '\n'.join(('Σχολικό έτος id ' + str(sxoliko_etos_id),\
                                  'Κατηγορία id ' + str(kathgoria_id),\
                                  'Κλάδος id ' + str(klados_id),\
                                  'Ημερομηνία id ' + str(hmeromhnia_id),\
                                  'Real ειδικότητα id ' + str(real_eidikothta_id)))
            send_email(app.config['TALAIPANAP_ADMIN'], 'New submit', msg_body)

        return redirect(url_for('result'))

    return render_template('index.html', form=form, current_time=datetime.utcnow())


@app.route('/result', methods=['GET', 'POST'])
def result():
    return render_template('result.html', sxoliko_etos_id=session.get('sxoliko_etos_id'),
                           kathgoria_id=session.get('kathgoria_id'),
                           klados_id=session.get('klados_id'),
                           hmeromhnia_id=session.get('hmeromhnia_id'),
                           real_eidikothta_id=session.get('real_eidikothta_id'))


@app.route('/_get_kathgories/')
def _get_kathgories():
    sxoliko_etos_id = request.args.get('sxoliko_etos')

    pinakes = Pinakas.query.filter_by(sxoliko_etos_id=sxoliko_etos_id).all()
    # kathgoria ids list
    kathgories_id = []
    for pinakas in pinakes:
        temp_kathgoria_id = pinakas.kathgoria_id
        if temp_kathgoria_id not in kathgories_id:
            kathgories_id.append(temp_kathgoria_id)
    # kathgoria choice tuples list
    choices_kathgories = []
    for kathgoria_id in kathgories_id:
        choices_kathgories.append((kathgoria_id, Kathgoria.query.filter_by(kathgoria_id=kathgoria_id).
                          first().greek_lektiko_kathgorias))
    choices_kathgories = sorted(choices_kathgories, key=lambda x: x[1]) # sort alphabetically

    return jsonify(choices_kathgories)


@app.route('/_get_kladoi/')
def _get_kladoi():
    sxoliko_etos_id = request.args.get('sxoliko_etos')
    kathgoria_id = request.args.get('kathgoria')

    pinakes = Pinakas.query.filter_by(sxoliko_etos_id=sxoliko_etos_id, kathgoria_id=kathgoria_id).all()
    # lists ids and choices
    eidikothtes_id = []
    real_eidikothtes_id = []
    choices_kladoi = []
    for pinakas in pinakes:
        temp_eidikothta_id = pinakas.eidikothta_id
        if temp_eidikothta_id not in eidikothtes_id:
            eidikothtes_id.append(temp_eidikothta_id)
            temp_real_eidikothta_id = Eidikothta.query.filter_by(eidikothta_id=temp_eidikothta_id).first().real_eidikothta_id
            if temp_real_eidikothta_id not in real_eidikothtes_id:
                real_eidikothtes_id.append(temp_real_eidikothta_id)
                temp_kladoi = Klados.query.filter_by(real_eidikothta_id=temp_real_eidikothta_id).all()
                for klados in temp_kladoi:
                    choices_kladoi.append((klados.klados_id, klados.kodikos_kladoy + ' ' + klados.lektiko_kladoy))
    choices_kladoi = sorted(choices_kladoi, key=lambda x: x[1])  # sort alphabetically

    return jsonify(choices_kladoi)


@app.route('/_get_hmeromhnies/')
def _get_hmeromhnies():
    sxoliko_etos_id = request.args.get('sxoliko_etos')
    kathgoria_id = request.args.get('kathgoria')
    klados_id = request.args.get('klados')

    print(sxoliko_etos_id)
    print(kathgoria_id)
    print(klados_id)

    real_eidikothta_id = Klados.query.filter_by(klados_id=klados_id).first().real_eidikothta_id
    eidikothtes = Eidikothta.query.filter_by(real_eidikothta_id=real_eidikothta_id).all()
    pinakes = []
    choices_hmeromhnies = []

    for eidikothta in eidikothtes:
        print(eidikothta.eidikothta_id, eidikothta.kodikos_eidikothtas)
        temp_pinakes = Pinakas.query.filter_by(sxoliko_etos_id=sxoliko_etos_id,\
                                               kathgoria_id=kathgoria_id,\
                                               eidikothta_id=eidikothta.eidikothta_id).all()
        for pinakas in temp_pinakes:
            if pinakas not in pinakes:
                pinakes.append(pinakas)

    for pinakas in pinakes:
        print(pinakas.pinakas_id, pinakas.lektiko_pinaka)
        temp_hmeromhnies = Hmeromhnia.query.filter_by(hmeromhnia_id=pinakas.hmeromhnia_id).all()
        for hmeromhnia in temp_hmeromhnies:
            choices_hmeromhnies.append((hmeromhnia.hmeromhnia_id, hmeromhnia.real_hmeromhnia))
    choices_hmeromhnies = sorted(choices_hmeromhnies, key=lambda x: x[1], reverse=True) # sort alphabetically decr.

    # fix hmeromhnia format (e.g. 10-Οκτ-2016)
    for i, choice in enumerate(choices_hmeromhnies):
        choice_list = list(choices_hmeromhnies[i])
        choice_list[1] = '{:%d-%b-%Y}'.format(choice_list[1])
        choices_hmeromhnies[i] = tuple(choice_list)

    return jsonify(choices_hmeromhnies)



@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)
#
# view functions end


if __name__ == '__main__':
    manager.run()