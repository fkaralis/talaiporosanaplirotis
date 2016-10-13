import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup

#url = input('Enter - ')
url = 'http://e-aitisi.sch.gr'
html = urllib.request.urlopen(url).read()
soup = BeautifulSoup(html, 'html.parser')

# Retrieve tags
count = 0
tags = soup('a')
for tag in tags:
    count += 1
    print(count, tag.get('href', None))