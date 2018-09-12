from datetime import datetime
from threading import Thread
import gzip
import os
import shutil
import pandas as pd
import json
import random
import time
import atexit
import apscheduler
import glob

from pathlib import PurePosixPath
from pathlib import Path

from flask import Flask
from flask import current_app
from flask import render_template
from flask import session
from flask import redirect
from flask import url_for
from flask import request
from flask import flash
from flask import jsonify
from flask import send_from_directory
from flask import after_this_request
from ..email import send_email
from . import main
from .forms import MainForm
from .. import db
from ..models import User, Kathgoria, Real_eidikothta, Klados, Sxoliko_etos, Hmeromhnia,\
Pinakas, Smeae_pinakas, Smeae_kathgoria, Perioxh, Mousiko_organo, Athlima,\
Smeae_kathgoria_greeklish, Perioxh_greeklish, Mousiko_organo_greeklish, Athlima_greeklish
from sqlalchemy import or_
from sqlalchemy import and_

from .utils import unzip_to_df
from .utils import match_klados

from apscheduler.schedulers.background import BackgroundScheduler

base_dir = current_app.config['BASE_DIR']
data_path = current_app.config['DATA_PATH']
temp_path = current_app.config['TEMP_PATH']

#create temp_path directory if not exists
temp_path = Path(temp_path)
temp_path.mkdir(exist_ok=True, parents=True)
# temp_path string
temp_path = str(temp_path)

@main.route('/', methods=['GET', 'POST'])
def index():
    form = MainForm()

    smeae_pinakas_id = 0
    smeae_pinakas_lektiko = ''

    smeae_kathgoria_id = 0
    smeae_kathgoria_lektiko = ''

    perioxh_id = 0
    perioxh_lektiko = ''

    mousiko_organo_id = 0
    mousiko_organo_lektiko = ''

    athlima_id = 0
    athlima_lektiko = ''

    hmeromhnia_id = 1
    hmeromhnia_real = ''
    hmeromhnia_lektiko = ''

    download_filename = ''

    if form.is_submitted():
        sxoliko_etos_id = form.sxoliko_etos.data
        sxoliko_etos_lektiko = Sxoliko_etos.query.filter_by(id=sxoliko_etos_id).\
                                first().lektiko_sxolikoy_etoys
        print('sx. etos', sxoliko_etos_id, sxoliko_etos_lektiko)

        kathgoria_id = form.kathgoria.data
        kathgoria_lektiko = Kathgoria.query.filter_by(id=kathgoria_id).\
                            first().greek_lektiko_kathgorias
        print('kathgoria', kathgoria_id, kathgoria_lektiko)

        klados_id = str(form.klados.data)
        klados_kodikos = Klados.query.filter_by(id=klados_id).\
                            first().kodikos_kladoy
        klados_lektiko = Klados.query.filter_by(id=klados_id).\
                            first().lektiko_kladoy
        print('klados', klados_id, klados_kodikos, klados_lektiko)

        #building download_filename
        download_filename = klados_kodikos + ' ' + kathgoria_lektiko

        if form.smeae_pinakas.data:
            smeae_pinakas_id = form.smeae_pinakas.data
            smeae_pinakas_lektiko = Smeae_pinakas.query.filter_by(id=smeae_pinakas_id).\
                                    first().lektiko
            print('sm pin', smeae_pinakas_id, smeae_pinakas_lektiko)
            download_filename += ' ' + smeae_pinakas_lektiko

        if form.smeae_kathgoria.data:
            smeae_kathgoria_id = form.smeae_kathgoria.data
            smeae_kathgoria_lektiko = Smeae_kathgoria.query.filter_by(id=smeae_kathgoria_id).\
                                        first().lektiko
            print('sm kat', smeae_kathgoria_id, smeae_kathgoria_lektiko)
            download_filename += ' ' + smeae_kathgoria_lektiko

        if form.perioxh.data:
            perioxh_id = form.perioxh.data
            perioxh_lektiko = Perioxh.query.filter_by(id=perioxh_id).\
                                first().lektiko
            print('perioxh', perioxh_id, perioxh_lektiko)
            download_filename += ' ' + perioxh_lektiko

        if form.mousiko_organo.data:
            mousiko_organo_id = form.mousiko_organo.data
            mousiko_organo_lektiko = Mousiko_organo.query.filter_by(id=mousiko_organo_id).\
                                        first().lektiko
            print('mous org', mousiko_organo_id, mousiko_organo_lektiko)
            download_filename += ' ' + mousiko_organo_lektiko

        if form.athlima.data:
            athlima_id = form.athlima.data
            athlima_lektiko = Athlima.query.filter_by(id=athlima_id).\
                                    first().lektiko
            print('athlima', athlima_id, athlima_lektiko)
            download_filename += ' ' + athlima_lektiko

        if form.hmeromhnia.data:
            hmeromhnia_id = form.hmeromhnia.data
            hmeromhnia_real = Hmeromhnia.query.filter_by(id=hmeromhnia_id).\
                                first().real_hmeromhnia
            hmeromhnia_lektiko = '{:%d-%b-%Y}'.format(hmeromhnia_real)
            print('hmnia', hmeromhnia_id, hmeromhnia_real, hmeromhnia_lektiko)
        else: print('hmnia clear')

        real_eidikothta_id = Klados.query.filter_by(id=klados_id).first().real_eidikothta_id
        real_eidikothta_kodikos = Real_eidikothta.query.filter_by(id=real_eidikothta_id).\
                                    first().kodikos_real_eidikothtas
        real_eidikothta_lektiko = Real_eidikothta.query.filter_by(id=real_eidikothta_id).\
                                    first().lektiko_real_eidikothtas
        print('real eid', real_eidikothta_id, real_eidikothta_kodikos, real_eidikothta_lektiko)


        try:
            q = Pinakas.query.filter_by(sxoliko_etos_id=sxoliko_etos_id,\
                                  kathgoria_id=kathgoria_id,\
                                  hmeromhnia_id=hmeromhnia_id,\
                                  smeae_pinakas_id=smeae_pinakas_id,\
                                  smeae_kathgoria_id=smeae_kathgoria_id,\
                                  perioxh_id=perioxh_id,\
                                  mousiko_organo_id=mousiko_organo_id,\
                                  athlima_id=athlima_id).\
                                    filter(Pinakas.klados_id.contains(klados_id))

            pinakes = q.all()

        except Exception as e:
            print(e)

        pinakas = Pinakas
        for p in pinakes:
            pinakas_id = p.id
            pinakas_klados_id = p.klados_id
            # print(pinakas_id, pinakas_klados_id)
            if match_klados('form', klados_id, pinakas_klados_id):
                pinakas = Pinakas.query.filter_by(id=pinakas_id).first()
                # print(pinakas_id, pinakas_klados_id)

        filename = pinakas.lektiko_pinaka
        url_pinaka = pinakas.url_pinaka
        path_pinaka = pinakas.path_pinaka
        size_pinaka = pinakas.size

        path_filename = url_for('static', filename=path_pinaka + filename)
        print('path_filename', path_filename)

        # download filename: readable Greek name
        if hmeromhnia_id != 1:
            download_filename += ' ' + hmeromhnia_lektiko
        else:
            download_filename += ' ' + sxoliko_etos_lektiko

        # download filename suffix
        download_filename += '.xls'

        print('download_filename', download_filename)

        session['sxoliko_etos_id']  = sxoliko_etos_id
        session['sxoliko_etos_lektiko']  = sxoliko_etos_lektiko

        session['kathgoria_id'] = kathgoria_id
        session['kathgoria_lektiko'] = kathgoria_lektiko

        session['klados_id'] = klados_id
        session['klados_kodikos'] = klados_kodikos
        session['klados_lektiko'] = klados_lektiko

        session['hmeromhnia_id'] = hmeromhnia_id
        session['hmeromhnia_real'] = hmeromhnia_real
        session['hmeromhnia_lektiko'] = hmeromhnia_lektiko

        session['smeae_pinakas_id'] = smeae_pinakas_id
        session['smeae_pinakas_lektiko'] = smeae_pinakas_lektiko

        session['smeae_kathgoria_id'] = smeae_kathgoria_id
        session['smeae_kathgoria_lektiko'] = smeae_kathgoria_lektiko

        session['perioxh_id'] = perioxh_id
        session['perioxh_lektiko'] = perioxh_lektiko

        session['mousiko_organo_id'] = mousiko_organo_id
        session['mousiko_organo_lektiko'] = mousiko_organo_lektiko

        session['athlima_id'] = athlima_id
        session['athlima_lektiko'] = athlima_lektiko

        session['real_eidikothta_id'] = real_eidikothta_id
        session['real_eidikothta_kodikos'] = real_eidikothta_kodikos
        session['real_eidikothta_lektiko'] = real_eidikothta_lektiko

        session['url_pinaka'] = url_pinaka

        session['path_pinaka'] = path_pinaka

        session['filename'] = filename
        session['path_filename'] = path_filename
        session['download_filename'] = download_filename

        session['size_pinaka'] = size_pinaka

        if current_app.config['TALAIPANAP_ADMIN']:
            send_email(current_app.config['TALAIPANAP_ADMIN'], ' New submit', 'mail/new_submit',\
                       sxoliko_etos_id=str(sxoliko_etos_id), sxoliko_etos_lektiko=sxoliko_etos_lektiko,\
                       kathgoria_id=str(kathgoria_id), kathgoria_lektiko=kathgoria_lektiko,\
                       klados_id=str(klados_id), klados_kodikos=klados_kodikos, klados_lektiko=klados_lektiko,\
                       hmeromhnia_id=str(hmeromhnia_id), hmeromhnia_real=str(hmeromhnia_real), hmeromhnia_lektiko=hmeromhnia_lektiko,\
                       smeae_pinakas_id=str(smeae_pinakas_id), smeae_pinakas_lektiko=smeae_pinakas_lektiko,\
                       smeae_kathgoria_id=str(smeae_kathgoria_id), smeae_kathgoria_lektiko=smeae_kathgoria_lektiko,\
                       perioxh_id=str(perioxh_id), perioxh_lektiko=perioxh_lektiko,\
                       mousiko_organo_id=str(mousiko_organo_id), mousiko_organo_lektiko=mousiko_organo_lektiko,\
                       athlima_id=str(athlima_id), athlima_lektiko=athlima_lektiko,\
                       real_eidikothta_id=str(real_eidikothta_id), real_eidikothta_kodikos=real_eidikothta_kodikos, real_eidikothta_lektiko=real_eidikothta_lektiko,\
                       url_pinaka=url_pinaka,\
                       path_pinaka=path_pinaka,\
                       filename=filename,\
                       path_filename=path_filename,\
                       download_filename=download_filename,\
                       size_pinaka=size_pinaka)

        return redirect(url_for('main.result'))

    return render_template('index.html', form=form)


@main.route('/result', methods=['GET', 'POST'])
def result():
    return render_template('result.html',
                           sxoliko_etos_id=session.get('sxoliko_etos_id'),
                           sxoliko_etos_lektiko=session.get('sxoliko_etos_lektiko'),
                           kathgoria_id=session.get('kathgoria_id'),
                           kathgoria_lektiko=session.get('kathgoria_lektiko'),
                           klados_id=session.get('klados_id'),
                           klados_kodikos=session.get('klados_kodikos'),
                           klados_lektiko=session.get('klados_lektiko'),
                           hmeromhnia_id=session.get('hmeromhnia_id'),
                           hmeromhnia_real=session.get('hmeromhnia_real'),
                           hmeromhnia_lektiko=session.get('hmeromhnia_lektiko'),
                           smeae_pinakas_id=session.get('smeae_pinakas_id'),
                           smeae_pinakas_lektiko=session.get('smeae_pinakas_lektiko'),
                           smeae_kathgoria_id=session.get('smeae_kathgoria_id'),
                           smeae_kathgoria_lektiko=session.get('smeae_kathgoria_lektiko'),
                           perioxh_id=session.get('perioxh_id'),
                           perioxh_lektiko=session.get('perioxh_lektiko'),
                           mousiko_organo_id=session.get('mousiko_organo_id'),
                           mousiko_organo_lektiko=session.get('mousiko_organo_lektiko'),
                           athlima_id=session.get('athlima_id'),
                           athlima_lektiko=session.get('athlima_lektiko'),
                           real_eidikothta_id=session.get('real_eidikothta_id'),
                           real_eidikothta_kodikos=session.get('real_eidikothta_kodikos'),
                           real_eidikothta_lektiko=session.get('real_eidikothta_lektiko'),
                           url_pinaka = session.get('url_pinaka'),
                           path_pinaka = session.get('path_pinaka'),
                           filename = session.get('filename'),
                           path_filename = session.get('path_filename'),
                           download_filename = session.get('download_filename'),
                           size_pinaka = session.get('size_pinaka'))



@main.route('/download_remove')
def download_remove():
    # csv.gz to df to excel
    #
    filename = session.get('filename')
    path_pinaka = session.get('path_pinaka')

    df = unzip_to_df(filename,
                      path_pinaka,
                      data_path,
                      temp_path)

    xls_temp_file_path = Path(temp_path + '/' + path_pinaka + filename[:-6] + 'xls')
    df.to_excel(str(xls_temp_file_path), index_label='Α/Α')

    @after_this_request
    def delete_file(response):
        # remove temp xls file
        try:
            os.remove(str(xls_temp_file_path))
        except Exception as e:
            print(e)
        return response

    print('after delete_file')
    return send_from_directory(str(xls_temp_file_path.parent), xls_temp_file_path.name)


@main.route('/pinakas_display')
def pinakas_display():
    filename = session.get('filename')
    path_pinaka = session.get('path_pinaka')

    df = unzip_to_df(filename,
                      path_pinaka,
                      data_path,
                      temp_path)
    df.reset_index(inplace=True)

    # get table headers and rows
    columns = df.columns.str.replace('index','')
    rows = df.to_json(force_ascii=False, orient='values').replace('None', '') 

    return render_template('display.html', columns=columns, rows=rows,
                           download_filename = session.get('download_filename'),
                           size_pinaka = session.get('size_pinaka'))


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


@main.route('/_update_fields/')
def _update_fields():

    print(request.args)

    sxoliko_etos_id = request.args.get('sxoliko_etos')
    kathgoria_id = request.args.get('kathgoria')
    klados_id = str(request.args.get('klados'))
    smeae_pinakas_id = request.args.get('smeae_pinakas')
    smeae_kathgoria_id = request.args.get('smeae_kathgoria')
    perioxh_id = request.args.get('perioxh')
    mousiko_organo_id = request.args.get('mousiko_organo')
    athlima_id = request.args.get('athlima')
    hmeromhnia_id = request.args.get('hmeromhnia')
    field = request.args.get('field')

    filters = {}
    filters['sxoliko_etos_id'] = sxoliko_etos_id
    filters['kathgoria_id'] = kathgoria_id

    choices_fields = []

    print('sxoliko_etos', sxoliko_etos_id,\
          '\nkathgoria', kathgoria_id,\
          '\nklados', klados_id,\
          '\nsmeae_pinakas', smeae_pinakas_id,\
          '\nsmeae_kathgoria', smeae_kathgoria_id,\
          '\nperioxh', perioxh_id,\
          '\nmousiko_organo', mousiko_organo_id,\
          '\nathlima_id', athlima_id,\
          '\nhmeromhnia_id', hmeromhnia_id,\
          '\nfield', field)

    #check fields
    if smeae_pinakas_id is not None:
        filters['smeae_pinakas_id'] = smeae_pinakas_id

    if smeae_kathgoria_id is not None:
        filters['smeae_kathgoria_id'] = smeae_kathgoria_id

    if perioxh_id is not None:
        filters['perioxh_id'] = perioxh_id

    if mousiko_organo_id is not None:
        filters['mousiko_organo_id'] = mousiko_organo_id

    if athlima_id is not None:
        filters['athlima_id'] = athlima_id

    if hmeromhnia_id is not None:
        print('in update fields hmnies')
        hmeromhnies = []

        # build filters query
        q = Pinakas.query
        if len(klados_id) > 1:
            q = q.filter(getattr(Pinakas, 'klados_id').like('%{0}%'.format(klados_id)))
        else:
            filters['klados_id'] = klados_id
        for attr, value in filters.items():
            print(attr, value)
            q = q.filter(getattr(Pinakas, attr) == value)
        print(q)
        pinakes = q.all()
        for pinakas in pinakes:
            if pinakas.hmeromhnia_id not in hmeromhnies:
                hmeromhnies.append(pinakas.hmeromhnia_id)
        choices_fields.append(('hmeromhnies', hmeromhnies))

        print(choices_fields)

    print('filters', filters)
    print('choices_fields', choices_fields)


    return jsonify(choices_fields)



@main.route('/_get_fields/')
def _get_fields():
    sxoliko_etos_id = request.args.get('sxoliko_etos')
    kathgoria_id = request.args.get('kathgoria')
    klados_id = str(request.args.get('klados'))

    smeae_pinakes = []
    smeae_kathgories = []
    perioxes = []
    mousika_organa = []
    athlimata = []
    hmeromhnies = []

    choices_fields = []

    q = Pinakas.query
    if len(klados_id) > 1:
        q = q.filter(getattr(Pinakas, 'klados_id').like('%{0}%'.format(klados_id)))
    else:
        q = q.filter(getattr(Pinakas, 'klados_id') == klados_id)
    q = q.filter(getattr(Pinakas, 'sxoliko_etos_id') == sxoliko_etos_id)
    q = q.filter(getattr(Pinakas, 'kathgoria_id') == kathgoria_id)


    #check smeae pinakas
    pinakes = q.filter(getattr(Pinakas, 'smeae_pinakas_id') != 0).all()
    if len(pinakes) > 0:
        for pinakas in pinakes:
            if match_klados('sm-pin', klados_id, pinakas.klados_id) and (pinakas.smeae_pinakas_id not in smeae_pinakes):
                smeae_pinakes.append(pinakas.smeae_pinakas_id)
        choices_fields.append(('smeae_pinakes', smeae_pinakes))


    #check smeae kathgoria
    pinakes = q.filter(getattr(Pinakas, 'smeae_kathgoria_id') != 0).all()
    if len(pinakes) > 0:
        for pinakas in pinakes:
            if match_klados('sm-kat', klados_id, pinakas.klados_id) and (pinakas.smeae_kathgoria_id not in smeae_kathgories):
                smeae_kathgories.append(pinakas.smeae_kathgoria_id)
        choices_fields.append(('smeae_kathgories', smeae_kathgories))


    #check perioxh
    pinakes = q.filter(getattr(Pinakas, 'perioxh_id') != 0).all()
    if len(pinakes) > 0:
        for pinakas in pinakes:
            if match_klados('per', klados_id, pinakas.klados_id) and (pinakas.perioxh_id not in perioxes):
                perioxes.append(pinakas.perioxh_id)
        choices_fields.append(('perioxes', perioxes))


    #check mousiko_organo
    pinakes = q.filter(getattr(Pinakas, 'mousiko_organo_id') != 0).all()
    if len(pinakes) > 0:
        for pinakas in pinakes:
            if match_klados('m-or', klados_id, pinakas.klados_id) and (pinakas.mousiko_organo_id not in mousika_organa):
                mousika_organa.append(pinakas.mousiko_organo_id)
        choices_fields.append(('mousika_organa', mousika_organa))


    #check athlima
    pinakes = q.filter(getattr(Pinakas, 'athlima_id') != 0).all()
    if len(pinakes) > 0:
        for pinakas in pinakes:
            if match_klados('ath', klados_id, pinakas.klados_id) and (pinakas.athlima_id not in athlimata):
                athlimata.append(pinakas.athlima_id)
        choices_fields.append(('athlimata', athlimata))


    #check hmeromhnia
    pinakes = q.filter(getattr(Pinakas, 'hmeromhnia_id') != 1).all()
    if len(pinakes) > 0:
        for pinakas in pinakes:
            if match_klados('hmnia', klados_id, pinakas.klados_id) and (pinakas.hmeromhnia_id not in hmeromhnies):
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



@main.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template('contact.html')

#
# # For Ajax url_to_file table display
# # Scheduler to remove txt files
# # Obsolete since solution without ajax, file
# #
# #
# @main.route('/scheduled_print')
# def scheduled_delete():
#   count = 0
#   # os.chdir("/home/fkaralis/talaiporosanaplirotis/app/static/")
#   # for file in glob.glob("*.txt"):
#   for file in os.listdir("app/static"):
#     if file.endswith(".txt"):
#       try:
#           os.remove("app/static/" + file)
#           count+=1
#           print(str(count) + " " + file)
#       except Exception as e:
#           print(e)
#   print(time.strftime("%A, %d. %B %Y %I:%M:%S %p") + " " + str(count) + " files")

# scheduler = BackgroundScheduler()
# scheduler.add_job(func=scheduled_delete, trigger="interval", minutes=10)
# scheduler.start()

# # Shut down the scheduler 
# # scheduler.shutdown()

# # Shut down the scheduler when exiting the app
# atexit.register(lambda: scheduler.shutdown())

# # end scheduled piankas txt files delete






#
#
# view functions end
# empty response return ('', 204)
