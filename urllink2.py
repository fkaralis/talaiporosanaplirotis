from urllib.request import urlopen
from bs4 import BeautifulSoup

url = input('Enter - ')
html = urlopen(url).read()
soup = BeautifulSoup(html, 'html.parser')

# Retrieve tags
count = 0
tags = soup('a')
for tag in tags:
    count += 1
    # look at tag parts
    print(count)
    print('TAG:', tag)
    print('URL:', tag.get('href', None))
    print('Contents:', tag.contents[0])
    print('Attrs:', tag.attrs, '\n')

