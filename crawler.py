import requests
from bs4 import BeautifulSoup
import json

def create_url(url, href):
    return url + '/' + href

def parse_link(url, text):
    
    filetypes = ['.xls', '.xlsx', '.csv']
    
    if any(url.endswith(x) for x in filetypes):
        print('Found xcel:', url, text)
        response = requests.get(url)
        filename = url.rsplit('/', 1)[1]
        
        with open(filename, 'wb') as output:
            output.write(response.content)
        print('Downloaded')
        
    elif url.endswith('html'):
        print('Found html', url, text)
        
    else:
        print('Found neither xcel nor html', url, text)


if __name__ == "__main__":
    url = 'http://e-aitisi.sch.gr'
    html = requests.get(url)
    html.encoding = 'ISO-8859-7'
    soup = BeautifulSoup(html.content, 'html.parser')
    
    tags = soup('a')
    count = 0
    for tag in tags:
        link_url = create_url(url, tag.get('href'))
        text = tag.get_string

        parse_link(link_url, text)       
        
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
    
