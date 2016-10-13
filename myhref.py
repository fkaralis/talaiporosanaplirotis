import re

hand = open('href.txt')
c = 0
for line in hand:
    line = line.rstrip()
    if re.findall('^href', line) :
        c += 1
        print(c, line)
    
    if re.findall('index.html$', line) :
        c += 1
        print(c, line)
