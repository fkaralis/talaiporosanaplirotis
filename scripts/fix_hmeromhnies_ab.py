#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
fix hmeromhnies yyyymmdd(a/b)
eg pinakas id 4704:
data/2014-2015/eniaios_smea_anap_14/20141027b/ENIAIOS_SMEA_ANAP_14_NORMAL/


'''
from flask import Flask
from flask import current_app
import requests
import re
import os
import os.path
import sys
import gzip
import json
import pandas as pd
from os import listdir
from os.path import isfile, isdir, join

import sqlalchemy
import pandas
import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists
from sqlalchemy import or_
from sqlalchemy import and_

from app import create_app
from app import db
from app.models import Kathgoria, Real_eidikothta, Klados, Sxoliko_etos, Hmeromhnia,\
Pinakas, Smeae_pinakas, Smeae_kathgoria, Perioxh, Mousiko_organo, Athlima,\
Smeae_kathgoria_greeklish, Perioxh_greeklish, Mousiko_organo_greeklish, Athlima_greeklish

engine = create_engine('sqlite:////home/fkaralis/talaiporosanaplirotis/e-aitisi_scraper/talaiporosanaplirotis.sqlite')
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = create_app(os.getenv('TALAIPANAP_CONFIG') or 'default')


#def main(sxoliko_etos_id_input):
def main():
    pinakes = session.query(Pinakas).filter_by(hmeromhnia_id=1).all()
    hmeromhnies = session.query(Hmeromhnia).all()

    count = 0
    for pinakas in pinakes:
        path = pinakas.path_pinaka
        id = pinakas.id
        try:
            hmnia = re.search('^.*/(\d{8}).*', path).group(1)
            real_hmnia = datetime.datetime.strptime(hmnia, "%Y%m%d").date()
            count += 1
            hmeromhnia = Hmeromhnia.query.filter_by(lektiko_hmeromhnias=hmnia).one()
            pinakas.hmeromhnia_id = hmeromhnia.id
            print(count, id, hmnia, real_hmnia, pinakas.hmeromhnia_id,\
                  hmeromhnia.id, hmeromhnia.lektiko_hmeromhnias, hmeromhnia.real_hmeromhnia)
        except Exception:
            pass

    session.commit()

if __name__ == "__main__":
    main()


'''




lektiko_pinaka = re.search('^(.+?)-.*', lektiko_pinaka).group(1)

    kathgories = {}
    pinakes = Pinakas.query.filter(Pinakas.smeae_pinakas_id != 0).all()
    for pinakas in pinakes:
        kathgoria_id = pinakas.kathgoria_id
        if kathgoria_id not in kathgories:
            kathgories[kathgoria_id] = Kathgoria.query.filter_by(id=kathgoria_id).one().greek_lektiko_kathgorias

    print(kathgories)

    smeae_kathgories_greeklish = session.query(Smeae_kathgoria_greeklish).all()
    #smeae_kathgoria_id
    normal = ['normal', 'NORMAL'] # 2009-2010, 2010-11: eniaios w/out braille knowlang
    braille = ['Braille', 'braille', 'BRAILLE']
    eng = ['Noimatiki', 'knowlang', 'noimatiki', 'ENG']
    braille_eng = ['braille_and_knowlang', 'brailleNoimatiki', 'braileNoimatiki', 'braille_noimatiki']

    #smeae_pinakas_id
    # _A _B

    count=0
    pinakes = session.query(Pinakas).filter(or_(Pinakas.kathgoria_id == 11,\
                                                Pinakas.kathgoria_id == 18,\
                                                Pinakas.kathgoria_id == 19)).all()
    for pinakas in pinakes:

        count+=1
        id = pinakas.id
        lektiko = pinakas.lektiko_pinaka
        path = pinakas.path_pinaka
        #print(count, id, lektiko, path)

        path_parts = re.split('\W+|_', path)

        # smeae kathgoria
        smeae_kathgoria_lektiko = None
        for i in braille_eng:
            if i in path_parts:
                pinakas.smeae_kathgoria_id = 4

        if not smeae_kathgoria_lektiko:
            for i in eng:
                if i in path_parts:
                    pinakas.smeae_kathgoria_id = 3

        if not smeae_kathgoria_lektiko:
            for i in braille:
                if i in path_parts:
                    pinakas.smeae_kathgoria_id = 2

        if pinakas.smeae_kathgoria_id == 0:
            pinakas.smeae_kathgoria_id = 1

        # smeae pinakas
        if 'A' in path_parts:
            pinakas.smeae_pinakas_id = 1
        elif 'B' in path_parts:
            pinakas.smeae_pinakas_id = 2


        print(count, id, path, pinakas.smeae_kathgoria_id, pinakas.smeae_pinakas_id)

    session.commit()

        print(count, id, path, session.query(Smeae_kathgoria).filter_by(id=pinakas.smeae_kathgoria_id).one().lektiko)


for smeae_kathgoria_greeklish in smeae_kathgories_greeklish:
            if smeae_kathgoria_greeklish.lektiko in path_parts:
                print(count, id, path, smeae_kathgoria_greeklish.lektiko)

                #pinakas.smeae_kathgoria_id = smeae_kathgoria_greeklish.smeae_kathgoria_id
# if greeklish lektika in list
#smeae_kathgoria_id
normal = ['normal', 'NORMAL'] # 2009-2010, 2010-11: eniaios w/out braille knowlang
braille = ['Braille', 'braille', 'BRAILLE']
eng = ['Noimatiki', 'knowlang', 'noimatiki', 'ENG']
braille_eng = ['braille_and_knowlang', 'brailleNoimatiki', 'braileNoimatiki', 'braille_noimatiki']
#if [item for item in path_parts if any(x in item for x in braille_eng)]:


 # athlimata
    count=0
    pinakes = session.query(Pinakas).filter(or_(Pinakas.klados_id == 16, Pinakas.klados_id == 146)).all()
    for pinakas in pinakes:
        lektiko_pinaka = pinakas.lektiko_pinaka
        if lektiko_pinaka.endswith('gz'):
            lektiko_pinaka = lektiko_pinaka[:-10]
        elif lektiko_pinaka.endswith('html'):
            lektiko_pinaka = lektiko_pinaka[:-5]
        elif lektiko_pinaka.endswith('xls'):
            lektiko_pinaka = lektiko_pinaka[:-4]

        if not (lektiko_pinaka.startswith('PE') or\
                lektiko_pinaka.startswith('pe') or\
                lektiko_pinaka.startswith('eniaios')):

            if not len(session.query(Perioxh_greeklish).filter_by(lektiko=lektiko_pinaka).all()) > 0:
                try:
                    lektiko_pinaka = re.search('^(.+?)-.*', lektiko_pinaka).group(1)
                except Exception:
                    pass

                try:
                    athlima_greeklish = session.query(Athlima_greeklish).filter_by(lektiko=lektiko_pinaka).one()
                    pinakas.athlima_id = athlima_greeklish.athlima_id
                    session.commit()
                except Exception:
                    count+=1
                    print(count, lektiko_pinaka)
                    athlima_lektiko = input('Δώσε άθλημα ')
                    if athlima_lektiko != '':
                        new_athlima = Athlima(lektiko = athlima_lektiko)
                        session.add(new_athlima)
                        session.commit()

                        pinakas.athlima_id = new_athlima.id
                        new_athlima_greeklish = Athlima_greeklish(lektiko=lektiko_pinaka, athlima_id=new_athlima.id)
                        session.add(new_athlima_greeklish)
                        session.commit()
                    else:
                        athlima_id = input('Δώσε ID ')

                        pinakas.athlima_id = athlima.id
                        new_athlima_greeklish = Athlima_greeklish(lektiko=lektiko_pinaka, athlima_id=athlima_id)
                        session.add(new_athlima_greeklish)
                        session.commit()


athlima_lektiko = input('Δώσε άθλημα: ')
                    new_athlima = Athlima(lektiko = athlima_lektiko)

# get IDs
    perioxes_greeklish = session.query(Perioxh_greeklish).all()
    for perioxh_greeklish in perioxes_greeklish:
        print(perioxh_greeklish.lektiko)
        perioxh_greeklish.perioxh_id = input('Δώσε ID ')
        session.commit()

# isolate lektiko
    mousika_organa_greeklish = session.query(Mousiko_organo_greeklish).all()
    for mousiko_organo_greklish in mousika_organa_greeklish:
        if mousiko_organo_greklish.lektiko.endswith('gz'):
            mousiko_organo_greklish.lektiko = mousiko_organo_greklish.lektiko[:-10]
        elif mousiko_organo_greklish.lektiko.endswith('html'):
            mousiko_organo_greklish.lektiko = mousiko_organo_greklish.lektiko[:-5]
        elif mousiko_organo_greklish.lektiko.endswith('xls'):
            mousiko_organo_greklish.lektiko = mousiko_organo_greklish.lektiko[:-4]
    session.commit()

    mousika_organa_greeklish = session.query(Mousiko_organo_greeklish).all()
    for mousiko_organo_greklish in mousika_organa_greeklish:
        try:
            mousiko_organo_greklish.lektiko = re.search('.*\d_(.+?)$', mousiko_organo_greklish.lektiko).group(1)
        except Exception:
            pass
    session.commit()

#delete duplicat rows
    mousika_organa_greeklish = session.query(Mousiko_organo_greeklish).all()
    for mousiko_organo_greeklish in mousika_organa_greeklish:
        if len(session.query(Mousiko_organo_greeklish).filter_by(lektiko=mousiko_organo_greeklish.lektiko).all()) > 1:
            session.delete(mousiko_organo_greeklish)

    session.commit()

# fill perioxh_greeklish
    count=0
    for pinakas in pinakes:
        lektiko_pinaka = pinakas.lektiko_pinaka
        if lektiko_pinaka not in greeklish_lektika:
            count+=1
            greeklish_lektika.append(lektiko_pinaka)
            new_perioxh_greeklish = Perioxh_greeklish(lektiko=lektiko_pinaka, perioxh_id=0)
            session.add(new_perioxh_greeklish)
    session.commit()

perioxes_greeklish = session.query(Perioxh_greeklish).all()
    for perioxh_greeklish in perioxes_greeklish:
        perioxh_greeklish.lektiko = perioxh_greeklish.lektiko[:-10]
    session.commit()
                      mousiko_organo.original_lektiko))



 #populate pinakas.perioxh_id
    count=0
    for pinakas in pinakes:
        count+=1
        lektiko_pinaka = pinakas.lektiko_pinaka
        if lektiko_pinaka.endswith('gz'):
            lektiko_pinaka = lektiko_pinaka[:-10]
        elif lektiko_pinaka.endswith('html'):
            lektiko_pinaka = lektiko_pinaka[:-5]
        elif lektiko_pinaka.endswith('xls'):
            lektiko_pinaka = lektiko_pinaka[:-4]
        try:
            lektiko_pinaka = re.search('.*E\._(.+?)?$', lektiko_pinaka).group(1)
        except Exception:
            pass

        try:
            pinakas.perioxh_id = session.query(Perioxh_greeklish).filter_by(lektiko=lektiko_pinaka).one().perioxh_id
            print(count, lektiko_pinaka, pinakas.perioxh_id)
        except Exception:
            print(count, lektiko_pinaka, ' not found in Perioxh_greeklish')

    session.commit()

'''


