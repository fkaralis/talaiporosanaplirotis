# finds links and tables in http://e-aitisi.sch.gr
# exec: python crawler.py year (eg 2003 for 2003-2004)
# out: folder & log
# checked from 2003-2004 up to 2009-2010

import requests
from bs4 import BeautifulSoup
import os, os.path
import re
import sys

def parse_link(url, tag):
    result = ''
    filename = ''
    global links_count
    global tables_count
    
    filetypes = ['.xls', '.xlsx', '.csv']

    # (entirely useless) fix // in middle of url 
    url = re.sub(r'^((?:(?!//).)*//(?:(?!//).)*)//', r'\1/', url)
    
    if any(url.endswith(x) for x in filetypes):
        filename = url.rsplit('/')[-1]
        result = 'Found excel table: ' + filename + ' ' + url + ' ' + str(tag.contents) + '\n'
        tables_count += 1
        log.write(result)
    
    
    elif url.endswith('gz'):
        filename = url.rsplit('/')[-1]
        result = 'Found gz table: ' + filename + ' ' + url + ' ' + str(tag.contents) + '\n'
        tables_count += 1
        log.write(result)
    
        
    elif url.endswith('.html') and 'index' not in url:
        filename = url.rsplit('/')[-1]
        result = 'Found html table: ' + filename + ' ' + url + ' ' + str(tag.contents) + '\n'
        tables_count += 1
        log.write(result)

            
    elif ('index' in url and 'old' not in url) or url.endswith('/'):
        result = '------------------\nFound link: ' + url + ' ' + str(tag.contents) + '\n'
        log.write(result)
        links_count = links_count + 1
        parse_url(url)
        
        
    else:
        result = '--Not xls, html, or gz ' + url + ' ' + str(tag.contents) + '\n'
        log.write(result)


def create_url(url, href):
    if url.endswith('/index.html'):
        url = url[:-11]
    return url + '/' + href


def parse_url(url):
    html = requests.get(url)
    html.encoding = 'ISO-8859-7'
    soup = BeautifulSoup(html.content, 'html.parser')
    
    # fix 'index.html' in middle of url
    if suffix in url:
        list = url.split(suffix)
        url = ''.join(list)        
        
    # fix suffix particularities    
    rogue_suffixes = ['/indexAB.html', '/indexC.html', '/indexG.html', 
                           '/indexABg.html', '/indexCg.html', '/indexGg.html']
    if any(x in url for x in rogue_suffixes):
        splitter = re.search('/index.+?\.html', url).group(0)
        list = url.split(splitter)
        url = ''.join(list)
    if '-index.html' in url:
        splitter = re.search('/\d?\D+\d?\D*-index.html', url).group(0)
        list = url.split(splitter)
        url = ''.join(list)


    tags = soup('a')
    for tag in tags:
        link_url = create_url(url, tag.get('href'))
        text = tag.get_string  
        parse_link(link_url, tag) 
        
    
if __name__ == "__main__":
    
    global suffix, log, links_count, tables_count
        
    year = str(sys.argv[1])
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
    log = open(log_filename, 'w') 
    print('Crawling through school year ' + school_year)
    log.write('Crawling through school year ' + school_year + '\n')
    
    #counts
    links_count = 0
    tables_count = 0

    # parse url
    url = 'http://e-aitisi.sch.gr'
    if year != '2016':
        url += suffix
    parse_url(url)
    
    # end output
    parse_result = '\nDone\n\nFound ' + str(links_count) + ' links and ' + str(tables_count) + ' tables'
    log.write(parse_result)
    print(parse_result)
    
