#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# finds links and tables in http://e-aitisi.sch.gr
# exec: python crawler.py year (eg 2003 for 2003-2004)
# out: folder & log
# checked for all years

import os
import os.path
import sys
import json
import logging
import logging.config

# talaiporosanaplirotis path
basedir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
print(basedir)

# read settings
with open(basedir + '/e-aitisi_scraper/settings.json', 'r', encoding='utf-8') as fd:
    settings = json.load(fd)

# Setup logging. you need to do this before importing the main module
logging.config.dictConfig(settings["logging"])
logger = logging.getLogger("crawler")

from parser import Parser


def main(year):

    basic_path = os.path.join(basedir, 'app', 'static', 'data')
    school_year = "%s-%d" % (year, int(year) + 1)
    full_path = basic_path + school_year
    logger.info("Starting parsing: %s", school_year)

    parser = Parser(year)
    suffix = '/index' + year + '.html'

    # ensure that destination dir exists
    os.makedirs(full_path, exist_ok=True)

    # parse initial url
    url = 'http://e-aitisi.sch.gr'
    if year != '2017':
        url += suffix
    parser.parse_url(url, suffix)

    logger.info("Finished parsing: %s", school_year)
    logger.info("Found %d links %d tables", len(parser.links), len(parser.tables))


if __name__ == "__main__":
    try:
        if len(sys.argv) != 2 or not (int(sys.argv[1]) >= 2003 and int(sys.argv[1]) <= 2017):
            print("Usage: 'python crawler.py YYYY' where YYYY is an integer representing a year from 2003 to 2017 (e.g. \'2014\').")
            sys.exit(1)
        year = sys.argv[1]
        main(year)
    except ValueError:
       print("That's not a number")