
# coding: utf-8
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

# This portion of the code is used to scrape the post-dispatch.
df_anual = pd.DataFrame()
df_totals = pd.DataFrame()
driver = init_driver()
driver.get("http://appcenter.grupoice.com/CenceWeb/CencePosdespachoNacional.jsf")

calendar = driver.wait.until(EC.presence_of_element_located((By.ID, "formPosdespacho:pickFechaInputDate")))

calendar.click()

box = driver.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "rich-calendar-month")))
box.click()

y = 2
for year_i in range(2014, 2015):

    print "Year Loop"
    print year_i

    year = driver.wait.until(EC.presence_of_element_located((By.ID, "formPosdespacho:pickFechaDateEditorLayoutY" + str(y))))
    year.click()

    time.sleep(1)

    df_month = pd.DataFrame()
    for month_i in range(1, 12):

        print ' Month loop ' + str(month_i)

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

        if month_i == 1:
            number_of_days = 31
        elif month_i == 2:
            number_of_days = 28
        elif month_i == 3:
            number_of_days = 31
        elif month_i == 4:
            number_of_days = 30
        elif month_i == 5:
            number_of_days = 31
        elif month_i == 6:
            number_of_days = 30
        elif month_i == 7:
            number_of_days = 30
        elif month_i == 8:
            number_of_days = 31
        elif month_i == 9:
            number_of_days = 30
        elif month_i == 10:
            number_of_days = 31
        elif month_i == 11:
            number_of_days = 30
        elif month_i == 12:
            number_of_days = 31

        for day_i in range(1, number_of_days + 1):

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
            df_day = pd.DataFrame()
            for row in table.tbody.findAll("tr"):
                plant = []
                df_plant = pd.DataFrame()
                for val in row.findAll("td"):
                    plant.append(val.text)
                df_plant = pd.DataFrame(plant)
                df_plant.columns = df_plant.iloc[0]
                df_plant = df_plant.drop(df_plant.index[[0, 25]])
                df_day = df_day.T.append(df_plant.T)
                df_day = df_day.T
            datetime_list = []
            for hour in range(0, 24):
                datetime_list.append(datetime(year_i, month_i, day_i, int(hour)))
            df_day['datetime'] = datetime_list
            df_day = df_day.set_index('datetime')
            # These two loops go around the cells and form the table of interest.
            df_month = df_month.append(df_day)
        calendar = driver.wait.until(EC.presence_of_element_located((By.ID, "formPosdespacho:pickFechaInputDate")))
        calendar.click()
        box = driver.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "rich-calendar-month")))
        box.click()

    time.sleep(5)
    df_anual = df_anual.append(df_month)
    y = 5
df_anual_Post = df_anual.fillna(0)
df_anual_Post.to_csv('df_anual_Post.csv', encoding='utf-8')

# This portion of the code is used to scrape the pre-dispatch.

df_anual = pd.DataFrame()
df_totals = pd.DataFrame()
driver.quit()
driver = init_driver()
driver.get("http://appcenter.grupoice.com/CenceWeb/CencePredespachoTecnicoNacional.jsf")
calendar = driver.wait.until(EC.presence_of_element_located((By.ID, "formPredespacho:pickFechaInputDate")))

calendar.click()

box = driver.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "rich-calendar-month")))
box.click()

y = 2
for year_i in range(2015, 2016):

    print "Year Loop"
    print year_i

    year = driver.wait.until(EC.presence_of_element_located((By.ID, "formPredespacho:pickFechaDateEditorLayoutY" + str(y))))
    year.click()

    time.sleep(1)

    df_month = pd.DataFrame()
    for month_i in range(1, 12):

        print ' Month loop ' + str(month_i)

        month = driver.wait.until(EC.presence_of_element_located((By.ID, "formPredespacho:pickFechaDateEditorLayoutM" + str(month_i - 1))))
        month.click()

        time.sleep(1)

        ok = driver.wait.until(EC.presence_of_element_located((By.ID, "formPredespacho:pickFechaDateEditorButtonOk")))
        ok.click()

        time.sleep(1)

        day_i = driver.wait.until(EC.presence_of_element_located((By.ID, "formPredespacho:pickFechaDayCell15")))
        day_i.click()
        calendar.click()
        calendar.send_keys(Keys.RETURN)

        time.sleep(1)

        if month_i == 1:
            number_of_days = 31
        elif month_i == 2:
            number_of_days = 28
        elif month_i == 3:
            number_of_days = 31
        elif month_i == 4:
            number_of_days = 30
        elif month_i == 5:
            number_of_days = 31
        elif month_i == 6:
            number_of_days = 30
        elif month_i == 7:
            number_of_days = 30
        elif month_i == 8:
            number_of_days = 31
        elif month_i == 9:
            number_of_days = 30
        elif month_i == 10:
            number_of_days = 31
        elif month_i == 11:
            number_of_days = 30
        elif month_i == 12:
            number_of_days = 31

        print ' day loop'
        for day_i in range(1, number_of_days):

            print "     " + str(day_i) + " " + str(month_i) + " " + str(year_i)

            calendar = driver.wait.until(EC.presence_of_element_located((By.ID, "formPredespacho:pickFechaInputDate")))
            calendar.click()
            day = driver.wait.until(EC.presence_of_element_located((By.ID, "formPredespacho:pickFechaDayCell" + str(day_i + (datetime(year_i, month_i, 1).weekday() - 1)))))
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
            df_day = pd.DataFrame()
            for row in table.tbody.findAll("tr"):
                plant = []
                df_plant = pd.DataFrame()
                for val in row.findAll("td"):
                    plant.append(val.text)
                df_plant = pd.DataFrame(plant)
                df_plant.columns = df_plant.iloc[0]
                df_plant = df_plant.drop(df_plant.index[[0, 25]])
                df_day = df_day.T.append(df_plant.T)
                df_day = df_day.T
            datetime_list = []
            for hour in range(0, 24):
                datetime_list.append(datetime(year_i, month_i, day_i, int(hour)))
            df_day['datetime'] = datetime_list
            df_day = df_day.set_index('datetime')
            # These two loops go around the cells and form the table of interest.
            df_month = df_month.append(df_day)
        calendar = driver.wait.until(EC.presence_of_element_located((By.ID, "formPredespacho:pickFechaInputDate")))
        calendar.click()
        box = driver.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "rich-calendar-month")))
        box.click()

    time.sleep(5)
    df_anual = df_anual.append(df_month)
    y = 5
df_anual_pre = df_anual.fillna(0)
df_anual_pre.to_csv('df_anual_pre.csv', encoding='utf-8')

# This portion of the code will stract the info from the exchanges
#driver.quit()
#driver = init_driver()

#driver.get("http://appcenter.grupoice.com/CenceWeb/CenceIntercambios.jsf?init=true")

#html = driver.page_source

#html[html.find('var chart_graficoIntercambios'):html.find('<!--END Script Block for Chart graficoIntercambios-->')]

#Header = html[html.find('categories'):html.find('dataset seriesName=\'Real Norte\'')]

#hfound = re.findall(';&lt;category label=(.+?)showLabel', Header)

#RN = html[html.find('seriesName=\'Real Norte\''):html.find(';dataset seriesName=\'Real Sur\'')]

#RN = RN.replace(",", ".")

#found = re.findall('&lt;set value=\'(.+?)\'/&gt;', RN)

#nfound = []
#for x in found:
#    nfound.append(float(x.encode('ascii', 'ignore')))
#Header.encode('ascii', 'ignore')
