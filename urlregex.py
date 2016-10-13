import urllib.request, urllib.parse, urllib.error
import re

url = input('Enter - ')
html = urllib.request.urlopen(url).read()
count = 0

links = re.findall(b'href="(http://.*?)"', html)
for link in links:
    count += 1
    print(count, link.decode())