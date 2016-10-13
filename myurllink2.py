from urllib.request import urlopen
from bs4 import BeautifulSoup

#url = input('Enter - ')
url = 'http://www.in.gr'
html = urlopen(url).read()
soup = BeautifulSoup(html, 'html.parser')



print(soup.p)
print(soup.a)
print(soup.find_all('img'))

#print(soup.get_text())
