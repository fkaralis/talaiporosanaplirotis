# missing πίνακες zero Προϋπηρεσίας με ίδιο όνομα

import requests
from bs4 import BeautifulSoup
import json
import os, os.path

def create_url(url, href):
    if url.endswith('/index.html'):
        url = url[:-11]
    return url + '/' + href

def parse_link(url, tag):
    
    filetypes = ['.xls', '.xlsx', '.csv']
    
    if any(url.endswith(x) for x in filetypes):
        print('--xcel:', url, tag.contents)
        
        filename = url.rsplit('/', 1)[1]
        if not os.path.isfile(filename):
            response = requests.get(url)
            with open(filename, 'wb') as output:
                output.write(response.content)
            print('Downloaded')
        else: 
            print('Already there')
        
    elif url.endswith('index.html'):
        print('--index.html', url, tag.contents)
        parse_url(url)
        
        
    else:
        print('--Not xcel nor index.html', url, tag.contents)
'''        
        reply = input('Download file? (y/n) ')
        if reply == 'y':
            with open(filename, 'wb') as output:
                output.write(response.content)
            print('Downloaded')
'''


def parse_url(url):
    html = requests.get(url)
    html.encoding = 'ISO-8859-7'
    soup = BeautifulSoup(html.content, 'html.parser')
    
    tags = soup('a')
    count = 0
    for tag in tags:
        link_url = create_url(url, tag.get('href'))
        text = tag.get_string
        parse_link(link_url, tag) 
    
if __name__ == "__main__":
    url = 'http://e-aitisi.sch.gr'
    global path 
    path = '2015-2026'
    os.makedirs(path)
    parse_url(url)
    
        
''' VERSION 1 build links list (created before 'for') & json 
     
        
        href = tag.get('href')
        
        #create dict for link
        link = {
            'link_url': url + '/' + href,
            'text' : tag.string,
        }
        
        # add link to links list 
        links.append(link)
    
    print(links)
    print(json.dumps(links, sort_keys=True, indent=4))


    d = {"name":"links",
         "children": links}
    j = json.dumps(d, sort_keys=True, indent=4)
    with open('links.json', 'w') as fp:
        json.dump(j, fp)
'''   
    
