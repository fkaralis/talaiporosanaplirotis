#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#### 17/3/2017
### html, xls(x) to gz
#### (not BAD files, some gz already there and small size anyawyay)

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

from db import Base, get_one_or_create
from db import Athlima, Athlima_greeklish, Hmeromhnia, Kathgoria,\
Klados, Mousiko_organo, Mousiko_organo_greeklish, Perioxh, Perioxh_greeklish,\
Pinakas, Real_eidikothta, Smeae_kathgoria, Smeae_kathgoria_greeklish,\
Smeae_pinakas, Sxoliko_etos


# talaiporosanaplirotis path
basedir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
datapath = os.path.join(os.path.dirname(basedir), 'app', 'static')

engine = create_engine('sqlite:///' + os.path.join(basedir, 'talaiporosanaplirotis.sqlite'))
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

#kathgories = session.query(Kathgoria).filter_by().all()
print(datapath)
count = 0


pinakes = session.query(Pinakas).filter(or_(Pinakas.lektiko_pinaka.endswith('xls'),\
                                            Pinakas.lektiko_pinaka.endswith('xlsx'))).all()
for pinakas in pinakes:
    filename = pinakas.lektiko_pinaka
    path_pinaka = os.path.join(datapath, pinakas.path_pinaka)
    full_filename = path_pinaka + filename
    size = Path(full_filename).stat().st_size
    klados_id = pinakas.klados_id

    if klados_id != '254':
        count += 1
        print(count, full_filename, pinakas.klados_id, size)

        try:
            with open(full_filename, 'rb') as f_in:
                with gzip.open(full_filename + '.gz', 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            pinakas.lektiko_pinaka = full_filename + '.gz'
            os.remove(full_filename)
            session.commit()
        except Exception as e:
            print(e)













'''
    try:
        pinakas.lektiko_pinaka = PurePosixPath(filename).name
        session.commit()

        count += 1
        print(count, pinakas.lektiko_pinaka, klados_id)

    except Exception as e:
        print(e)



       try:
            df = pd.read_html(full_filename, header=0)

        except Exception as e:
            print('No file', e, full_filename, pinakas.klados_id, size)



        for row in df.iterrows():
            if row[1]:
                print('row 1', full_filename, pinakas.klados_id, size)
            else:
                print('NO row 1', full_filename, pinakas.klados_id, size)



    #print(filename)
    filename_stem = PurePosixPath(filename).stem
    try:
        similar = session.query(Pinakas).filter(Pinakas.lektiko_pinaka.startswith(filename_stem),\
                                                Pinakas.lektiko_pinaka.endswith('gz'),\
                                                Pinakas.kathgoria_id==pinakas.kathgoria_id,\
                                                Pinakas.sxoliko_etos_id==pinakas.sxoliko_etos_id,\
                                                Pinakas.hmeromhnia_id==pinakas.hmeromhnia_id,\
                                                Pinakas.smeae_pinakas_id==pinakas.smeae_pinakas_id,\
                                                Pinakas.smeae_kathgoria_id==pinakas.smeae_kathgoria_id,\
                                                ).first()
        count += 1
        print(count, pinakas.lektiko_pinaka, pinakas.path_pinaka, similar.lektiko_pinaka, similar.path_pinaka, '\n-----\n')
    except Exception:
        continue



#print(pinakeslist, len(pinakeslist))

#print(list(set(htmlfiles) - set(pinakeslist)))

htmlfiles = [os.path.join(root, name)
             for root, dirs, files in os.walk(datapath)
             for name in files
             if name.startswith("PLIROFORIKH_D-E.html")]

print(htmlfiles, len(htmlfiles))

for root, dirs, files in os.walk(datapath):
   for name in files:
       if name.endswith((".html", ".htm")):
           count += 1
           print(count, name)
'''