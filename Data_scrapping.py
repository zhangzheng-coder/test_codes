import urllib2
import pandas as pd
from bs4 import BeautifulSoup

url = 'http://appcenter.grupoice.com/CenceWeb/CencePosdespachoNacional.jsf'
html_doc = urllib2.urlopen(url).read()
#linechange test. 

soup = BeautifulSoup(html_doc, 'html.parser')

plantaSoup1 = soup.find('table', id='formPosdespacho:tableEx1').find('tbody')\
    .findAll('tr')[0]

plantaSoup2 = soup.find('tbody', id='formPosdespacho:tableEx1:tb')\
    .findAll('tr')

# it goes through all the rows, its not needed to change the index
for plantRow in plantaSoup2:
    plantNames = plantRow.findAll('td')[0].text.encode('ascii', 'ignore')

print plantNames

plant_list = []
power_list = []
for plantRow in plantaSoup2:
    power_list = []
    for hourly_power in plantRow.findAll('td'):
            power_list.append(hourly_power.text.encode('ascii', 'ignore'))
    plant_list.append(power_list)

df = pd.DataFrame(plant_list).T

print df
