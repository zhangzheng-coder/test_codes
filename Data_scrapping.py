import urllib2
import pandas as pd
from bs4 import BeautifulSoup

url = 'http://appcenter.grupoice.com/CenceWeb/CencePosdespachoNacional.jsf'
html_doc = urllib2.urlopen(url).read()

soup = BeautifulSoup(html_doc, 'html.parser')

plantaSoup1 = soup.find('table', id='formPosdespacho:tableEx1').find('tbody')\
    .findAll('tr')[0]

plantaSoup2 = soup.find('tbody', id='formPosdespacho:tableEx1:tb')\
    .findAll('tr')

# it goes through all the rows, its not needed to change the index
for plantRow in plantaSoup2:
    plantNames = plantRow.findAll('td')[0].text.encode('ascii', 'ignore')

print plantNames

for plantRow in plantaSoup2:
    for hourly_power in plantRow.findAll('td'):
            print hourly_power.text.encode('ascii', 'ignore')
