#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#### 8/5/2017
### multi-sheet xcel to csv to gz

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

ks = session.query(Real_eidikothta).all()
for k in ks:
	print(k)

'''

file_path = Path('/home/fkaralis/Downloads/pinakas_avlona_2016.xls')
work_sheets = pd.ExcelFile(str(file_path)).sheet_names

#excel to df
df = pd.read_excel(str(file_path), sheetname=work_sheets, skiprows=1, index_col=None, na_values=['-'])
#df to csv
for k in df.keys():
	print('csv', k)
	df[k].set_index(['Α/Α'], inplace=True)
	csv_file_path = Path(str(file_path.parent) + '/' + file_path.stem + '_' + k + '.csv')
	df[k].to_csv(str(csv_file_path), encoding='utf-8')

#csv to gz
for k in df.keys():
	print('gz', k)
	csv_file_path = Path(str(file_path.parent) + '/' + file_path.stem + '_' + k + '.csv')
	csv_gz_file_path = Path(str(file_path.parent) + '/' + file_path.stem + '_' + k + '.csv.gz')
	with open(str(csv_file_path), 'rb') as f_in:
	    with gzip.open(str(csv_gz_file_path), 'wb') as f_out:
	        shutil.copyfileobj(f_in, f_out)

####
### TODO fill DB with csv.gz's
'''