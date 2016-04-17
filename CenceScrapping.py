
# coding: utf-8

# In[47]:

import time
import re
from datetime import datetime
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from pprint import pprint


def init_driver():
    driver = webdriver.Chrome()
    driver.wait = WebDriverWait(driver, 5)
    return driver

driver = init_driver()

df_month = pd.DataFrame()
df_anual = pd.DataFrame()
df_totals = pd.DataFrame()

# This portion of the code is used to scrape the dispatch.

calendar = driver.wait.until(EC.presence_of_element_located((By.ID, "formPosdespacho:pickFechaInputDate")))

calendar.click()

box = driver.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "rich-calendar-month")))
box.click()

y = 2
for year_i in range(2014, 2016):

    print "Year Loop"
    print year_i

    year = driver.wait.until(EC.presence_of_element_located((By.ID, "formPosdespacho:pickFechaDateEditorLayoutY" + str(y))))
    year.click()

    time.sleep(1)

    print ' Month loop'
    for month_i in range(4, 6):

        print month_i

        month = driver.wait.until(EC.presence_of_element_located((By.ID, "formPosdespacho:pickFechaDateEditorLayoutM" + str(month_i - 1))))
        month.click()

        time.sleep(1)

        ok = driver.wait.until(EC.presence_of_element_located((By.ID, "formPosdespacho:pickFechaDateEditorButtonOk")))
        ok.click()

        time.sleep(1)

        day_i = driver.wait.until(EC.presence_of_element_located((By.ID, "formPosdespacho:pickFechaDayCell15")))
        day_i.click()
        calendar.click()
        calendar.send_keys(Keys.RETURN)

        time.sleep(1)

        print ' day loop'
        for day_i in range(10, 13):

            print "     " + str(day_i) + " " + str(month_i) + " " + str(year_i)

            calendar = driver.wait.until(EC.presence_of_element_located((By.ID, "formPosdespacho:pickFechaInputDate")))
            calendar.click()
            day = driver.wait.until(EC.presence_of_element_located((By.ID, "formPosdespacho:pickFechaDayCell" + str(day_i + (datetime(year_i, month_i, 1).weekday() - 1)))))
            day.click()
            calendar.click()
            calendar.send_keys(Keys.RETURN)
            time.sleep(1)
            html = driver.page_source
            # Download into Python
            soup = BeautifulSoup(html, 'html.parser')
            # Searches through HTML
            table = soup.find('table', {"class": "tablaDatos"})
            # looks for the table, I have to look into the name or class.
            col_headers = ['año', 'mes', 'dia']
            for header in table.thead.findAll("tr")[0].findAll("th"):
                col_headers.append(header.text)
            plants = []
            for row in table.tbody.findAll("tr"):
                date = [str(year_i), str(month_i), str(day_i)]
                plant = date
                for val in row.findAll("td"):
                    plant.append(val.text)
                plants.append(plant)

            df_day = pd.DataFrame(plants, columns=col_headers)
            # These two loops go around the cells and form the table of interest.
            del df_day['Total']
            df_month = df_month.append(df_day, ignore_index=True)
        calendar = driver.wait.until(EC.presence_of_element_located((By.ID, "formPosdespacho:pickFechaInputDate")))
        calendar.click()
        box = driver.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "rich-calendar-month")))
        box.click()

    time.sleep(5)
    df_anual = df_anual.append(df_month, ignore_index=True)
    df_totals = df_totals.append(df_anual[df_anual.Planta == 'Total'], ignore_index=True)
    df_anual = df_anual[df_anual.Planta != 'Total']
    del df_totals['Planta']
    y = 5


# This portion of the code will stract the info from the exchanges
driver.quit()
driver = init_driver()

driver.get("http://appcenter.grupoice.com/CenceWeb/CenceIntercambios.jsf?init=true")

html = driver.page_source

html[html.find('var chart_graficoIntercambios'):html.find('<!--END Script Block for Chart graficoIntercambios-->')]

Header = html[html.find('categories'):html.find('dataset seriesName=\'Real Norte\'')]

hfound = re.findall(';&lt;category label=(.+?)showLabel', Header)

RN = html[html.find('seriesName=\'Real Norte\''):html.find(';dataset seriesName=\'Real Sur\'')]

RN = RN.replace(",", ".")

found = re.findall('&lt;set value=\'(.+?)\'/&gt;', RN)

nfound = []
for x in found:
    nfound.append(float(x.encode('ascii', 'ignore')))
Header.encode('ascii', 'ignore')
