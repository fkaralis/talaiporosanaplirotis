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
from wtforms import StringField, SubmitField
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



class NameForm(FlaskForm):
    name = StringField('Σχολικό έτος', validators=[Required()])
    submit = SubmitField('Δώσε')



@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500



@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()

    if form.validate_on_submit():
        sxoliko_etos = Sxoliko_etos.query.filter_by(lektiko_sxolikoy_etoys=form.name.data).first()
        if sxoliko_etos is not None:
            sxoliko_etos_id = sxoliko_etos.sxoliko_etos_id
            lektiko_sxolikoy_etoys = sxoliko_etos.lektiko_sxolikoy_etoys
        else:
            sxoliko_etos_id = None
            lektiko_sxolikoy_etoys = None
        session['sxoliko_etos_id'] = sxoliko_etos_id
        session['lektiko_sxolikoy_etoys'] = lektiko_sxolikoy_etoys
        form.name.data = ''
        return redirect(url_for('index'))

    return render_template('index.html', form=form,
                           sxoliko_etos_id=session.get('sxoliko_etos_id'),
                           lektiko_sxolikoy_etoys=session.get('lektiko_sxolikoy_etoys'),
                           current_time=datetime.utcnow())


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


if __name__ == '__main__':
    manager.run()