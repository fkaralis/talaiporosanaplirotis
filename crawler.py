#!/usr/bin/env python
# -*- coding: utf-8 -*-
# finds links and tables in http://e-aitisi.sch.gr
# exec: python crawler.py year (eg 2003 for 2003-2004)
# out: folder & log
# checked for all years

import os
import os.path
import sys

import globalvars
from parser import *

if __name__ == "__main__":
        
    year = str(sys.argv[1])
    school_year = year + '-' + str(int(year) + 1)
    globalvars.suffix = '/index' + year + '.html'

    # create folder
    if not os.path.exists(school_year):
        try:
            os.makedirs(school_year)
        except OSError as exc: # Guard against race condition (me: ??)
            if exc.errno != errno.EEXIST:
                raise

    # create log file
    log_filename = school_year + '/log ' + school_year + '.txt'
    globalvars.log = open(log_filename, 'w')
    msg = 'Crawling through school year ' + school_year + '\n'
    print(msg.rstrip())
    globalvars.log.write(msg)

    # parse initial url
    url = 'http://e-aitisi.sch.gr'
    if year != '2016':
        url += globalvars.suffix
    parse_url(url)

    # end output
    msg = '\nDone\n\nFound ' + str(globalvars.links_count) + ' links and ' + str(globalvars.tables_count) + ' tables'
    globalvars.log.write(msg)
    print(msg)


if __name__ == "__main__":
    year = str(sys.argv[1])
