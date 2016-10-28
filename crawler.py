#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# finds links and tables in http://e-aitisi.sch.gr
# exec: python crawler.py year (eg 2003 for 2003-2004)
# out: folder & log
# checked for all years

import os
import os.path
import sys

import parser
from parser import *

def main(year):
    parser = Parser()
    
    school_year = year + '-' + str(int(year) + 1)
    suffix = '/index' + year + '.html'
    
    # create folder
    if not os.path.exists(school_year):
        try:
            os.makedirs(school_year)
        except OSError as exc: # Guard against race condition (me: ??)
            if exc.errno != errno.EEXIST:
                raise

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
    if len(sys.argv) != 2 or not isinstance(sys.argv[1], int):
        print("Usage: 'python crawler.py XXXX' where XXXX is an integer representing a year from 2003 to 2016 (e.g. \'2014\').")
        sys.exit(1)
        
    year = str(sys.argv[1])
    
    if int(year) > 2016 or int(year) < 2003:
        print("Year min 2003, max 2016")
        sys.exit(1)
    main(year)
