import urllib.request, urllib.parse, urllib.error
import re

#url = input('Enter - ')
url = 'http://e-aitisi.sch.gr'
html = urllib.request.urlopen(url).read()
count = 0

links = re.findall(b'href="(.*)"', html)
for link in links:
    count += 1
    print(count, link.decode())
    