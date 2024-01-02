# Nepiecišamu bibliotēku importēšana

######################## Selenium bibliotēkas #######################

import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
####################### Bibliotēkas lai stradātu ar Excel failiem ######################

from openpyxl import Workbook, load_workbook
import pandas as pd

english_info = "English"
german_info = "German"
russian_info = "Russia"
chinese_info = "Chinese"
polish_info = "Polish"
portuguese_info = "Portuguese"

info_list = []

fail = pd.read_excel("data1.xlsx")
df_description = pd.DataFrame(fail)

if english_info in df_description['Language'].values:
    info_list = fail.values.tolist()

print(info_list)






















#service = Service()
#option = webdriver.ChromeOptions()
#driver = webdriver.Chrome(service=service, options=option)

#url = "https://www.deepl.com/translator"
#driver.get(url)
#time.sleep(2)

#find = driver.find_element(By.class,"er8xn")
#find.clear()
#find.send_keys(get_info)
#find = driver.find_element(By.ID,"output")
#temp = find.get_attribute("value")

