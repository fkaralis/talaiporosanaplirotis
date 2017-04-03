#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#### 3/4/2017
### bad qeury in main._get_fields

import pandas as pd
import re
import os
import sys
import requests
import datetime
import gzip
import shutil
from pathlib import PurePosixPath
from pathlib import Path

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists
from sqlalchemy import and_
from sqlalchemy import or_

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app import db
from app.models import Athlima, Athlima_greeklish, Hmeromhnia, Kathgoria,\
Klados, Mousiko_organo, Mousiko_organo_greeklish, Perioxh, Perioxh_greeklish,\
Pinakas, Real_eidikothta, Smeae_kathgoria, Smeae_kathgoria_greeklish,\
Smeae_pinakas, Sxoliko_etos

app = create_app(os.getenv('TALAIPANAP_CONFIG') or 'default')

# talaiporosanaplirotis path
basedir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
data_path = os.path.join(basedir, 'app', 'static')
print(basedir)
print(data_path)

engine = create_engine('sqlite:///' + os.path.join(basedir, 'e-aitisi_scraper', 'talaiporosanaplirotis.sqlite'))
DBSession = sessionmaker(bind=engine)
session = DBSession()

choices_fields = []
filters = {}
hmeromhnies = []
kladoi = []

sxoliko_etos_id = 4
kathgoria_id = 11
klados_id = '148'
#mousiko_organo_id = 11
#smeae_pinakas_id = 2
#smeae_kathgoria_id = 1

filters['sxoliko_etos_id'] = sxoliko_etos_id
filters['kathgoria_id'] = kathgoria_id
#filters['mousiko_organo_id'] = mousiko_organo_id
#filters['smeae_pinakas_id'] = smeae_pinakas_id
#filters['smeae_kathgoria_id'] = smeae_kathgoria_id

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





'''

for pinakas in pinakes:
    klados_id = pinakas.klados_id
    if klados_id not in kladoi:
        kladoi.append(klados_id)

print(sorted(kladoi))

q = q.filter(getattr(Pinakas, attr).like("%%%s%%" % value))

pinakes = session.query(Pinakas).filter(Pinakas.klados_id == '254').\
                                filter(or_(Pinakas.id == 10361,\
                                           Pinakas.id == 10480,\
                                           Pinakas.id == 10529)).all()



'''