
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


# This portion of the code is used to scrape the dispatch.

for year_i in range(2015, 2016):
    calendar = driver.wait.until(EC.presence_of_element_located((By.ID, "formPosdespacho:pickFechaInputDate")))
    calendar.click()

    box = driver.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "rich-calendar-month")))
    box.click()

    year = driver.wait.until(EC.presence_of_element_located((By.ID, "formPosdespacho:pickFechaDateEditorLayoutY3")))
    year.click()

    time.sleep(1)

    for month_i in range(2, 4):

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

        for day_i in range(2, 5):

            print day_i

            calendar = driver.wait.until(EC.presence_of_element_located((By.ID, "formPosdespacho:pickFechaInputDate")))
            calendar.click()
            day = driver.wait.until(EC.presence_of_element_located((By.ID, "formPosdespacho:pickFechaDayCell" + str(day_i + (datetime(year_i, month_i, 1).weekday() - 1)))))
            day.click()
            calendar.click()
            calendar.send_keys(Keys.RETURN)

            print 'day loop'
            time.sleep(1)

            html = driver.page_source
# Download into Python
            soup = BeautifulSoup(html, 'html.parser')
# Searches through HTML
            table = soup.find('table', {"class": "tablaDatos"})
# looks for the table, I have to look into the name or class.
            col_headers = []
            for header in table.thead.findAll("tr")[0].findAll("th"):
                col_headers.append(header.text)
            plants = []
            for row in table.tbody.findAll("tr"):
                plant = []
                for val in row.findAll("td"):
                    plant.append(val.text)
                plants.append(plant)

            df = pd.DataFrame(plants, columns=col_headers)
# These two loops go around the cells and form the table of interest.

        calendar = driver.wait.until(EC.presence_of_element_located((By.ID, "formPosdespacho:pickFechaInputDate")))
        calendar.click()
        box = driver.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "rich-calendar-month")))
        box.click()
        print 'Month re-start'

# This portion of the code will stract the info from the exchanges



driver.quit()
driver = init_driver()

driver.get("http://appcenter.grupoice.com/CenceWeb/CenceIntercambios.jsf?init=true")

html = driver.page_source

html[html.find('var chart_graficoIntercambios'):html.find('<!--END Script Block for Chart graficoIntercambios-->')]

Header = html[html.find('categories'):html.find('dataset seriesName=\'Real Norte\'')]

RN = html[html.find('seriesName=\'Real Norte\''):html.find(';dataset seriesName=\'Real Sur\'')]

RN = RN.replace(",", ".")

found = re.findall('&lt;set value=\'(.+?)\'/&gt;', RN)
