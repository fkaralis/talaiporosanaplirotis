#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#### 9/6/2017
### reduce size by cutting columns

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

# talaiporosanaplirotis path
basedir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
data_path = os.path.join(basedir, 'app', 'static')
print(basedir)
print(data_path)

engine = create_engine('sqlite:///' + os.path.join(basedir, 'e-aitisi_scraper', 'talaiporosanaplirotis.sqlite'))
DBSession = sessionmaker(bind=engine)
session = DBSession()

print('aaaaa')


'''
# get pinakes
#sxoliko_etos_id = int(sys.argv[1])

bad_read = 0
bad_read_files = {}

bad_count = 0
bad_files = {}

count = 0
pinakes = session.query(Pinakas).filter(Pinakas.klados_id != '254').all()
for pinakas in pinakes:
    id_pinaka = pinakas.id
    lektiko_pinaka = pinakas.lektiko_pinaka
    path_pinaka = pinakas.path_pinaka

    try:
        if not lektiko_pinaka.endswith('csv.gz'):
            count += 1

            # unzip file to temp file
            file_path = Path(data_path+ '/' + path_pinaka + lektiko_pinaka)
            temp_file_path = Path(path_pinaka + lektiko_pinaka[:-3])
            temp_file_path.parent.mkdir(parents=True, exist_ok=True)

            #gz to xls or html
            with gzip.open(str(file_path), 'rb') as infile:
                    with open(str(temp_file_path), 'wb') as outfile:
                        for line in infile:
                            outfile.write(line)

            #build pandas frame
            try:
                if temp_file_path.name.endswith('html'):
                    df = pd.read_html(str(temp_file_path), header=0)[0]
                elif 'xls' in temp_file_path.name:
                    df = pd.read_excel(str(temp_file_path))
            except Exception as e:
                pinakas.klados_id = '254'
                session.commit()
                bad_read += 1
                bad_read_files[id_pinaka] = e
                print(bad_read, id_pinaka, 'bad read')
                continue

            #fix index
            try:
                df.set_index(['Α/Α'], inplace=True)
            except Exception as e:
                try:
                    df.set_index(['α/α'], inplace=True)
                except Exception as e:
                    try:
                        df.set_index(['ΣΕΙΡΑ ΠΙΝΑΚΑ'], inplace=True)
                    except Exception as e:
                        df.index += 1
            df.index.name=None

            #df to csv
            csv_temp_file_path = Path(str(temp_file_path.parent) + '/' + temp_file_path.stem + '.csv')
            df.to_csv(str(csv_temp_file_path), encoding='utf-8')

            csv_gz_temp_file_path = Path(str(csv_temp_file_path) + '.gz')
            #csv to csv.gz
            with open(str(csv_temp_file_path), 'rb') as f_in:
                with gzip.open(str(csv_gz_temp_file_path), 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)

            #move temp file to target
            target_file_path = Path(str(file_path.parent) + '/' + str(csv_gz_temp_file_path.name))
            shutil.copy(str(csv_gz_temp_file_path), str(target_file_path))

            #delete original file
            os.remove(str(file_path))

            #update DB entry
            pinakas.lektiko_pinaka = csv_gz_temp_file_path.name

            session.commit()
            print(count, id_pinaka, 'OK')

    except Exception as e:
        bad_count += 1
        bad_files[id_pinaka] = e
        print(bad_count, id_pinaka, 'bad')
        continue

print('updated', count)
print('bad read', bad_read)
print('other failed', bad_count)


'''


'''

            pinakas.lektiko_pinaka = full_filename + '.gz'
            os.remove(full_filename)
            session.commit()


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



if 'home' in path_pinaka:
    pinakas.path_pinaka = path_pinaka[48:]

session.commit()
'''