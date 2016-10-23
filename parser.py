import re
from bs4 import BeautifulSoup
import requests

import globalvars

def parse_link(url, tag):
    
    filetypes = ['.xls', '.xlsx', '.csv']

    # (entirely useless) fix // in middle of url 
    url = re.sub(r'^((?:(?!//).)*//(?:(?!//).)*)//', r'\1/', url)
    
    if any(url.endswith(x) for x in filetypes):
        filename = url.rsplit('/')[-1]
        msg = 'Found excel table: ' + filename + ' ' + url + ' ' + str(tag.contents) + '\n'
        globalvars.tables_count += 1
        globalvars.log.write(msg)
    
    
    elif url.endswith('gz'):
        filename = url.rsplit('/')[-1]
        msg = 'Found gz table: ' + filename + ' ' + url + ' ' + str(tag.contents) + '\n'
        globalvars.tables_count += 1
        globalvars.log.write(msg)
    
        
    elif url.endswith('.html') and 'index' not in url:
        filename = url.rsplit('/')[-1]
        msg = 'Found html table: ' + filename + ' ' + url + ' ' + str(tag.contents) + '\n'
        globalvars.tables_count += 1
        globalvars.log.write(msg)

            
    elif ('index' in url and 'old' not in url) or url.endswith('/'):
        msg = '------------------\nFound link: ' + url + ' ' + str(tag.contents) + '\n'
        globalvars.log.write(msg)
        globalvars.links_count += 1
        if url != 'http://e-aitisi.sch.gr/triantamino_07/index.html' or url != 'http://e-aitisi.sch.gr/eniaios_smea_orom_11_B/index.html':   # 2007 link to 20016 index and 2011 link to 2013 index (!)
            parse_url(url)
        else:
            globalvars.log.write('Crazy 2007/2011 link to 2016/2013 index\n')
        
        
    else:
        msg = '--Not xls, html, or gz ' + url + ' ' + str(tag.contents) + '\n'
        globalvars.log.write(msg)


def create_url(url, href):
    if url.endswith('/index.html'):
        url = url[:-11]
    return url + '/' + href


def fix_url(url, suffix):  
    if suffix in url:       # initial index,html
        list = url.split(suffix)
        url = ''.join(list)        

    rogue_suffixes = ['/indexAB.html', '/indexC.html', '/indexG.html', 
                           '/indexABg.html', '/indexCg.html', '/indexGg.html']
    if any(x in url for x in rogue_suffixes):       # 2003-4
        splitter = re.search('/index.+?\.html', url).group(0)
        list = url.split(splitter)
        url = ''.join(list)
    if '-index.html' in url:        # ~2010 tadmon(TAD/ETAD)
        splitter = re.search('/\d?\D+\d?\D*-index.html', url).group(0)
        list = url.split(splitter)
        url = ''.join(list)
    if '_13/indexdior.html' in url:     # 2013
        splitter = re.search('/indexdior.html', url).group(0)
        list = url.split(splitter)
        url = ''.join(list)
    
    return url


def parse_url(url):
    html = requests.get(url)
    html.encoding = 'ISO-8859-7'
    soup = BeautifulSoup(html.content, 'html.parser')
    
    # fix .html suffixes in middle of url  
    url = fix_url(url, globalvars.suffix)

    tags = soup('a')
    for tag in tags:
        href = tag.get('href')
        if not re.match('index\d+\.html', href):        # end 2016
            link_url = create_url(url, href)
            parse_link(link_url, tag) 