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

from app.models import Athlima, Athlima_greeklish, Hmeromhnia, Kathgoria,\
Klados, Mousiko_organo, Mousiko_organo_greeklish, Perioxh, Perioxh_greeklish,\
Pinakas, Real_eidikothta, Smeae_kathgoria, Smeae_kathgoria_greeklish,\
Smeae_pinakas, Sxoliko_etos

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

sxoliko_etos_id = 1
kathgoria_id = 10
klados_id = '6'
hmeromhnia_id = 207
mousiko_organo_id = 0
smeae_pinakas_id = 0
smeae_kathgoria_id = 0
athlima_id = 0
perioxh_id = 0

# filters['sxoliko_etos_id'] = sxoliko_etos_id
# filters['kathgoria_id'] = kathgoria_id
#filters['mousiko_organo_id'] = mousiko_organo_id
#filters['smeae_pinakas_id'] = smeae_pinakas_id
#filters['smeae_kathgoria_id'] = smeae_kathgoria_id

count=0
pinakes_kladoi_id = []
q = session.query(Pinakas).filter_by(sxoliko_etos_id=sxoliko_etos_id,\
                              kathgoria_id=kathgoria_id,\
                              hmeromhnia_id=hmeromhnia_id,\
                              smeae_pinakas_id=smeae_pinakas_id,\
                              smeae_kathgoria_id=smeae_kathgoria_id,\
                              perioxh_id=perioxh_id,\
                              mousiko_organo_id=mousiko_organo_id,\
                              athlima_id=athlima_id).\
                            filter(Pinakas.klados_id.contains(klados_id))

# q = q.filter(getattr(Pinakas, 'klados_id') == klados_id)
# q = q.filter_by(klados_id=klados_id)


# if len(klados_id) > 1:
#     q = q.filter(getattr(Pinakas, 'klados_id').like('%{0}%'.format(klados_id)))
# else:
#     q = q.filter(getattr(Pinakas, 'klados_id') == klados_id)

pinakes = q.all()
print(type(pinakes), len(pinakes))

pinakas = Pinakas

for p in pinakes:
    id = p.id
    pinakas_klados_id = p.klados_id
    print(id, pinakas_klados_id)
    if re.match('^' + klados_id +'$', pinakas_klados_id) or re.match('^' + klados_id + '\s(.)*$', pinakas_klados_id) or re.match('^(.)*\s' + klados_id + '$', pinakas_klados_id) or re.match('^(.)*\s' + klados_id + '\s(.)*$', pinakas_klados_id):
        pinakas = session.query(Pinakas).filter_by(id=id).first()
        print(id, pinakas_klados_id)
	#if pinakas_klados_id not in pinakes_kladoi_id:
	#pinakes_kladoi_id.append(pinakas_klados_id)
	# if re.match('^' + klados_id +'$', pinakas_klados_id) or re.match('^' + klados_id + '\s(.)*$', pinakas_klados_id) or re.match('^(.)*\s' + klados_id + '$', pinakas_klados_id) or re.match('^(.)*\s' + klados_id + '\s(.)*$', pinakas_klados_id) :
	# 	count+=1
	# 	print(count, id, pinakas_klados_id)

print(pinakas.id, pinakas.lektiko_pinaka)

'''

filter(Pinakas.klados_id.contains(klados_id))

q = Pinakas.query.filter_by(sxoliko_etos_id=sxoliko_etos_id,\
                                  kathgoria_id=kathgoria_id,\
                                  hmeromhnia_id=hmeromhnia_id,\
                                  smeae_pinakas_id=smeae_pinakas_id,\
                                  smeae_kathgoria_id=smeae_kathgoria_id,\
                                  perioxh_id=perioxh_id,\
                                  mousiko_organo_id=mousiko_organo_id,\
                                  athlima_id=athlima_id)

            if len(klados_id) > 1:
                q = q.filter(getattr(Pinakas, 'klados_id').like('%{0}%'.format(klados_id)))
            else:
                q = q.filter(getattr(Pinakas, 'klados_id') == klados_id)

            pinakas = q.first()



'^' + klados_id +'$'
'^' + klados_id + '\s(.)*$'
'^(.)*\s' + klados_id + '$'
'^(.)*\s' + klados_id + '\s(.)*$'


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
