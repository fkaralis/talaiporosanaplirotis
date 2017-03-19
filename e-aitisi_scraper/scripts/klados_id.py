#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''   fill pinakas.klados_id column
NOT TODO turn all non smea pinakes plhroforikh to klados 247 and mousikh to 249
DONE klados_id --> multiple ids??

DOING use pandas see kladoi.py for checking which eidikothtes/kladoi in pinakes ΟΚ

2/1/2017
remaining about 1000 null klados_id
now working on sxol_et 12, kat 5 6 TE DE
must download tables and then run pandas to put kladoi_id

31/12/2016
got tables from html, now see if klados is other than 32.50

30/12
filled smea
now start from pinakas.klados_id is None

28-12-2016 going for > 2 kladoi per real_eidikothta
catching all not smea kladoys and corresponding eidikothtes


'''
import requests
import re
import os
import os.path
import sys
import gzip
import json
import pandas as pd
from os import listdir
from os.path import isfile, isdir, join

import sqlalchemy
import pandas

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists

from db import Base, Klados, Real_eidikothta, Eidikothta, Pinakas

engine = create_engine('sqlite:///talaiporosanaplirotis.sqlite')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


#def main(sxoliko_etos_id_input):
def main():
    #klados = session.query(Klados).filter(Klados.id == 1).one()
    kladoi = session.query(Klados).all()
    real_eidikothtes = session.query(Real_eidikothta).all()
    pinakes = session.query(Pinakas).filter_by(klados_id=254).all()

    count = 0

    mul_kladoi = {}
    kladoi_pinaka_ids = {}

    print(len(pinakes))

'''
    for pinakas in pinakes:

        lek_pinaka = pinakas.lektiko_pinaka
        path_pinaka = pinakas.path_pinaka
        url_pinaka = pinakas.url_pinaka

        filename_pinaka = (pinakas.path_pinaka + lek_pinaka).replace('/', '\\')
        size_pinaka = os.path.getsize(filename_pinaka)

        kladoi_pinaka_ids[pinakas.id] = []

        count += 1

        print(count, pinakas.id, lek_pinaka, pinakas.klados_id, size_pinaka)

        pinakas.klados_id = 254

        session.commit()
        print(count, pinakas.id, lek_pinaka, pinakas.klados_id, size_pinaka)

            try:
                if filename_pinaka.endswith('gz'):
                    #print('in gz')
                    try:
                        with gzip.open(filename_pinaka, 'r') as fh:
                            html_file = fh.read()
                    except Exception as e:
                        print('no gzip', filename_pinaka, e)
                        continue
                    try:
                        df = pd.read_html(html_file, header=0)
                        #print(df[0])
                        ### HERE see kladoi in table
                        for row in df[0].iterrows():
                            klados_pinaka = row[1]['ΚΛΑΔΟΣ']
                            if klados_pinaka == 'ΠΕ11.01':
                                klados_pinaka = 'ΠΕ11.50'
                            try:
                                klados_row_id = session.query(Klados).filter_by(kodikos_kladoy=klados_pinaka).one().id
                                #print(klados_row_id)
                                if klados_row_id not in kladoi_pinaka_ids[pinakas.id]:
                                    print('new', klados_row_id)
                                    kladoi_pinaka_ids[pinakas.id].append(klados_row_id)
                            except Exception as e:
                                print('no klados', klados_pinaka)
                    except Exception as e:
                        print('e1', lek_pinaka, e, klados_pinaka)
                        continue
                elif filename_pinaka.endswith('html'):
                    #print('in html')
                    try:
                        df = pd.read_html(filename_pinaka, header=0)
                        #print(df[0])
                        ### HERE see kladoi in table
                        for row in df[0].iterrows():
                            klados_pinaka = row[1]['ΚΛΑΔΟΣ']
                            if klados_pinaka == 'ΠΕ11.01':
                                klados_pinaka = 'ΠΕ11.50'
                            try:
                                klados_row_id = session.query(Klados).filter_by(kodikos_kladoy=klados_pinaka).one().id
                                #print(klados_row_id)
                                if klados_row_id not in kladoi_pinaka_ids[pinakas.id]:
                                    print('new', klados_row_id)
                                    kladoi_pinaka_ids[pinakas.id].append(klados_row_id)
                            except Exception as e:
                                print('no klados', klados_pinaka)
                    except Exception as e:
                        print('e2', lek_pinaka, e, klados_pinaka)
                        continue
                elif 'xls' in filename_pinaka:
                    #print('in xls')
                    try:
                        df = pd.read_excel(filename_pinaka, header=0)
                        #print(df)
                        ### HERE see kladoi in table
                        for row in df.iterrows():
                            klados_pinaka = row[1]['ΚΛΑΔΟΣ']
                            if klados_pinaka == 'ΠΕ11.01':
                                klados_pinaka = 'ΠΕ11.50'
                            try:
                                klados_row_id = session.query(Klados).filter_by(kodikos_kladoy=klados_pinaka).one().id
                                #print(klados_row_id)
                                if klados_row_id not in kladoi_pinaka_ids[pinakas.id]:
                                    print('new', klados_row_id)
                                    kladoi_pinaka_ids[pinakas.id].append(klados_row_id)
                            except Exception as e:
                                print('no klados', klados_pinaka)
                    except Exception as e:
                        print('e3', lek_pinaka, e, klados_pinaka)
                        continue
                elif filename_pinaka.endswith('csv'):
                    #print('in csv')
                    try:
                        df = pd.read_csv(filename_pinaka, header=0)
                        #print(df[0])
                        ### HERE see kladoi in table
                        for row in df[0].iterrows():
                            klados_pinaka = row[1]['ΚΛΑΔΟΣ']
                            if klados_pinaka == 'ΠΕ11.01':
                                klados_pinaka = 'ΠΕ11.50'
                            try:
                                klados_row_id = session.query(Klados).filter_by(kodikos_kladoy=klados_pinaka).one().id
                                #print(klados_row_id)
                                if klados_row_id not in kladoi_pinaka_ids[pinakas.id]:
                                    print('new', klados_row_id)
                                    kladoi_pinaka_ids[pinakas.id].append(klados_row_id)
                            except Exception as e:
                                print('no klados', klados_pinaka)
                    except Exception as e:
                        print('e4', lek_pinaka, e, klados_pinaka)
                        continue
            except Exception as e:
                print('no hope', e)
                continue

            kladoi_pinaka = ''
            for id in kladoi_pinaka_ids[pinakas.id]:
                kladoi_pinaka += str(id) + ' '

            pinakas.klados_id = kladoi_pinaka[:-1]
            print('kladoi_pinaka', kladoi_pinaka)
            print(count, pinakas.id, lek_pinaka, pinakas.klados_id, size_pinaka)

            session.commit()

            print(count, pinakas.id, '\n',\
                  pinakas.kathgoria_id,'\n',\
                  pinakas.path_pinaka, '\n',\
                  pinakas.url_pinaka, '\n',\
                  filename_pinaka, '\n',\
                  size_pinaka)


        if size_pinaka < 500:
            pinakas.klados_id = '254'
            session.commit()
            continue

        if lek_pinaka.endswith('html') and size_pinaka in [2030, 2033, 1990, 3449, 3575, 3124, 3636, 3354, 3185]:
            pinakas.klados_id = '254'
            session.commit()
            continue

        if pinakas.kathgoria_id in [17, 21]:
            pinakas.klados_id = 16
            session.commit()
            continue

        if '/TE.html/' in path_pinaka:
            pinakas.path_pinaka = path_pinaka.replace('/TE.html/', '/TE/')
            pinakas.url_pinaka = url_pinaka.replace('/TE.html/', '/')

        if '/DE.html/' in path_pinaka:
            pinakas.path_pinaka = path_pinaka.replace('/DE.html/', '/DE/')
            pinakas.url_pinaka = url_pinaka.replace('/DE.html/', '/')

        filename_pinaka = (pinakas.path_pinaka + lek_pinaka).replace('/', '\\')

        size_pinaka = os.path.getsize(filename_pinaka)
        #if size_pinaka == 168:

        session.commit()

        print(count, pinakas.id, '\n',\
              pinakas.kathgoria_id,'\n',\
              pinakas.path_pinaka, '\n',\
              pinakas.url_pinaka, '\n',\
              filename_pinaka, '\n',\
              size_pinaka)

        response = requests.get(url_pinaka)
        with open(filename_pinaka, 'wb') as output:
            output.write(response.content)

    if lek_pinaka.endswith('gz'):
        lek_pinaka = lek_pinaka.replace('_g', '').replace('.gz','')
        url_pinaka = url_pinaka.replace('_g', '').replace('.gz','')

        filename_pinaka = (pinakas.path_pinaka + lek_pinaka).replace('/', '\\')

        response = requests.get(url_pinaka)
        with open(filename_pinaka, 'wb') as output:
            output.write(response.content)

        size_pinaka = os.path.getsize(filename_pinaka)

        pinakas.lektiko_pinaka = lek_pinaka
        pinakas.url_pinaka = url_pinaka

        session.commit()

        print(count, pinakas.id, '\n',\
              pinakas.kathgoria_id,'\n',\
              pinakas.path_pinaka, '\n',\
              pinakas.url_pinaka, '\n',\
              filename_pinaka, '\n',\
              size_pinaka)

    #session.commit()

        kladoi_pinaka_ids[pinakas.id] = []

        if filename_pinaka.endswith('gz'):
            #print('in gz')
            try:
                with gzip.open(filename_pinaka, 'r') as fh:
                    html_file = fh.read()
            except Exception as e:
                print('no gzip', filename_pinaka, e)
                continue
            try:
                df = pd.read_html(html_file, header=0)
                #print(df[0])
                ### HERE see kladoi in table
                for row in df[0].iterrows():
                    klados_pinaka = row[1]['ΚΛΑΔΟΣ']
                    if klados_pinaka == 'ΠΕ11.01':
                        klados_pinaka = 'ΠΕ11.50'
                    try:
                        klados_row_id = session.query(Klados).filter_by(kodikos_kladoy=klados_pinaka).one().id
                        #print(klados_row_id)
                        if klados_row_id not in kladoi_pinaka_ids[pinakas.id]:
                            print('new', klados_row_id)
                            kladoi_pinaka_ids[pinakas.id].append(klados_row_id)
                    except Exception as e:
                        print('no klados', klados_pinaka)
            except Exception as e:
                print('e1', lek_pinaka, e, klados_pinaka)
        elif filename_pinaka.endswith('html'):
            #print('in html')
            try:
                df = pd.read_html(filename_pinaka, header=0)
                #print(df[0])
                ### HERE see kladoi in table
                for row in df[0].iterrows():
                    klados_pinaka = row[1]['ΚΛΑΔΟΣ']
                    if klados_pinaka == 'ΠΕ11.01':
                        klados_pinaka = 'ΠΕ11.50'
                    try:
                        klados_row_id = session.query(Klados).filter_by(kodikos_kladoy=klados_pinaka).one().id
                        #print(klados_row_id)
                        if klados_row_id not in kladoi_pinaka_ids[pinakas.id]:
                            print('new', klados_row_id)
                            kladoi_pinaka_ids[pinakas.id].append(klados_row_id)
                    except Exception as e:
                        print('no klados', klados_pinaka)
            except Exception as e:
                print('e2', lek_pinaka, e, klados_pinaka)
        elif 'xls' in filename_pinaka:
            #print('in xls')
            try:
                df = pd.read_excel(filename_pinaka, header=0)
                #print(df)
                ### HERE see kladoi in table
                for row in df.iterrows():
                    klados_pinaka = row[1]['ΚΛΑΔΟΣ']
                    if klados_pinaka == 'ΠΕ11.01':
                        klados_pinaka = 'ΠΕ11.50'
                    try:
                        klados_row_id = session.query(Klados).filter_by(kodikos_kladoy=klados_pinaka).one().id
                        #print(klados_row_id)
                        if klados_row_id not in kladoi_pinaka_ids[pinakas.id]:
                            print('new', klados_row_id)
                            kladoi_pinaka_ids[pinakas.id].append(klados_row_id)
                    except Exception as e:
                        print('no klados', klados_pinaka)
            except Exception as e:
                print('e3', lek_pinaka, e, klados_pinaka)
        elif filename_pinaka.endswith('csv'):
            #print('in csv')
            try:
                df = pd.read_csv(filename_pinaka, header=0)
                #print(df[0])
                ### HERE see kladoi in table
                for row in df[0].iterrows():
                    klados_pinaka = row[1]['ΚΛΑΔΟΣ']
                    if klados_pinaka == 'ΠΕ11.01':
                        klados_pinaka = 'ΠΕ11.50'
                    try:
                        klados_row_id = session.query(Klados).filter_by(kodikos_kladoy=klados_pinaka).one().id
                        #print(klados_row_id)
                        if klados_row_id not in kladoi_pinaka_ids[pinakas.id]:
                            print('new', klados_row_id)
                            kladoi_pinaka_ids[pinakas.id].append(klados_row_id)
                    except Exception as e:
                        print('no klados', klados_pinaka)
            except Exception as e:
                print('e4', lek_pinaka, e, klados_pinaka)

        kladoi_pinaka = ''
        for id in kladoi_pinaka_ids[pinakas.id]:
            kladoi_pinaka += str(id) + ' '
        if size_pinaka > 1000:
            pinakas.klados_id = kladoi_pinaka[:-1]
        else:
            kladoi_pinaka += '254'
            pinakas.klados_id = '254'

        print('kladoi_pinaka', kladoi_pinaka)
        print(count, pinakas.id, lek_pinaka, pinakas.klados_id, size_pinaka)
        session.commit()

    print('done')


    #f.write(str(len(kladoi_pinaka_ids)) + '\n' + json.dumps(kladoi_pinaka_ids))
    #f.write('\n' + str(kladoi_pinaka_ids))
    #f.close()

'''

if __name__ == "__main__":
    #sxoliko_etos_id_input = sys.argv[1]
    #main(sxoliko_etos_id_input)
    main()

