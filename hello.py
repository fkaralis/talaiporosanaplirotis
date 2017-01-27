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

# linux locale
loc = locale.getdefaultlocale()
locale.setlocale(locale.LC_ALL, loc)
# win locale
#locale.setlocale(locale.LC_ALL, 'ell')

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
             self.hmeromhnia_id, self.path_pinaka, self.url_pinaka)

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

class Smeae_pinakas(db.Model):
    __table__ = db.Model.metadata.tables['smeae_pinakas']

    def __repr__(self):
        return '\nΣΜΕΑΕ Πίνακας\nid %r\nλεκτικό %r' %\
            (self.id, self.lektiko)

class Smeae_kathgoria(db.Model):
    __table__ = db.Model.metadata.tables['smeae_kathgoria']

    def __repr__(self):
        return '\nΣΜΕΑΕ Κατηγορία\nid %r\nλεκτικό %r' %\
            (self.id, self.lektiko)

class Smeae_kathgoria_greeklish(db.Model):
    __table__ = db.Model.metadata.tables['smeae_kathgoria_greeklish']

    def __repr__(self):
        return '\nΣΜΕΑΕ Κατηγορία grklsh\nid %r\nλεκτικό %r\nΣΜΕΑΕ κατηγορία id' %\
            (self.id, self.lektiko, self.smeae_kathgoria_id)

class Perioxh(db.Model):
    __table__ = db.Model.metadata.tables['perioxh']

    def __repr__(self):
        return '\nΣΜΕΑΕ Περιοχή\nid %r\nλεκτικό %r' %\
            (self.id, self.lektiko)

class Perioxh_greeklish(db.Model):
    __table__ = db.Model.metadata.tables['perioxh_greeklish']

    def __repr__(self):
        return '\nΠεριοχή grklsh\nid %r\nλεκτικό %r\nΠεριοχή id' %\
            (self.id, self.lektiko, self.perioxh_id)

class Mousiko_organo(db.Model):
    __table__ = db.Model.metadata.tables['mousiko_organo']

    def __repr__(self):
        return '\nΜουσικό όργανο\nid %r\nλεκτικό %r' %\
            (self.id, self.lektiko)

class Mousiko_organo_greeklish(db.Model):
    __table__ = db.Model.metadata.tables['mousiko_organo_greeklish']

    def __repr__(self):
        return '\Μουσικό όργανο grklsh\nid %r\nλεκτικό %r\nΜουσικό όργανο id' %\
            (self.id, self.lektiko, self.mousiko_organo_id)

class Athlima(db.Model):
    __table__ = db.Model.metadata.tables['athlima']

    def __repr__(self):
        return '\nΆθλημα\nid %r\nλεκτικό %r' %\
            (self.id, self.lektiko)

class Athlima_greeklish(db.Model):
    __table__ = db.Model.metadata.tables['athlima_greeklish']

    def __repr__(self):
        return '\nΆθλημα grklsh\nid %r\nλεκτικό %r\Άθλημα id' %\
            (self.id, self.lektiko, self.athlima_id)
#
# Model end


# main page form
#
## gather choices
choices_sxolika_eth = []
choices_kathgories = []
choices_kladoi = []
choices_hmeromhnies = []
choices_smeae_pinakes = []
choices_smeae_kathgories = []
choices_perioxes = []
choices_mousika_organa = []
choices_athlimata = []

sxolika_eth = Sxoliko_etos.query.all()
kathgories = Kathgoria.query.all()
kladoi = Klados.query.all()
hmeromhnies = Hmeromhnia.query.all()
smeae_pinakes = Smeae_pinakas.query.all()
smeae_kathgories = Smeae_kathgoria.query.all()
perioxes = Perioxh.query.all()
mousika_organa = Mousiko_organo.query.all()
athlimata = Athlima.query.all()

for sxoliko_etos in sxolika_eth:
    choice = (sxoliko_etos.sxoliko_etos_id, sxoliko_etos.lektiko_sxolikoy_etoys)
    choices_sxolika_eth.append(choice)
choices_sxolika_eth = sorted(choices_sxolika_eth)[:5] # up to 2012-13
choices_sxolika_eth.insert(0, (0, '--Επιλογή σχ. έτους--'))

for kathgoria in kathgories:
    choice = (kathgoria.kathgoria_id, kathgoria.greek_lektiko_kathgorias)
    choices_kathgories.append(choice)
choices_kathgories = sorted(choices_kathgories, key=lambda x: x[1]) # sort alphabetically
choices_kathgories.insert(0, (0, '--Επιλογή κατηγορίας--'))

for klados in kladoi:
    choice = (klados.klados_id, klados.kodikos_kladoy+' '+klados.lektiko_kladoy)
    choices_kladoi.append(choice)
choices_kladoi = sorted(choices_kladoi, key=lambda x: x[1]) # sort alphabetically
choices_kladoi.insert(0, (0, '--Επιλογή κλάδου--'))

for hmeromhnia in hmeromhnies:
    choice = (hmeromhnia.hmeromhnia_id, hmeromhnia.real_hmeromhnia)
    choices_hmeromhnies.append(choice)
choices_hmeromhnies = sorted(choices_hmeromhnies, key=lambda x: x[1], reverse=True)  # sort alphabetically decr.

# fix hmeromhnia format (e.g. 10-Οκτ-2016)
for i, choice in enumerate(choices_hmeromhnies):
    choice_list = list(choices_hmeromhnies[i])
    choice_list[1] = '{:%d-%b-%Y}'.format(choice_list[1])
    choices_hmeromhnies[i] = tuple(choice_list)
choices_hmeromhnies.insert(0, (0, '--Επιλογή ημ/νίας--'))

for smeae_pinakas in smeae_pinakes:
    choice = (smeae_pinakas.id, smeae_pinakas.lektiko)
    choices_smeae_pinakes.append(choice)
choices_smeae_pinakes = sorted(choices_smeae_pinakes, key=lambda x: x[1]) # sort alphabetically
choices_smeae_pinakes.insert(0, (0, '--Επιλογή πίνακα ΣΜΕΑΕ--'))

for smeae_kathgoria in smeae_kathgories:
    choice = (smeae_kathgoria.id, smeae_kathgoria.lektiko)
    choices_smeae_kathgories.append(choice)
choices_smeae_kathgories.insert(0, (0, '--Επιλογή κατηγορίας ΣΜΕΑΕ--'))

for perioxh in perioxes:
    choice = (perioxh.id, perioxh.lektiko)
    choices_perioxes.append(choice)
choices_perioxes = sorted(choices_perioxes, key=lambda x: x[1]) # sort alphabetically
choices_perioxes.insert(0, (0, '--Επιλογή περιοχής--'))

for mousiko_organo in mousika_organa:
    choice = (mousiko_organo.id, mousiko_organo.lektiko)
    choices_mousika_organa.append(choice)
choices_mousika_organa = sorted(choices_mousika_organa, key=lambda x: x[1]) # sort alphabetically
choices_mousika_organa.insert(0, (0, '--Επιλογή περιοχής--'))

for athlima in athlimata:
    choice = (athlima.id, athlima.lektiko)
    choices_athlimata.append(choice)
choices_athlimata = sorted(choices_athlimata, key=lambda x: x[1]) # sort alphabetically
choices_athlimata.insert(0, (0, '--Επιλογή αθλήματος--'))

## end choices




# form class
class Form(FlaskForm):
    sxoliko_etos = SelectField('Σχολικό έτος',\
                               choices=choices_sxolika_eth,\
                               validators=[DataRequired()],\
                               coerce=int,\
                               id='select_sxoliko_etos')
    kathgoria = SelectField('Κατηγορία',\
                            choices=choices_kathgories,\
                            validators=[DataRequired()],\
                            coerce=int,\
                            id='select_kathgoria')
    smeae_pinakas = SelectField('Πίνακας ΣΜΕΑΕ',\
                                choices=choices_smeae_pinakes,\
                                coerce=int,\
                                id='select_smeae_pinakas')
    smeae_kathgoria = SelectField('Κατηγορία για ΣΜΕΑΕ',\
                        choices=choices_smeae_kathgories,\
                        coerce=int,\
                        id='select_smeae')
    klados = SelectField('Κλάδος',\
                         choices=choices_kladoi,\
                         validators=[DataRequired()],\
                         coerce=int, id='select_klados')
    hmeromhnia = SelectField('Ημερομηνία',\
                             choices=choices_hmeromhnies,\
                             validators=[DataRequired()],\
                             coerce=int,\
                             id='select_hmeromhnia')
    perioxh = SelectField('Περιοχή',\
                             choices=choices_perioxes,\
                             validators=[DataRequired()],\
                             coerce=int,\
                             id='select_perioxh')
    mousiko_organo = SelectField('Mουσικό όργανο',\
                             choices=choices_mousika_organa,\
                             validators=[DataRequired()],\
                             coerce=int,\
                             id='select_mousiko_organo')
    athlima = SelectField('Άθλημα',\
                             choices=choices_athlimata,\
                             validators=[DataRequired()],\
                             coerce=int,\
                             id='select_athlima')
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

    if form.validate_on_submit():
        sxoliko_etos_id = form.sxoliko_etos.data
        kathgoria_id = form.kathgoria.data
        if form.smeae_pinakas.data:
            smeae_pinakas_id = form.smeae_pinakas.data
        else:
            smeae_pinakas_id = 0
        if form.smeae_kathgoria.data:
            smeae_kathgoria_id = form.smeae_kathgoria.data
        else:
            smeae_kathgoria_id = 0
        klados_id = str(form.klados.data)
        hmeromhnia_id = form.hmeromhnia.data
        real_eidikothta_id = Klados.query.filter_by(klados_id=klados_id).first().real_eidikothta_id

        url_pinaka = Pinakas.query.filter_by(sxoliko_etos_id=sxoliko_etos_id,\
                                          kathgoria_id=kathgoria_id,\
                                          hmeromhnia_id=hmeromhnia_id).\
                                          filter(Pinakas.klados_id.contains(klados_id)).\
                                          first().url_pinaka

        session['sxoliko_etos_id']  = sxoliko_etos_id
        session['kathgoria_id'] = kathgoria_id
        session['smeae_pinakas_id'] = smeae_pinakas_id
        session['smeae_kathgoria_id'] = smeae_kathgoria_id
        session['klados_id'] = klados_id
        session['hmeromhnia_id'] = hmeromhnia_id
        session['real_eidikothta_id'] = real_eidikothta_id
        session['url_pinaka'] = url_pinaka

        if app.config['TALAIPANAP_ADMIN']:
            msg_body = '\n'.join(('Σχολικό έτος id ' + str(sxoliko_etos_id),\
                                  'Κατηγορία id ' + str(kathgoria_id),\
                                  'Πίνακας ΣΜΕΑΕ id' + str(smeae_pinakas_id),\
                                  'Κατηγορία ΣΜΕΑΕ id: ' + str(smeae_kathgoria_id),\
                                  'Κλάδος id ' + str(klados_id),\
                                  'Ημερομηνία id ' + str(hmeromhnia_id),\
                                  'Real ειδικότητα id ' + str(real_eidikothta_id),\
                                  url_pinaka))
            send_email(app.config['TALAIPANAP_ADMIN'], 'New submit', msg_body)

        return redirect(url_for('result'))

    return render_template('index.html', form=form)


@app.route('/result', methods=['GET', 'POST'])
def result():
    return render_template('result.html', sxoliko_etos_id=session.get('sxoliko_etos_id'),
                           kathgoria_id=session.get('kathgoria_id'),
                           smeae_pinakas_id=session.get('smeae_pinakas_id'),
                           smeae_kathgoria_id=session.get('smeae_kathgoria_id'),
                           klados_id=session.get('klados_id'),
                           hmeromhnia_id=session.get('hmeromhnia_id'),
                           real_eidikothta_id=session.get('real_eidikothta_id'),
                           url_pinaka = session.get('url_pinaka'))


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
    choices_kathgories.insert(0, (0, '--Επιλογή κατηγορίας--'))

    return jsonify(choices_kathgories)


@app.route('/_get_kladoi/')
def _get_kladoi():
    sxoliko_etos_id = request.args.get('sxoliko_etos')
    kathgoria_id = request.args.get('kathgoria')

    pinakes = Pinakas.query.filter_by(sxoliko_etos_id=sxoliko_etos_id, kathgoria_id=kathgoria_id).all()
    # lists ids and choices
    choices_kladoi = []
    for pinakas in pinakes:
        kladoi_id = pinakas.klados_id
        kladoi_id = kladoi_id.split(' ')
        for klados_id in kladoi_id:
            klados = Klados.query.filter_by(klados_id=klados_id).first()
            if klados.klados_id != 254:     # not Bad or No File
                klados_tuple = (klados.klados_id, klados.kodikos_kladoy + ' ' + klados.lektiko_kladoy)
            if klados_tuple not in choices_kladoi:
                choices_kladoi.append(klados_tuple)

    choices_kladoi = sorted(choices_kladoi, key=lambda x: x[1])  # sort alphabetically
    choices_kladoi.insert(0, (0, '--Επιλογή κλάδου--'))

    return jsonify(choices_kladoi)


@app.route('/_get_hmeromhnies/')
def _get_hmeromhnies():
    sxoliko_etos_id = request.args.get('sxoliko_etos')
    kathgoria_id = request.args.get('kathgoria')
    klados_id = request.args.get('klados')

    klados = Klados.query.filter_by(klados_id=klados_id).first()
    real_eidikothta_id = klados.real_eidikothta_id
    pinakes = []
    choices_hmeromhnies = []

    pinakes = Pinakas.query.filter_by(sxoliko_etos_id=sxoliko_etos_id,\
                                               kathgoria_id=kathgoria_id).\
                                               filter(Pinakas.klados_id.contains(klados_id)).all()

    for pinakas in pinakes:
        hmeromhnia = Hmeromhnia.query.filter_by(hmeromhnia_id=pinakas.hmeromhnia_id).first()
        hmeromhnia_tuple = (hmeromhnia.hmeromhnia_id, hmeromhnia.real_hmeromhnia)
        if hmeromhnia_tuple not in choices_hmeromhnies:
            #print(hmeromhnia_tuple, pinakas.pinakas_id)
            choices_hmeromhnies.append(hmeromhnia_tuple)
    choices_hmeromhnies = sorted(choices_hmeromhnies, key=lambda x: x[1], reverse=True) # sort alphabetically decr.

    # fix hmeromhnia format (e.g. 10-Οκτ-2016)
    for i, choice in enumerate(choices_hmeromhnies):
        choice_list = list(choices_hmeromhnies[i])
        choice_list[1] = '{:%d-%b-%Y}'.format(choice_list[1])
        choices_hmeromhnies[i] = tuple(choice_list)

    choices_hmeromhnies.insert(0, (0, '--Επιλογή ημ/νίας--'))

    return jsonify(choices_hmeromhnies)


# tutorial leftover
@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)
#
# view functions end


if __name__ == '__main__':
    manager.run()