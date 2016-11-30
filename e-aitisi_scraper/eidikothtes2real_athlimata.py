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

real_eidikothtes = session.query(Real_eidikothta).all()
eidikothtes = session.query(Eidikothta).filter_by(real_eidikothta_id=0).all()
kladoi = session.query(Klados).all()
pinakes = session.query(Pinakas).filter_by(eidikothta_id = 1439).all()
'''
count_eid = 0
for eidikothta in eidikothtes:
    count_eid += 1

    eidikothta_id = eidikothta.id
    kodikos_eidikothtas = eidikothta.kodikos_eidikothtas

    #logger.info('--------\n %s %s %s', count_eid, eidikothta_id, kodikos_eidikothtas)

    pinakes = session.query(Pinakas).filter_by(eidikothta_id=eidikothta_id).all()
'''

count = 0
for pinakas in pinakes:

    pinakas_eidikothta_id = pinakas.eidikothta_id

    count += 1
    pinakas_id = pinakas.id
    lektiko_pinaka = pinakas.lektiko_pinaka
    path_pinaka = pinakas.path_pinaka
    #logger.info('--------\n %s %s %s', count_eid, eidikothta_id, kodikos_eidikothtas)
    logger.info('%s %s %s %s', count, pinakas_id, lektiko_pinaka, path_pinaka)

    lektiko_pinaka = lektiko_pinaka.split('_')[0]
    letters_pinaka = re.search('(\D*)\d+\.*\d+', lektiko_pinaka).group(1)
    numbers_pinaka = re.search('\D*(\d+\.*\d+)', lektiko_pinaka).group(1)
    first_pinaka = numbers_pinaka.split('.')[0]
    last_pinaka = numbers_pinaka.split('.')[1]

    if letters_pinaka == 'PE': letters_pinaka = 'ΠΕ'
    if letters_pinaka == 'DE': letters_pinaka = 'ΔΕ'
    if letters_pinaka == 'TE': letters_pinaka = 'ΤΕ'

    lektiko_pinaka = letters_pinaka + numbers_pinaka

    try:
        klados = session.query(Klados).filter_by(kodikos_kladoy = lektiko_pinaka).one()
    except Exception as e:
        klados = session.query(Klados).filter_by(kodikos_kladoy = lektiko_pinaka[:-3]).one()

    klados_real_eidikothta_id = klados.real_eidikothta_id
    kodikos_k = klados.kodikos_kladoy
    lektiko_k = klados.lektiko_kladoy

    real_eidikothta = session.query(Real_eidikothta).filter_by(id = klados_real_eidikothta_id).one()
    kodikos_re = real_eidikothta.kodikos_real_eidikothtas
    lektiko_re = real_eidikothta.lektiko_real_eidikothtas

    logger.info("%s %s %s %s %s %s", lektiko_pinaka, letters_pinaka,
                kodikos_k, lektiko_k, kodikos_re, lektiko_re)




'''

            letters_pinaka = re.search('(\D+)\d*', lektiko_pinaka_parts[0]).group(1)
            first_pinaka = re.search('\D+(\d+)', lektiko_pinaka_parts[0].split('.')[0]).group[1]

            logger.info('%s %s %s', letters_pinaka, first_pinaka, last_pinaka)
'''




        #print('Eidikothta', eidikothta.kodikos_eidikothtas, 'not MOYSIKH!!')
        #eidikothta.real_eidikothta_id = 16
        #session.commit()




