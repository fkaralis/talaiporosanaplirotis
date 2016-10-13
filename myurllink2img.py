#finds all img tags

import urllib.request, urllib.parse, urllib.error
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import os
import time

#url = input('Enter - ')
url = 'http://www.in.gr'
html = urlopen(url).read()
soup = BeautifulSoup(html, 'html.parser')

# Retrieve tags
count = 0
tags = soup('img')
for tag in tags:
    count += 1
    src = tag.get('src', None)
    alt = tag.get('alt')

    print(count)
    print('TAG:', tag)
    print('SRC:', src)
    print('ALT:', alt, '\n\n')
    
    img_name = src.rsplit('/', 1)[-1]
    img_url = url + '/' + src
    img = urllib.request.urlopen(img_url).read()
    
    fhand = open(img_name, 'wb')
    fhand.write(img)
    fhand.close()
    
    time.sleep(2)
    
    




#print(soup.get_text())
