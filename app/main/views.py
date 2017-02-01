from datetime import datetime
from threading import Thread
from flask import Flask
from flask import current_app
from flask import render_template
from flask import session
from flask import redirect
from flask import url_for
from flask import request
from flask import flash
from flask import jsonify
from ..email import send_email
from . import main
from .forms import MainForm
from .. import db
from ..models import Kathgoria, Real_eidikothta, Klados, Sxoliko_etos, Hmeromhnia,\
Pinakas, Smeae_pinakas, Smeae_kathgoria, Perioxh, Mousiko_organo, Athlima,\
Smeae_kathgoria_greeklish, Perioxh_greeklish, Mousiko_organo_greeklish, Athlima_greeklish
from sqlalchemy import or_
from sqlalchemy import and_



@main.route('/', methods=['GET', 'POST'])
def index():
    form = MainForm()

    smeae_pinakas_id = 0
    smeae_kathgoria_id = 0
    perioxh_id = 0
    mousiko_organo_id = 0
    athlima_id = 0

    if form.validate_on_submit():
        sxoliko_etos_id = form.sxoliko_etos.data
        kathgoria_id = form.kathgoria.data
        klados_id = str(form.klados.data)
        hmeromhnia_id = form.hmeromhnia.data

        if form.smeae_pinakas.data:
            smeae_pinakas_id = form.smeae_pinakas.data
        if form.smeae_kathgoria.data:
            smeae_kathgoria_id = form.smeae_kathgoria.data
        if form.perioxh.data:
            perioxh_id = form.perioxh.data
        if form.mousiko_organo.data:
            mousiko_organo_id = form.mousiko_organo.data
        if form.athlima.data:
            athlima_id = form.athlima.data

        real_eidikothta_id = Klados.query.filter_by(id=klados_id).first().id


        url_pinaka = Pinakas.query.filter_by(sxoliko_etos_id=sxoliko_etos_id,\
                                          kathgoria_id=kathgoria_id,\
                                          hmeromhnia_id=hmeromhnia_id,\
                                          smeae_pinakas_id=smeae_pinakas_id,\
                                          smeae_kathgoria_id=smeae_kathgoria_id,\
                                          perioxh_id=perioxh_id,\
                                          mousiko_organo_id=mousiko_organo_id,\
                                          athlima_id=athlima_id).\
                                          filter(Pinakas.klados_id.contains(klados_id)).\
                                          first().url_pinaka

        session['sxoliko_etos_id']  = sxoliko_etos_id
        session['kathgoria_id'] = kathgoria_id
        session['klados_id'] = klados_id
        session['hmeromhnia_id'] = hmeromhnia_id
        session['smeae_pinakas_id'] = smeae_pinakas_id
        session['smeae_kathgoria_id'] = smeae_kathgoria_id
        session['perioxh_id'] = perioxh_id
        session['mousiko_organo_id'] = mousiko_organo_id
        session['athlima_id'] = athlima_id
        session['real_eidikothta_id'] = real_eidikothta_id
        session['url_pinaka'] = url_pinaka

        if current_app.config['TALAIPANAP_ADMIN']:
            msg_body = '\n'.join(('Σχολικό έτος id ' + str(sxoliko_etos_id),\
                                  'Κατηγορία id ' + str(kathgoria_id),\
                                  'Κλάδος id ' + str(klados_id),\
                                  'Ημερομηνία id ' + str(hmeromhnia_id),\
                                  'Πίνακας ΣΜΕΑΕ id: ' + str(smeae_pinakas_id),\
                                  'Κατηγορία ΣΜΕΑΕ id: ' + str(smeae_kathgoria_id),\
                                  'Περιοχή id' + str(perioxh_id),\
                                  'Μουσικό όργανο id: ' + str(mousiko_organo_id),\
                                  'Άθλημα id: ' + str(athlima_id),\
                                  'Real ειδικότητα id ' + str(real_eidikothta_id),\
                                  url_pinaka))
            send_email(current_app.config['TALAIPANAP_ADMIN'], 'New submit', msg_body)

        return redirect(url_for('main.result'))

    return render_template('index.html', form=form)


@main.route('/result', methods=['GET', 'POST'])
def result():
    return render_template('result.html', sxoliko_etos_id=session.get('sxoliko_etos_id'),
                           kathgoria_id=session.get('kathgoria_id'),
                           klados_id=session.get('klados_id'),
                           hmeromhnia_id=session.get('hmeromhnia_id'),
                           smeae_pinakas_id=session.get('smeae_pinakas_id'),
                           smeae_kathgoria_id=session.get('smeae_kathgoria_id'),
                           perioxh_id=session.get('perioxh_id'),
                           mousiko_organo_id=session.get('mousiko_organo_id'),
                           athlima_id=session.get('athlima_id'),
                           real_eidikothta_id=session.get('real_eidikothta_id'),
                           url_pinaka = session.get('url_pinaka'))


@main.route('/_get_kathgories/')
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
        choices_kathgories.append((kathgoria_id, Kathgoria.query.filter_by(id=kathgoria_id).
                          first().greek_lektiko_kathgorias))
    choices_kathgories = sorted(choices_kathgories, key=lambda x: x[1]) # sort alphabetically
    choices_kathgories.insert(0, (0, '--Επιλογή κατηγορίας--'))

    return jsonify(choices_kathgories)


@main.route('/_get_kladoi/')
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
            klados = Klados.query.filter_by(id=klados_id).first()
            if klados.id != 254:     # not Bad or No File
                klados_tuple = (klados.id, klados.kodikos_kladoy + ' ' + klados.lektiko_kladoy)
            if klados_tuple not in choices_kladoi:
                choices_kladoi.append(klados_tuple)

    choices_kladoi = sorted(choices_kladoi, key=lambda x: x[1])  # sort alphabetically
    choices_kladoi.insert(0, (0, '--Επιλογή κλάδου--'))

    return jsonify(choices_kladoi)


@main.route('/_get_fields/')
def _get_fields():
    sxoliko_etos_id = request.args.get('sxoliko_etos')
    kathgoria_id = request.args.get('kathgoria')
    klados_id = request.args.get('klados')

    pinakes = Pinakas.query.filter_by(sxoliko_etos_id=sxoliko_etos_id,\
                                               kathgoria_id=kathgoria_id).\
                                               filter(Pinakas.klados_id.contains(klados_id)).all()

    smeae_pinakas = False
    smeae_kathgoria = False
    perioxh = False
    mousiko_organo = False
    athlima = False

    if len(Pinakas.query.filter_by(sxoliko_etos_id=sxoliko_etos_id,\
                                               kathgoria_id=kathgoria_id).\
                                               filter(and_(Pinakas.klados_id.contains(klados_id),
                                                      Pinakas.smeae_pinakas_id != 0)).all()) > 0:
           smeae_pinakas = True

    if len(Pinakas.query.filter_by(sxoliko_etos_id=sxoliko_etos_id,\
                                               kathgoria_id=kathgoria_id).\
                                               filter(and_(Pinakas.klados_id.contains(klados_id),
                                                      Pinakas.smeae_kathgoria_id != 0)).all()) > 0:
           smeae_kathgoria = True

    if len(Pinakas.query.filter_by(sxoliko_etos_id=sxoliko_etos_id,\
                                               kathgoria_id=kathgoria_id).\
                                               filter(and_(Pinakas.klados_id.contains(klados_id),
                                                      Pinakas.perioxh_id != 0)).all()) > 0:
           perioxh = True


    if len(Pinakas.query.filter_by(sxoliko_etos_id=sxoliko_etos_id,\
                                               kathgoria_id=kathgoria_id).\
                                               filter(and_(Pinakas.klados_id.contains(klados_id),
                                                      Pinakas.mousiko_organo_id != 0)).all()) > 0:
           mousiko_organo = True


    if len(Pinakas.query.filter_by(sxoliko_etos_id=sxoliko_etos_id,\
                                               kathgoria_id=kathgoria_id).\
                                               filter(and_(Pinakas.klados_id.contains(klados_id),
                                                      Pinakas.athlima_id != 0)).all()) > 0:
           athlima = True

    return jsonify([('smeae_pinakas',smeae_pinakas),\
                      ('smeae_kathgoria',smeae_kathgoria),\
                      ('perioxh',perioxh),\
                      ('mousiko_organo',mousiko_organo),\
                      ('athlima',athlima)])



@main.route('/_get_hmeromhnies/')
def _get_hmeromhnies():
    sxoliko_etos_id = request.args.get('sxoliko_etos')
    kathgoria_id = request.args.get('kathgoria')
    klados_id = request.args.get('klados')

    pinakes = []
    choices_hmeromhnies = []

    pinakes = Pinakas.query.filter_by(sxoliko_etos_id=sxoliko_etos_id,\
                                               kathgoria_id=kathgoria_id).\
                                               filter(Pinakas.klados_id.contains(klados_id)).all()

    for pinakas in pinakes:
        hmeromhnia = Hmeromhnia.query.filter_by(id=pinakas.hmeromhnia_id).first()
        hmeromhnia_tuple = (hmeromhnia.id, hmeromhnia.real_hmeromhnia)
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
@main.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)
#
# view functions end


'''
    smeae_pinakes_id = []
    smeae_kathgories_id = []
    perioxes_id = []
    mousika_organa_id = []
    athlimata_id = []

    for pinakas in pinakes:
        smeae_pinakas_id = pinakas.smeae_pinakas_id
        smeae_kathgoria_id = pinakas.smeae_kathgoria_id
        perioxh_id = pinakas.perioxh_id
        mousiko_organo_id = pinakas.mousiko_organo_id
        athlima_id = pinakas.athlima_id

        if smeae_pinakas_id !=0 and smeae_pinakas_id not in smeae_pinakes_id:
            smeae_pinakes_id.append(smeae_pinakas_id)
        if smeae_kathgoria_id !=0 and smeae_kathgoria_id not in smeae_kathgories_id:
            smeae_kathgories_id.append(smeae_kathgoria_id)
        if perioxh_id !=0 and perioxh_id not in perioxes_id:
            perioxes_id.append(perioxh_id)
        if mousiko_organo_id !=0 and mousiko_organo_id not in mousika_organa_id:
            mousika_organa_id.append(mousiko_organo_id)
        if athlima_id !=0 and athlima_id not in athlimata_id:
            athlimata_id.append(athlima_id)

'''