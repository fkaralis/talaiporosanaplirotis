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

# ks = session.query(Real_eidikothta).all()
# for k in ks:
# 	print(k)


data_dir_path = Path('data/2016-2017/avlonas_2016/')

path_pinaka = str(data_dir_path)
url_pinaka = 'http://e-aitisi.sch.gr/avlonas_2016/pinakas_avlona_2016.xls'

file_path = Path('/home/fkaralis/Downloads/pinakas_avlona_2016/')
p = file_path.glob('**/*')
files = [x for x in p if x.is_file()]

for f in files:
	if str(f).endswith('csv'):
		print('-----------------------------------------------------')
		print(f)
		klados_in_pinakas = f.stem.split('_')[-1]
		print(klados_in_pinakas)

		lektiko_pinaka = str(f.name) + '.gz'

		klados_id = ''
		try:
			klados = session.query(Klados).filter_by(kodikos_kladoy = klados_in_pinakas).first()
			print(klados.lektiko_kladoy, klados.id)
			klados_id += str(klados.id)
		except Exception as e: # composite klados
			klados_in_pinakas_split = klados_in_pinakas.split(' ')
			print(klados_in_pinakas_split)
			for k in klados_in_pinakas_split:
				try:
					klados = session.query(Klados).filter_by(kodikos_kladoy = k).first()
					print(klados.lektiko_kladoy, klados.id)
					klados_id += str(klados.id) + ' '
				except Exception as e:
					print('no such klados', e)

		if klados_id != '':
			klados_id = klados_id.rstrip()
			print('final klados', klados_id)

			try:
				session.add(Pinakas(lektiko_pinaka = lektiko_pinaka,\
							sxoliko_etos_id = 1,\
							kathgoria_id = 10,\
							hmeromhnia_id = 206,\
							path_pinaka = path_pinaka,\
							url_pinaka = url_pinaka,\
							klados_id = klados_id,\
							smeae_pinakas_id = 0,\
							smeae_kathgoria_id = 0,\
							perioxh_id = 0,\
							mousiko_organo_id = 0,\
							athlima_id = 0))

				try:
				    os.remove(str(f))
				    os.remove(str(f) + '.gz')
				except Exception as e:
				    print(e)

				session.commit()

			except Exception as e:
				print(e)







'''
session.add(Pinakas(lektiko_pinaka = lektiko_pinaka,\
							sxoliko_etos_id = 1,\
							kathgoria_id = 10,\
							hmeromhnia_id = 207,\
							path_pinaka = path_pinaka,\
							url_pinaka = url_pinaka,\
							klados_id = klados_id,\
							smeae_pinakas_id = 0,\
							smeae_kathgoria_id = 0,\
							perioxh_id = 0,\
							mousiko_organo_id = 0,\
							athlima_id = 0))
		session.commit()


session.add(Hmeromhnia(lektiko_hmeromhnias = '20160902', real_hmeromhnia = datetime.datetime.strptime('20160902', "%Y%m%d").date()))
session.commit()



get_one_or_create(
            session,
            Pinakas,
            lektiko_pinaka=filename,
            sxoliko_etos_id=sxoliko_etos_id,
            kathgoria_id=kathgoria_id,
            hmeromhnia_id=new_hmeromhnia.id,
            path_pinaka=full_path,
            url_pinaka=url,
            klados_id=klados_id,
            smeae_pinakas_id=smeae_pinakas_id,
            smeae_kathgoria_id=smeae_kathgoria_id,
            perioxh_id=perioxh_id,
            mousiko_organo_id=mousiko_organo_id,
            athlima_id=athlima_id,
        )

        session.commit()



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

'''