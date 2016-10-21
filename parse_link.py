import re

def parse_link(url, tag):
    result = ''
    filename = ''
    global links_count
    global tables_count
    global log
    
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
        # fix crazy 2011 link
        if url != 'http://e-aitisi.sch.gr/eniaios_smea_orom_11_B/index.html':
            parse_url(url)
        else:
            log.write('Crazy link to 2013-2014 index\n')
        
        
    else:
        result = '--Not xls, html, or gz ' + url + ' ' + str(tag.contents) + '\n'
        log.write(result)