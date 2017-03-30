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

from ... import app

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


kathgories = Kathgoria.query.all()

for kathgoria in kathgories:
    print(kathgoria.lektiko_kathgorias)












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