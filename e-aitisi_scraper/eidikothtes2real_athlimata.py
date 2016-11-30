#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
fill eidikothta.real_eidikothta_id
athlimata
'''

import re
import os
import json
import logging
import logging.config

import sqlalchemy

from sqlalchemy import create_engine
from sqlalchemy import and_
from sqlalchemy import or_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists

from db import Base, get_one_or_create
from db import Kathgoria, Real_eidikothta, Klados, Eidikothta, Sxoliko_etos, Hmeromhnia, Pinakas

# read settings
with open("settings.json", "r", encoding="utf-8") as fd:
    settings = json.load(fd)

# Setup logging. you need to do this before importing the main module
try:
    os.remove('eid2real.log')
except OSError:
    pass

logging.config.dictConfig(settings["logging"])
logger = logging.getLogger("eid2real")
hdlr = logging.FileHandler('eid2real.log')
logger.addHandler(hdlr)

engine = create_engine('sqlite:///talaiporosanaplirotis.sqlite')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

def match(eidikothta, real_eidikothta):
    print("Assigning %s %s to Eidikothta %s",
                real_eidikothta.kodikos_real_eidikothtas, real_eidikothta.lektiko_real_eidikothtas,
                eidikothta.kodikos_eidikothtas)
    eidikothta.real_eidikothta_id = real_eidikothta.id
    session.commit()

#real_eidikothtes = session.query(Real_eidikothta).all()
real_eidikothtes = session.query(Real_eidikothta).all()
eidikothtes = session.query(Eidikothta).filter_by(real_eidikothta_id=0).all()
kladoi = session.query(Klados).all()

count_eid = 0
for eidikothta in eidikothtes:
    count_eid += 1

    eidikothta_id = eidikothta.id
    kodikos_eidikothtas = eidikothta.kodikos_eidikothtas

    #print('--------\n', count_eid, eidikothta_id, kodikos_eidikothtas)

    pinakes = session.query(Pinakas).filter_by(eidikothta_id=eidikothta_id).all()
    count_p = 0
    for pinakas in pinakes:
        path_pinaka = pinakas.path_pinaka
        if 'mous' in path_pinaka:
            count_p += 1
            pinakas_id = pinakas.id
            lektiko_pinaka = pinakas.lektiko_pinaka

            #print(count_p, pinakas_id, lektiko_pinaka, path_pinaka)
            print('Eidikothta', eidikothta.kodikos_eidikothtas, 'MOYSIKH!!')
            eidikothta.real_eidikothta_id = 27
            session.commit()
            break






    '''

    #re pattern
    p = re.compile(r'_|\.|,+')
    eidikothta_parts = p.split(kodikos_eidikothtas)

    try:
        letters_eidikothtas = re.search('(\D+)\d*', eidikothta_parts[0]).group(1).upper()
    except Exception as e:
        letters_eidikothtas = None

    # for PE, DE, TE
    if len(letters_eidikothtas) < 3:
        try:
            numbers_eidikothtas = []
            for i in eidikothta_parts:
                numbers_eidikothtas.append(re.search('\D*(\d*)', i).group(1))
                # remove ''
                numbers_eidikothtas = [x for x in numbers_eidikothtas if x != '']
        except Exception as e:
            print('IN NUMBERS_EIDIKOTHTAS LIST')

        try:
            first_eidikothtas = numbers_eidikothtas[0]
        except Exception as e:
            first_eidikothtas = None

        try:
            last_eidikothtas = numbers_eidikothtas[1]
        except Exception as e:
            last_eidikothtas = None

        print('--------------\n', count, eidikothta_id, kodikos_eidikothtas,
              letters_eidikothtas, numbers_eidikothtas,
              first_eidikothtas, last_eidikothtas)

        for klados in kladoi:
            kodikos_kladoy = klados.kodikos_kladoy
            letters_kladoy = re.search('(\D+)\d+\.*\d*\D*', kodikos_kladoy).group(1)
            if letters_kladoy == 'ΠΕ':
                letters_kladoy = 'PE'
            elif letters_kladoy == 'ΤΕ':
                letters_kladoy = 'TE'
            elif letters_kladoy == 'ΔΕ':
                letters_kladoy = 'DE'

            if letters_eidikothtas == letters_kladoy:
                klados_id = klados.id
                lektiko_kladoy = klados.lektiko_kladoy
                real_eidikothta_id_kladoy = klados.real_eidikothta_id

                number_kladoy = re.search('\D*(\d+\.*\d*)\D*', kodikos_kladoy).group(1)
                parts_number_kladoy = number_kladoy.split('.')
                first_kladoy = parts_number_kladoy[0]
                if first_eidikothtas == first_kladoy:
                    if len(parts_number_kladoy) > 1:
                        last_kladoy = parts_number_kladoy[1]

                        if last_eidikothtas == last_kladoy:
                            print(kodikos_kladoy, lektiko_kladoy, 'match')
                            real_eidikothta = session.query(Real_eidikothta).filter_by(id=real_eidikothta_id_kladoy).one()
                            print(real_eidikothta.kodikos_real_eidikothtas,
                                  real_eidikothta.lektiko_real_eidikothtas)
                            match(eidikothta, real_eidikothta)
    # for Moysika Organa, Athlimata
    else:
        print(letters_eidikothtas, 'mousiko organo, athlima')
'''