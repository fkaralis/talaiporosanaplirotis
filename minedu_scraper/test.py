#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#### 30/3/2017
### test


import pandas as pd
import re
import os
import sys
import requests
from bs4 import BeautifulSoup
import datetime
import gzip
import shutil
from pathlib import PurePosixPath
from pathlib import Path
import json
import logging
import logging.config

import sqlalchemy
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
datapath = os.path.join(os.path.dirname(basedir), 'app', 'static')
print('basedir', basedir)
dloads_path = Path(basedir, 'minedu_scraper/downloads')

#kathgories = session.query(Kathgoria).filter_by().all()
# print(datapath)
# print(basedir)

# kathgories = Kathgoria.query.all()

# for kathgoria in kathgories:
#     print(kathgoria.lektiko_kathgorias)# read settings
with open(basedir + "/minedu_scraper/settings.json", "r", encoding="utf-8") as fd:
    settings = json.load(fd)

# Setup logging. you need to do this before importing the main module
logging.config.dictConfig(settings["logging"])
logger = logging.getLogger("minedu_scraper")


def main():
	base_url = 'https://www.minedu.gov.gr'
	url = base_url + '/ekpaideutikoi-m/anaplirotes-new/proslipseis-anapl/poreia-mon'
	os.makedirs(str(dloads_path), exist_ok=True)

	pros_links = {}
	count = 0
	xls_links = {}
	xls_count = 0
	dload_count = 0

	try:
		# url = 'https://www.minedu.gov.gr/ekpaideutikoi-m/anaplirotes-new/proslipseis-anapl?limit=260'
		soup = parse_url(url + '?limit=220')
		for tag in soup('a'):
			href = tag.get('href')
			text = tag.get_text().strip()
			if 'ροσλ' in text or 'ρόσλ' in text:
				count += 1
				if href not in pros_links:
					pros_links[href] = text

				link_soup = parse_url(url + href)
				for tag in link_soup.find_all('a', href=lambda x: x and 'xls' in x):
					link_href = tag.get('href')
					# logger.info("%s", link_href)
					link_text = tag.get_text().strip()
					# count += 1
					xls_count += 1
					if link_href in xls_links:
					 	logger.info("Double xls link\n%s\n%s", url+href, link_href)
					xls_links[link_href] = link_text
					logger.info("Found XLS")
					logger.info("%s %s %s", xls_count, link_href, link_text)
					if download_table(base_url, link_href):
						dload_count += 1
	except Exception as e:
		pass

	logger.info("Links %s %s, XLS %s %s\n-------------------------------------------------------",\
		count, len(pros_links), xls_count, len(xls_links))

	for key in xls_links:
		print(key, xls_links[key])

	print('downloaded', dload_count)

def parse_url(href):
	html = requests.get(href)
	html.encoding = 'ISO-8859-7'

	return BeautifulSoup(html.content, 'html.parser')


def download_table(base_url, link_href):
	try:
		full_url = base_url + link_href
		filename = Path(link_href).name
		print('in dload table')
		full_file_path = Path(dloads_path, filename)
		print(str(full_file_path))
		if not os.path.isfile(str(full_file_path)):
			response = requests.get(full_url)
			with open(str(full_file_path), 'wb') as output:
				output.write(response.content)
			logger.info('Downloaded')
			return True
		else:
			logger.info('Pinakas already there?')
			return False

	except Exception as e:
		print(e)



if __name__ == "__main__":
    main()