#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# finds links and tables in http://e-aitisi.sch.gr
# exec: python crawler.py year (eg 2003 for 2003-2004)
# out: folder & log
# checked for all years

import os
import os.path
import sys

from parser import Parser

def main(year):
    parser = Parser()

    school_year = year + '-' + str(int(year) + 1)
    suffix = '/index' + year + '.html'

    # ensure that destination dir exists
    os.makedirs(school_year, exist_ok=True)

    # create log file
    log_filename = school_year + '/log ' + school_year + '.txt'
    parser.log = open(log_filename, 'w')
    msg = 'Crawling through school year ' + school_year + '\n'
    print(msg.rstrip())
    parser.log.write(msg)

    # parse initial url
    url = 'http://e-aitisi.sch.gr'
    if year != '2016':
        url += suffix
    parser.parse_url(url, suffix)

    # end output
    msg = '\nDone\n\nFound ' + str(len(parser.links)) + ' links and ' + str(len(parser.tables)) + ' tables'
    parser.log.write(msg)
    print(msg)


if __name__ == "__main__":
    try:
        if len(sys.argv) != 2 or not (int(sys.argv[1]) >= 2003 and int(sys.argv[1]) <= 2016): 
            print("Usage: 'python crawler.py YYYY' where YYYY is an integer representing a year from 2003 to 2016 (e.g. \'2014\').")
            sys.exit(1)
        year = sys.argv[1]
        main(year)
    except ValueError:
       print("That's not a number")