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
eidikothtes = session.query(Eidikothta).filter_by(real_eidikothta_id = 0).all()
#kladoi = session.query(Klados).all()

count_eid = 0
for eidikothta in eidikothtes:
    count_eid += 1

    eidikothta_id = eidikothta.id
    kodikos_eidikothtas = eidikothta.kodikos_eidikothtas
    if eidikothta_id > 744 and eidikothta_id < 774:
        logger.info('--------\n %s %s %s', count_eid, eidikothta_id, kodikos_eidikothtas)
        eidikothta.real_eidikothta_id = 16
        session.commit()



    elif 'FYSIKHS' in kodikos_eidikothtas:

        logger.info('--------\n %s %s %s', count_eid, eidikothta_id, kodikos_eidikothtas)


#    pinakes = session.query(Pinakas).filter_by(eidikothta_id=eidikothta_id).all()





