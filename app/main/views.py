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
    hmeromhnia_id = 1

    if form.validate_on_submit():
        sxoliko_etos_id = form.sxoliko_etos.data
        print(sxoliko_etos_id)
        kathgoria_id = form.kathgoria.data
        print(kathgoria_id)
        klados_id = str(form.klados.data)
        print(klados_id)

        if form.smeae_pinakas.data:
            smeae_pinakas_id = form.smeae_pinakas.data
            print(smeae_pinakas_id)
        if form.smeae_kathgoria.data:
            smeae_kathgoria_id = form.smeae_kathgoria.data
            print(smeae_kathgoria_id)
        if form.perioxh.data:
            perioxh_id = form.perioxh.data
            print(perioxh_id)
        if form.mousiko_organo.data:
            mousiko_organo_id = form.mousiko_organo.data
            print(mousiko_organo_id)
        if form.athlima.data:
            athlima_id = form.athlima.data
            print(athlima_id)
        if form.hmeromhnia.data:
            hmeromhnia_id = form.hmeromhnia.data
            print(hmeromhnia_id)

        real_eidikothta_id = Klados.query.filter_by(id=klados_id).first().id
        print(real_eidikothta_id)


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

    smeae_pinakes = []
    smeae_kathgories = []
    perioxes = []
    mousika_organa = []
    athlimata = []
    hmeromhnies = []

    choices_fields = []

    #check smeae pinakas
    pinakes = Pinakas.query.filter_by(sxoliko_etos_id=sxoliko_etos_id,\
                                               kathgoria_id=kathgoria_id).\
                                               filter(and_(Pinakas.klados_id.contains(klados_id),\
                                                           Pinakas.smeae_pinakas_id != 0)).all()
    if len(pinakes) > 0:
        for pinakas in pinakes:
            if pinakas.smeae_pinakas_id not in smeae_pinakes:
                smeae_pinakes.append(pinakas.smeae_pinakas_id)
        choices_fields.append(('smeae_pinakes', smeae_pinakes))


    #check smeae kathgoria
    pinakes = Pinakas.query.filter_by(sxoliko_etos_id=sxoliko_etos_id,\
                                               kathgoria_id=kathgoria_id).\
                                               filter(and_(Pinakas.klados_id.contains(klados_id),\
                                                      Pinakas.smeae_kathgoria_id != 0)).all()
    if len(pinakes) > 0:
        for pinakas in pinakes:
            if pinakas.smeae_kathgoria_id not in smeae_kathgories:
                smeae_kathgories.append(pinakas.smeae_kathgoria_id)
        choices_fields.append(('smeae_kathgories', smeae_kathgories))


    #check perioxh
    pinakes = Pinakas.query.filter_by(sxoliko_etos_id=sxoliko_etos_id,\
                                               kathgoria_id=kathgoria_id).\
                                               filter(and_(Pinakas.klados_id.contains(klados_id),\
                                                      Pinakas.perioxh_id != 0)).all()
    if len(pinakes) > 0:
        for pinakas in pinakes:
            if pinakas.perioxh_id not in perioxes:
                perioxes.append(pinakas.perioxh_id)
        choices_fields.append(('perioxes', perioxes))


    #check mousiko_organo
    pinakes = Pinakas.query.filter_by(sxoliko_etos_id=sxoliko_etos_id,\
                                               kathgoria_id=kathgoria_id).\
                                               filter(and_(Pinakas.klados_id.contains(klados_id),\
                                                      Pinakas.mousiko_organo_id != 0)).all()
    if len(pinakes) > 0:
        for pinakas in pinakes:
            if pinakas.mousiko_organo_id not in mousika_organa:
                mousika_organa.append(pinakas.mousiko_organo_id)
        choices_fields.append(('mousika_organa', mousika_organa))


    #check athlima
    pinakes = Pinakas.query.filter_by(sxoliko_etos_id=sxoliko_etos_id,\
                                               kathgoria_id=kathgoria_id).\
                                               filter(and_(Pinakas.klados_id.contains(klados_id),\
                                                      Pinakas.athlima_id != 0)).all()
    if len(pinakes) > 0:
        for pinakas in pinakes:
            if pinakas.athlima_id not in athlimata:
                athlimata.append(pinakas.athlima_id)
        choices_fields.append(('athlimata', athlimata))


    #check hmeromhnia
    pinakes = Pinakas.query.filter_by(sxoliko_etos_id=sxoliko_etos_id,\
                                               kathgoria_id=kathgoria_id).\
                                               filter(and_(Pinakas.klados_id.contains(klados_id),\
                                                      Pinakas.hmeromhnia_id != 1)).all()
    if len(pinakes) > 0:
        for pinakas in pinakes:
            if pinakas.hmeromhnia_id not in hmeromhnies:
                hmeromhnies.append(pinakas.hmeromhnia_id)
        choices_fields.append(('hmeromhnies', hmeromhnies))


    return jsonify(choices_fields)


@main.route('/_get_smeae_pinakes/')
def _get_smeae_pinakes():
    smeae_pinakes_id = request.args.getlist('ids[]')
    choices_smeae_pinakes = []

    for smeae_pinakas_id in smeae_pinakes_id:
        smeae_pinakas_tuple = (smeae_pinakas_id, Smeae_pinakas.query.filter_by(id=smeae_pinakas_id).one().lektiko)
        if smeae_pinakas_tuple not in choices_smeae_pinakes:
            choices_smeae_pinakes.append(smeae_pinakas_tuple)

    choices_smeae_pinakes = sorted(choices_smeae_pinakes, key=lambda x: x[1])  # sort alphabetically
    choices_smeae_pinakes.insert(0, (0, '--Επιλογή πίνακα--'))

    return jsonify(choices_smeae_pinakes)


@main.route('/_get_smeae_kathgories/')
def _get_smeae_kathgories():
    smeae_kathgories_id = request.args.getlist('ids[]')
    choices_smeae_kathgories = []

    for smeae_kathgoria_id in smeae_kathgories_id:
        smeae_kathgoria_tuple = (smeae_kathgoria_id, Smeae_kathgoria.query.filter_by(id=smeae_kathgoria_id).one().lektiko)
        if smeae_kathgoria_tuple not in choices_smeae_kathgories:
            choices_smeae_kathgories.append(smeae_kathgoria_tuple)

    choices_smeae_kathgories = sorted(choices_smeae_kathgories)  # sort id acc
    choices_smeae_kathgories.insert(0, (0, '--Επιλογή κατηγορίας--'))

    return jsonify(choices_smeae_kathgories)


@main.route('/_get_perioxes/')
def _get_perioxes():
    perioxes_id = request.args.getlist('ids[]')
    choices_perioxes = []

    for perioxh_id in perioxes_id:
        perioxh_tuple = (perioxh_id, Perioxh.query.filter_by(id=perioxh_id).one().lektiko)
        if perioxh_tuple not in choices_perioxes:
            choices_perioxes.append(perioxh_tuple)

    choices_perioxes = sorted(choices_perioxes, key=lambda x: x[1])  # sort alphabetically
    choices_perioxes.insert(0, (0, '--Επιλογή περιοχής--'))

    return jsonify(choices_perioxes)


@main.route('/_get_mousika_organa/')
def _get_mousika_organa():
    mousika_organa_id = request.args.getlist('ids[]')
    choices_mousika_organa = []

    for mousiko_organo_id in mousika_organa_id:
        mousiko_organo_tuple = (mousiko_organo_id, Mousiko_organo.query.filter_by(id=mousiko_organo_id).one().lektiko)
        if mousiko_organo_tuple not in choices_mousika_organa:
            choices_mousika_organa.append(mousiko_organo_tuple)

    choices_mousika_organa = sorted(choices_mousika_organa, key=lambda x: x[1])  # sort alphabetically
    choices_mousika_organa.insert(0, (0, '--Επιλογή μουσικού οργάνου--'))

    return jsonify(choices_mousika_organa)


@main.route('/_get_athlimata/')
def _get_athlimata():
    athlimata_id = request.args.getlist('ids[]')
    choices_athlimata = []

    for athlima_id in athlimata_id:
        athlima_tuple = (athlima_id, Athlima.query.filter_by(id=athlima_id).one().lektiko)
        if athlima_tuple not in choices_athlimata:
            choices_athlimata.append(athlima_tuple)

    choices_athlimata = sorted(choices_athlimata, key=lambda x: x[1])  # sort alphabetically
    choices_athlimata.insert(0, (0, '--Επιλογή αθλήματος--'))

    return jsonify(choices_athlimata)


@main.route('/_get_hmeromhnies/')
def _get_hmeromhnies():
    hmeromhnies_id = request.args.getlist('ids[]')
    choices_hmeromhnies = []

    for hmeromhnia_id in hmeromhnies_id:
        hmeromhnia_tuple = (hmeromhnia_id, Hmeromhnia.query.filter_by(id=hmeromhnia_id).one().real_hmeromhnia)
        if hmeromhnia_tuple not in choices_hmeromhnies:
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
