
# coding: utf-8

# In[47]:

import time
from datetime import datetime
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
 
def init_driver():
    driver = webdriver.Chrome()
    driver.wait = WebDriverWait(driver, 5)
    return driver


# In[ ]:




# In[55]:

driver.quit()
driver = init_driver()
#dfs = lookup(driver, "Selenium")
year = 2016
month = 4
day = 5
driver.get("http://appcenter.grupoice.com/CenceWeb/CencePosdespachoNacional.jsf")


box = driver.wait.until(EC.presence_of_element_located(
                (By.ID, "formPosdespacho:pickFechaInputDate")))
box.click()
calendar = driver.wait.until(EC.presence_of_element_located(
        (By.ID, "formPosdespacho:pickFecha")))
date = calendar.find_element(By.ID,"formPosdespacho:pickFechaDayCell"+str(day+(datetime(year,month,1).weekday()-1)))
date.click()


calendar = driver.wait.until(EC.presence_of_element_located(
        (By.ID, "formPosdespacho:pickFechaInputDate")))
calendar.click()
date = driver.wait.until(EC.presence_of_element_located(
        (By.ID, "formPosdespacho:pickFechaDayCell4")))
calendar.send_keys(Keys.RETURN)


html = driver.page_source
#Download into Python
soup = BeautifulSoup(html, 'html.parser')
#Searches through HTML
table = soup.find('table',{"class":"tablaDatos"})
#looks for the table, I have to look into the name or class. 
col_headers = []
for header in table.thead.findAll("tr")[0].findAll("th"):
    col_headers.append(header.text)
plants = []
for row in table.tbody.findAll("tr"):
    plant = []
    for val in row.findAll("td"):
        plant.append(val.text)
    plants.append(plant)
df = pd.DataFrame(plants,columns=col_headers)
#These two loops go around the cells and form the table of interest. 


# In[63]:

#Code for the exchanges 
driver.quit()
driver = init_driver()

driver.get("http://appcenter.grupoice.com/CenceWeb/CenceIntercambios.jsf?init=true")

html = driver.page_source


# In[66]:

html[html.find('var chart_graficoIntercambios'):html.find('<!--END Script Block for Chart graficoIntercambios-->')]


# In[ ]:



