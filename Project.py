import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

service = Service()
option = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=option)

url = "https://translate.google.com/"
driver.get(url)
time.sleep(2)

find = driver.find_element(By.class,"er8xn")
find.clear()
find.send_keys(get_info)
find = driver.find_element(By.ID,"output")
temp = find.get_attribute("value")

