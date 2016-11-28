#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
fill eidikothta.id_real_eidikothtas, eidikothta.lektiko_real_eidikothtas
'''

import re
import os
import json
import logging
import logging.config

import sqlalchemy

from sqlalchemy import create_engine
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

real_eidikothtes = session.query(Real_eidikothta).all()
eidikothtes = session.query(Eidikothta).all()

kodikoi_real_eidikothtwn = []
for real_eidikothta in real_eidikothtes:
    id_real_eidikothtas = real_eidikothta.id
    kodikos_real_eidikothtas = real_eidikothta.kodikos_real_eidikothtas
    lektiko_real_eidikothtas = real_eidikothta.lektiko_real_eidikothtas

    letters_real_eidikothtas = re.search('(\D+)\d+\.*\d*\D*', kodikos_real_eidikothtas).group(1)
    if letters_real_eidikothtas == 'ΠΕ':
        letters_real_eidikothtas = 'PE'
    elif letters_real_eidikothtas == 'ΤΕ':
        letters_real_eidikothtas = 'TE'
    elif letters_real_eidikothtas == 'ΔΕ':
        letters_real_eidikothtas = 'DE'
    number_real_eidikothtas = re.search('\D*(\d+\.*\d*)\D*', kodikos_real_eidikothtas).group(1)
    first_real_eidikothtas = number_real_eidikothtas.split('.')[0]
    #first_real_eidikothtas = re.search('(\d+)\.*\d*', number_real_eidikothtas).group(1)
    last_real_eidikothtas = number_real_eidikothtas.split('.')[1]
    #last_real_eidikothtas = re.search('\d+\.*(\d*)', number_real_eidikothtas).group(1)

    logger.info("----------------------\n%s %s %s %s %s %s %s", id_real_eidikothtas, kodikos_real_eidikothtas, lektiko_real_eidikothtas,
          letters_real_eidikothtas, number_real_eidikothtas,
          first_real_eidikothtas, last_real_eidikothtas)

    for eidikothta in eidikothtes:
        eidikothta_id = eidikothta.id
        kodikos_eidikothtas = eidikothta.kodikos_eidikothtas

        #re pattern
        p = re.compile(r'_|\.|,+')
        eidikothta_parts = p.split(kodikos_eidikothtas)

        try:
            letters_eidikothtas = re.search('(\D+)\d*', eidikothta_parts[0]).group(1).upper()
        except Exception as e:
            letters_eidikothtas = None

        try:
            numbers_eidikothtas = []
            for i in eidikothta_parts:
                numbers_eidikothtas.append(re.search('\D*(\d*)', i).group(1))
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

        if letters_real_eidikothtas == letters_eidikothtas:
            if first_real_eidikothtas == first_eidikothtas:
                #logger.info("first match %s %s %s", kodikos_real_eidikothtas, kodikos_eidikothtas, last_eidikothtas)
                if len(numbers_eidikothtas) < 3:
                    if last_eidikothtas is not None:
                        if last_real_eidikothtas == last_eidikothtas:
                            logger.info("first AND last match %s %s", kodikos_real_eidikothtas, kodikos_eidikothtas)
                    else:
                        logger.info("first ONLY match %s %s", kodikos_real_eidikothtas, kodikos_eidikothtas)
                else:
                    logger.info("%s", kodikos_eidikothtas)
            #logger.info("%s %s %s %s %s %s", eidikothta_id, kodikos_eidikothtas, letters_eidikothtas, number_eidikothtas, first_eidikothtas, last_eidikothtas)























