#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#### 10/3/2017
### finds & downloads new tables & updates DB (checked 2016-2017)

import pandas as pd
import re
import os
from bs4 import BeautifulSoup
import requests
import datetime
import logging

import sqlalchemy

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists

from pathlib import PurePosixPath
from pathlib import Path

import gzip
import shutil

from db import Base, get_one_or_create
from db import Athlima, Athlima_greeklish, Hmeromhnia, Kathgoria,\
Klados, Mousiko_organo, Mousiko_organo_greeklish, Perioxh, Perioxh_greeklish,\
Pinakas, Real_eidikothta, Smeae_kathgoria, Smeae_kathgoria_greeklish,\
Smeae_pinakas, Sxoliko_etos


# talaiporosanaplirotis path
basedir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
#print(basedir)

engine = create_engine('sqlite:///' + os.path.join(basedir, 'e-aitisi_scraper', 'talaiporosanaplirotis.sqlite'))
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

logger = logging.getLogger("parser")


class Parser:

    def __init__(self, year, url='http://e-aitisi.sch.gr'):
        self.year = year
        self.suffix = '/index%s.html' % year
        if year != '2017':
            url += self.suffix
        self.url = url
        self.links = {}
        self.tables = {}

    def parse_url(self, url, suffix):
        #print('> in parse_url', url, suffix)
        html = requests.get(url)
        html.encoding = 'ISO-8859-7'
        soup = BeautifulSoup(html.content, 'html.parser')

        # fix .html suffixes in middle of url, and other irregularities
        url = self.fix_url(url, suffix)

        tags = soup('a')
        for tag in tags:
            href = tag.get('href')
            if not re.match('index\d+\.html', href):        # end 2016
                link_url = self.create_url(url, href)
                self.parse_link(link_url, tag, suffix)


    def parse_link(self, url, tag, suffix):
        #print('> in parse_link', url, tag, suffix)
        year = suffix[6:][:-5]
        sxoliko_etos = year + '-' + str(int(year) + 1)

        # (entirely useless) fix // in middle of url
        url = re.sub(r'^((?:(?!//).)*//(?:(?!//).)*)//', r'\1/', url)

        if (url.endswith('xls') or url.endswith('xlsx') or url.endswith('gz')):
            filename = url.rsplit('/')[-1]
            if self.table_exists(filename, url, sxoliko_etos):
                logger.info("Table exists %s <%r>", url, tag.contents)
            else:
                self.download_table(filename, url, sxoliko_etos)
                self.tables[len(self.tables)+1] = url
                logger.info("Found new table: %s %s <%r>", filename, url, tag.contents)

        elif ((url.endswith('.html') and 'index' not in url)):
            if any(url.endswith(suf) for suf in ['DE.html','TE.html']):    # 2006 and back, DE and TE indexes
                self.links[len(self.links)+1] = url
                self.parse_url(url, suffix)
                logger.info("------------------\nFound link: %s <%r>", url, tag.contents)
            else:
                filename = url.rsplit('/')[-1]
                if self.table_exists(filename, url, sxoliko_etos):
                    logger.info("Table exists %s <%r>", url, tag.contents)
                else:
                    # only html tables (2012 and back)
                    valid_names = [
                        'eniaioidior',
                        'eniaios_diorismwn',
                        'triantamino',
                        'eikositetramino',
                        'specialcat',
                        'eniaiosp_2012',
                        'eniaiosp_zero_2012',
                        'eniaiosd_2012',
                        'eniaiosd_zero_2012',
                        'eniaios_bthmias_2003',
                    ]
                    if any(name in url for name in valid_names):
                        self.download_table(filename, url, sxoliko_etos)

                    self.tables[len(self.tables)+1] = url
                    logger.info("Found new html table: %s %s <%r>", filename, url, tag.contents)


        elif ('index' in url and 'old' not in url) or url.endswith('/'):
            logger.info("Found old link: %s <%r>", url, tag.contents)
            self.links[len(self.links)+1] = url
            if url == 'http://e-aitisi.sch.gr/triantamino_07/index.html':
                logger.warning('Crazy 2007 link to 2016 index\n')
            elif url == 'http://e-aitisi.sch.gr/eniaios_smea_orom_11_B/index.html':
                logger.warning('Crazy 2011 link to 2013 index\n')
            else:
                self.parse_url(url, suffix)

        else:
            logger.info("Not xls, html or gz %s <%r>", url, tag.contents)


    def download_table(self, filename, url, sxoliko_etos):
        #print('> in download_table', url, suffix)

        # collect params for download
        # lektiko_pinaka
        print('filename', filename)

        # path_pinaka
        path_pinaka = url[22:][:-len(filename)]     # len('http://e-aitisi.sch.gr') == 22
        path_pinaka_parts = path_pinaka.rsplit('/')
        print('path_pinaka', path_pinaka)

        # create path if not exists
        full_path = '/home/fkaralis/talaiporosanaplirotis/app/static/data/' + sxoliko_etos + path_pinaka
        print('full_path', full_path)
        os.makedirs(full_path, exist_ok=True)

        full_filename = ('').join([full_path, filename])
        print('full_filename', full_filename, os.path.isfile(full_filename))

        # Download table
        if not os.path.isfile(full_filename):
            response = requests.get(url)
            with open(full_filename, 'wb') as output:
                output.write(response.content)
            logger.info('Downloaded')
        else:
            logger.info('Pinakas already there')


        # find Pinakas attributes
        # Sxoliko etos
        sxoliko_etos_id = session.query(Sxoliko_etos).filter_by(lektiko_sxolikoy_etoys=sxoliko_etos).first().id
        print('sxoliko_etos_id', sxoliko_etos_id)


        # Hmeromhnia ----only field to possibly create new
        if path_pinaka_parts[-2].isdigit():      # date YYYYMMDD in path pinaka
            hmeromhnia = path_pinaka_parts[-2]
        elif path_pinaka_parts[-2][:8].isdigit():     # date YYYYMMDD(a/b)
            hmeromhnia = path_pinaka_parts[-2][:8]
        elif path_pinaka_parts[-3].isdigit():      # smea date 2015 in other position
            hmeromhnia = path_pinaka_parts[-3]
        else:
            hmeromhnia = '10101010'     # no date in path
        new_hmeromhnia, _ = get_one_or_create(
            session,
            Hmeromhnia,
            lektiko_hmeromhnias=hmeromhnia,
            real_hmeromhnia=datetime.datetime.strptime(hmeromhnia, "%Y%m%d").date()
        )
        print('new_hmeromhnia', new_hmeromhnia)


        # Kathgoria
        kathgoria_id = self.find_kathgoria(path_pinaka.split('/')[1], filename)
        print('kathgoria_id', kathgoria_id)


        #Klados
        # re.match('^' + klados_id +'$', pinakas_klados_id) or re.match('^' + klados_id + '\s(.)*$', pinakas_klados_id) or re.match('^(.)*\s' + klados_id + '$', pinakas_klados_id) or re.match('^(.)*\s' + klados_id + '\s(.)*$', pinakas_klados_id):
        klados_id = ''
        try:
            df = pd.read_excel(full_filename, header=0)
            for row in df.iterrows():
                try:
                    kodikos_kladoy = row[1]['ΚΛΑΔΟΣ']
                except Exception as e:
                    logger.error(e)
                    klados_id = '254' # bad file

                try:
                    temp_klados_id = str(session.query(Klados).filter_by(kodikos_kladoy=kodikos_kladoy).first().id)
                except Exception as e:
                    logger.error(e)
                    print('new klados?', kodikos_kladoy)

                if not (re.match('^' + temp_klados_id +'$', klados_id) or re.match('^' + temp_klados_id + '\s(.)*$', klados_id) or re.match('^(.)*\s' + temp_klados_id + '$', klados_id) or re.match('^(.)*\s' + temp_klados_id + '\s(.)*$', klados_id)):
                    print('NEW kodikos_kladoy', temp_klados_id)
                    klados_id += ' ' + temp_klados_id
        except Exception as e:
            klados_id = '254' # bad file
            logger.error(e)

        klados_id = klados_id.strip()
        print('klados_id', klados_id)


        #Smeae_pinakas, _kathgoria
        smeae_pinakas_id = 0 # default
        smeae_kathgoria_id = 0

        if kathgoria_id in [11, 18, 19]:
            if '_A/' in path_pinaka:
                smeae_pinakas_id = 1
            elif '_B/' in path_pinaka:
                smeae_pinakas_id = 2

            # populate greeklish lektika lists
            smeae_kathgories_greeklish_normal_lektika = []
            smeae_kathgories_greeklish_braille_lektika = []
            smeae_kathgories_greeklish_eng_lektika = []
            smeae_kathgories_greeklish_braille_eng_lektika = []
            smeae_kathgories_greeklish = session.query(Smeae_kathgoria_greeklish).all()
            for smeae_kathgoria_greeklish in smeae_kathgories_greeklish:
                if smeae_kathgoria_greeklish.smeae_kathgoria_id == 1:
                    smeae_kathgories_greeklish_normal_lektika.append(smeae_kathgoria_greeklish.lektiko)
                elif smeae_kathgoria_greeklish.smeae_kathgoria_id == 2:
                    smeae_kathgories_greeklish_braille_lektika.append(smeae_kathgoria_greeklish.lektiko)
                elif smeae_kathgoria_greeklish.smeae_kathgoria_id == 3:
                    smeae_kathgories_greeklish_eng_lektika.append(smeae_kathgoria_greeklish.lektiko)
                elif smeae_kathgoria_greeklish.smeae_kathgoria_id == 4:
                    smeae_kathgories_greeklish_braille_eng_lektika.append(smeae_kathgoria_greeklish.lektiko)

            if any(x in path_pinaka for x in smeae_kathgories_greeklish_normal_lektika):
                smeae_kathgoria_id = 1;
            elif any(x in path_pinaka for x in smeae_kathgories_greeklish_braille_lektika):
                smeae_kathgoria_id = 2;
            elif any(x in path_pinaka for x in smeae_kathgories_greeklish_eng_lektika):
                smeae_kathgoria_id = 3;
            elif any(x in path_pinaka for x in smeae_kathgories_greeklish_braille_eng_lektika):
                smeae_kathgoria_id = 4;

        print('smeae_pinakas_id', smeae_pinakas_id)
        print('smeae_kathgoria_id', smeae_kathgoria_id)


        #Perioxh
        perioxh_id = 0 # default
        perioxes_greeklish = session.query(Perioxh_greeklish).all()
        for perioxh_greeklish in perioxes_greeklish:
            if perioxh_greeklish.lektiko in filename:
                perioxh_id = perioxh_greeklish.perioxh_id
        print('perioxh_id', perioxh_id)


        #Mousiko_organo
        mousiko_organo_id = 0 # default
        mousika_organa_greeklish = session.query(Mousiko_organo_greeklish).all()
        for mousiko_organo_greeklish in mousika_organa_greeklish:
            if mousiko_organo_greeklish.lektiko in filename:
                mousiko_organo_id = mousiko_organo_greeklish.mousiko_organo_id
        print('mousiko_organo_id', mousiko_organo_id)


        #Athlima
        athlima_id = 0 # default
        athlimata_greeklish = session.query(Athlima_greeklish).all()
        for athlima_greeklish in athlimata_greeklish:
            if athlima_greeklish.lektiko in filename:
                athlima_id = athlima_greeklish.athlima_id
        print('athlima_id', athlima_id)


        logger.debug("filename: %s; sx.etos_id: %s; kathgoria_id: %s; hmnia_id: %s;\
                     full_path: %s; url: %s; klados_id: %s; smeae_pinakas_id: %s; smeae_kathgoria_id: %s;\
                     perioxh_id: %s; perioxh_id: %s; athlima_id: %s; ",
                     filename, sxoliko_etos_id, kathgoria_id, new_hmeromhnia.id,\
                     full_path, url, klados_id, smeae_pinakas_id, smeae_kathgoria_id,\
                     perioxh_id, mousiko_organo_id, athlima_id)

        # excel to csv.gz (and delete xcel)
        filename = self.xcel_to_csv_gz(full_path, filename)

        # final path for pinakas
        path_pinaka = 'data/' + sxoliko_etos + path_pinaka

        # size pinaka
        full_path = Path(full_path)
        full_path_filename = full_path.joinpath(filename)
        if klados_id == '254':
            size = 0
        else:
            size = full_path_filename.stat().st_size

        # Create pinakas
        get_one_or_create(
            session,
            Pinakas,
            lektiko_pinaka=filename,
            sxoliko_etos_id=sxoliko_etos_id,
            kathgoria_id=kathgoria_id,
            hmeromhnia_id=new_hmeromhnia.id,
            path_pinaka=path_pinaka,
            url_pinaka=url,
            klados_id=klados_id,
            smeae_pinakas_id=smeae_pinakas_id,
            smeae_kathgoria_id=smeae_kathgoria_id,
            perioxh_id=perioxh_id,
            mousiko_organo_id=mousiko_organo_id,
            athlima_id=athlima_id,
            size=size,
        )

        session.commit()



    def xcel_to_csv_gz(self, full_path, filename):
        try:
            full_path = Path(full_path)
            full_path_filename = full_path.joinpath(filename)

            csv_filename = full_path_filename.stem + '.csv'
            csv_gz_filename = full_path_filename.stem + '.csv.gz'

            csv_full_path = full_path.joinpath(csv_filename)
            csv_gz_full_path = full_path.joinpath(csv_gz_filename)

            # xcel to df
            df = pd.read_excel(str(full_path_filename))

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

            # df to csv
            df.to_csv(str(csv_full_path), encoding='utf-8')

            # csv to csv.gz
            with open(str(csv_full_path), 'rb') as f_in:
                with gzip.open(str(csv_gz_full_path), 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)

            # delete csv and xcel files
            os.remove(str(csv_full_path))
            os.remove(str(full_path_filename))
        except Exception as e:
            print('xcel_to_csv', e)

        return csv_gz_filename




    def find_kathgoria(self, kathgoria, filename):
        kathgoria_id = 0

        # pinakes diorismwn
        if kathgoria.startswith('eniaios_diorismwn') or kathgoria.startswith('eniaioidior_13'):
            kathgoria_id = 13
        elif kathgoria.startswith('triantamino'):
            kathgoria_id = 15
        elif kathgoria.startswith('eikositetramino'):
            kathgoria_id = 16

        # diorismoi eidikh kathgoria
        elif kathgoria.startswith('specialcat'):
            kathgoria_id = 14

        # eniaioi a/b-thmias
        elif kathgoria.startswith('eniaiosp'):
            if kathgoria.startswith('eniaiosp_zero'):
                kathgoria_id = 4
            else:
                kathgoria_id = 3
        elif kathgoria.startswith('eniaiosd'):
            if kathgoria.startswith('eniaiosd_zero'):
                kathgoria_id = 6
            else:
                kathgoria_id = 5

        # oloimera-oromisthioi
        elif kathgoria.startswith('oloimera'):
            kathgoria_id = 20
        elif (kathgoria == 'eniaios_oromis8iwn_05_zero'):
            kathgoria_id = 23
        elif kathgoria.startswith('eniaios_oromis8iwn') or kathgoria.startswith('oromisthioi'):
            kathgoria_id = 12

        # mousika
        elif kathgoria.startswith('mousika'):
            if kathgoria.startswith('mousika_orom'):
                kathgoria_id = 8
            else:
                kathgoria_id = 7

        # smea
        elif 'smea' in kathgoria:
            if kathgoria.startswith('eniaios_smea_oloim'):
                kathgoria_id = 19
            elif kathgoria.startswith('eniaios_smea_anap'):
                kathgoria_id = 11
            else:
                kathgoria_id = 18

        # politeknoi 2009
        elif kathgoria == 'politeknoi2009':
            kathgoria_id == 22

        # tad/ead
        elif kathgoria.startswith('tad'):
            if kathgoria.startswith('tadmon'):
                kathgoria_id = 25
            if kathgoria.startswith('tadanap'):
                kathgoria_id = 21
            else:
                kathgoria_id = 17

        # diagrafentes logw mh analhpshs yphresias
        elif kathgoria.startswith('diagrafentes'):
            kathgoria_id = 2

        # diagrafentes logw apolyshs
        elif kathgoria.startswith('kataggelia'):
            kathgoria_id = 1

        # meinotika thrakhs
        elif kathgoria.startswith('pe73'):
            if 'PE73_B' in filename:    # case meionotika_thrakhs_mhdenikhs_proyphresias
                kathgoria_id = 24
            else:
                kathgoria_id = 9

        # meinotika thrakhs
        elif kathgoria.startswith('avlonas'):
            kathgoria_id = 10

        return kathgoria_id


    def table_exists(self, filename, url, sxoliko_etos):
        #print('> in table_exists', filename, url, sxoliko_etos)

        path_pinaka = url[23:][:-len(filename)]     # len('http://e-aitisi.sch.gr/') == 23
        path_pinaka_parts = path_pinaka.rsplit('/') # <-- what for?
        #print('path_pinaka', path_pinaka)

        # create path if not exists
        full_path = os.path.join(basedir, 'app', 'static', 'data', sxoliko_etos, path_pinaka)
        #print(full_path, basedir, sxoliko_etos, path_pinaka)
        os.makedirs(full_path, exist_ok=True)

        filename = Path(filename)
        filename = filename.stem + '.csv.gz'

        full_filename = ('').join([full_path, filename])
        #print('full_filename', full_filename, os.path.isfile(full_filename))

        if os.path.isfile(full_filename):
            return True
        else:
            print('file NOT exists', full_filename)
            return False


    def create_url(self, url, href):
        #print('> in create_url', url, href)
        if url.endswith('/index.html'):
            url = url[:-11]
        return url + '/' + href


    def fix_url(self, url, suffix):
        if suffix in url:       # initial index.html
            url_parts = url.split(suffix)
            url = ''.join(url_parts)

        rogue_suffixes = ['/indexAB.html', '/indexC.html', '/indexG.html',
                               '/indexABg.html', '/indexCg.html', '/indexGg.html']
        if any(x in url for x in rogue_suffixes):       # 2003-4
            splitter = re.search('/index.+?\.html', url).group(0)
            url_parts = url.split(splitter)
            url = ''.join(url_parts)
        if '-index.html' in url:        # ~2010 tadmon(TAD/ETAD)
            splitter = re.search('/\d?\D+\d?\D*-index.html', url).group(0)
            url_parts = url.split(splitter)
            url = ''.join(url_parts)
        if '_13/indexdior.html' in url:     # 2013
            splitter = re.search('/indexdior.html', url).group(0)
            url_parts = url.split(splitter)
            url = ''.join(url_parts)

        return url

