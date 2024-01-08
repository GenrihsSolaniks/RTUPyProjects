# IMPORT LIBRARIES
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import time

import requests
import bs4

# DATA FOR WORK SEARCHING (QUESTIONS)
work_place = str(input("Vēlamā darba atrašanās vieta: "))
work_sphere = str(input("Amata kategorijas: "))
key_words = str(input("Atslēgvārdi: "))
salary_eur = str(input("Alga, sākot no: "))
salary_type = str(input("Izvelēties mēneša algu vai stundas likme: "))
work_time = str(input("Izvēlēties darba veidu (Pilna slodze / Pilnas slodzes maiņu darbs / Pusslodze / Noteikts termiņš / Prakse / Darbs pēc mācībām / Ārštata darbinieks): "))
work_lang = str(input("Izvēlēties Jums nepieciešamās valodas (Latviešu / Angļu / Krievu /): "))

# OPENING WEBSITE USING SELENIUM
service = Service()
option = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=option)

url = "https://cv.lv/lv"
driver.get(url)
time.sleep(2)
delay_time = 10

# COOKIES ACCEPT
accept = driver.find_element(By.CLASS_NAME, "cookie-consent-button")
accept.click()

# CHOOSING CITY
find_city_selector = WebDriverWait(driver, delay_time).until(EC.presence_of_all_elements_located((By.XPATH, '//input[@tabindex="0"]')))
find_city_selector = driver.find_element(By.XPATH, '//input[@tabindex="0"]')
driver.execute_script("arguments[0].click();", find_city_selector)
find_city_selector.send_keys(work_place)
find_city_selector.send_keys(Keys.TAB)

# CHOOSING WORK SPHERE
work_sphere_selector = WebDriverWait(driver, delay_time).until(EC.presence_of_all_elements_located((By.XPATH, '//input[@id="react-select-3-input"]')))
work_sphere_selector = driver.find_element(By.XPATH, '//input[@id="react-select-3-input"]')
driver.execute_script("arguments[0].click();", work_sphere_selector)
work_sphere_selector.send_keys(work_sphere)
work_sphere_selector.send_keys(Keys.TAB)

# ADDING KEY WORDS
key_words_selector = WebDriverWait(driver, delay_time).until(EC.presence_of_all_elements_located((By.XPATH, '//input[@id="react-select-2-input"]')))
key_words_selector = driver.find_element(By.XPATH, '//input[@id="react-select-2-input"]')
list_of_all_selectors_with_same_id = driver.find_elements(By.XPATH, '//input[@id="react-select-2-input"]')
second_key_word_selector = list_of_all_selectors_with_same_id[1]
driver.execute_script("arguments[0].click();", second_key_word_selector)
second_key_word_selector.send_keys(key_words)
second_key_word_selector.send_keys(Keys.TAB)

# PRESSING BUTTON "MORE OPTIONS"
more_options = WebDriverWait(driver, delay_time).until(EC.presence_of_all_elements_located((By.XPATH, '//button[@class="jsx-2273220519 btn-plain btn-plain--standard"]')))
more_options = driver.find_element(By.XPATH, '//button[@class="jsx-2273220519 btn-plain btn-plain--standard"]')
driver.execute_script("arguments[0].click();", more_options)

# ADDING MINIMAL SALARY
minimal_salary_selector = WebDriverWait(driver, delay_time).until(EC.presence_of_all_elements_located((By.XPATH, '//input[@name="salaryFrom"]')))
minimal_salary_selector = driver.find_element(By.XPATH, '//input[@name="salaryFrom"]')
minimal_salary_selector = WebDriverWait(driver, delay_time).until(EC.element_to_be_clickable((By.XPATH, '//input[@name="salaryFrom"]')))
driver.execute_script("arguments[0].click();", minimal_salary_selector)
minimal_salary_selector.clear()
minimal_salary_selector.send_keys(salary_eur)
minimal_salary_selector.send_keys(Keys.TAB)

# CHOOSING BETWEEN "MĒNEŠA ALGA" UN "STUNDAS LIKME"
salary_type_selector = WebDriverWait(driver, delay_time).until(EC.presence_of_all_elements_located((By.XPATH, '//input[@id="react-select-4-input"]')))
salary_type_selector = driver.find_element(By.XPATH, '//input[@id="react-select-4-input"]')
driver.execute_script("arguments[0].click();", salary_type_selector)
salary_type_selector.send_keys(salary_type)

# CHOOSING WORK TIME
work_time_selector = WebDriverWait(driver, delay_time).until(EC.presence_of_all_elements_located((By.XPATH, '//input[@id="react-select-5-input"]')))
work_time_selector = driver.find_element(By.XPATH, '//input[@id="react-select-5-input"]')
driver.execute_script("arguments[0].click();", work_time_selector)
work_time_selector.send_keys(work_time)
work_time_selector.send_keys(Keys.TAB)

# ADDING PRIORITIZED LANGUAGES
work_lang_selector = WebDriverWait(driver, delay_time).until(EC.presence_of_all_elements_located((By.XPATH, '//input[@id="react-select-6-input"]')))
work_lang_selector = driver.find_element(By.XPATH, '//input[@id="react-select-6-input"]')
driver.execute_script("arguments[0].click();", work_lang_selector)
work_lang_selector.send_keys(work_lang)
work_lang_selector.send_keys(Keys.TAB)

# PRESSING BUTTON "SHOW >>> RESULTS"
show_results = WebDriverWait(driver, delay_time).until(EC.presence_of_all_elements_located((By.XPATH, '//button[@class="jsx-2393269544 btn btn--width-full"]')))
show_results = driver.find_element(By.XPATH, '//button[@class="jsx-2393269544 btn btn--width-full"]')
driver.execute_script("arguments[0].click();", show_results)
time.sleep(10)

# SAVING NEW URL AFTER SELENIUM AUTOMATIZATION (CHANGES), FOR USING BS4 AND GET DATA
url_after_changes = driver.current_url
data = requests.get(url_after_changes)

# RECIVING DATA FROM WEB PAGE USING BS4
if data.status_code == 200:
    page = bs4.BeautifulSoup(data.content, 'html.parser')

    # LISTS FOR STRUCTURIZING DATA
    list_for_work_title = []
    list_for_company_title = []
    list_for_salary = []
    list_for_expire_date = []
    complete_vacancy_title = []

    # TAKING VACANCY TITLE
    found_work_title = page.find_all(class_="jsx-3024910437 vacancy-item__title")

    # TAKING COMPANY NAME
    found_company_title = page.find_all("a", class_="jsx-3024910437")

    # TAKING SALARY
    found_salary_element = page.find_all("span", class_="jsx-3024910437 vacancy-item__salary-label")

    # TAKING VACANCY EXPIRY DATE
    found_expire_date_element = page.find_all("span", "jsx-3024910437 vacancy-item__expiry")

    # LOOP FOR ADDING INTO LIST WORK TITLES
    for x in found_work_title:
        list_for_work_title.append(x.string)
    
    # LOOP FOR ADDING INTO LIST COMPANY TITLES
    for y in found_company_title:
        if y.string is not None:
            list_for_company_title.append("==> Kompānijas nosaukums: " + y.string)

    # LOOP FOR ADDING INTO LIST SALARY INFORAMATION
    for w in found_salary_element:
        list_for_salary.append("==> Alga: " + w.string)

    # LOOP FOR ADDING INTO LIST VACANCY EXPIRY DATE
    for q in found_expire_date_element:
        list_for_expire_date.append("==> Vakances termiņš " + q.string)
    
    # WORK TITLE + COMPANY TITLE + SALARY + EXPIRE DATE
    for index1, index2, index3, index4 in zip(list_for_work_title, list_for_company_title, list_for_salary,list_for_expire_date):
        complete_vacancy_title.append(index1 + " " + index2 + " " + index3 + " " + index4)

    # RESULT OUTPUT :)   (NUMERĀCIJA)
    for index5, element in enumerate(complete_vacancy_title, start=1):
        if key_words in element:
            print(f"{index5}. {element}")
            print()

    driver.quit()

    # CHOOSE A VACANCY THAT YOU LIKE
    input_of_vacancy_number = int(input("Ievadiet vēlamās vakances numuru: "))
    if 1 <= input_of_vacancy_number <= len(complete_vacancy_title):
        selected_vacancy = complete_vacancy_title[input_of_vacancy_number - 1]
        print(f"Izvēlētā vakance: {selected_vacancy}")

    # OPENING WEBSITE USING SELENIUM
    service = Service()
    option = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=option)

    url = "https://cv.lv/lv"
    driver.get(url)
    time.sleep(2)
    delay_time = 10

    # COOKIES ACCEPT
    accept = driver.find_element(By.CLASS_NAME, "cookie-consent-button")
    accept.click()

    # ADDING KEY WORDS =====> SELECTED_VACANCY
    key_words_selected_vacancy = WebDriverWait(driver, delay_time).until(EC.presence_of_all_elements_located((By.XPATH, '//input[@id="react-select-2-input"]')))
    key_words_selected_vacancy = driver.find_element(By.XPATH, '//input[@id="react-select-2-input"]')
    list_of_all_selectors_with_same_id = driver.find_elements(By.XPATH, '//input[@id="react-select-2-input"]')
    second_key_word_selector = list_of_all_selectors_with_same_id[1]
    driver.execute_script("arguments[0].click();", second_key_word_selector)
    second_key_word_selector.send_keys(str(selected_vacancy))
    second_key_word_selector.send_keys(Keys.TAB)

    # PRESSING BUTTON "SHOW >>> RESULTS"
    show_results = WebDriverWait(driver, delay_time).until(EC.presence_of_all_elements_located((By.XPATH, '//button[@class="jsx-2393269544 btn btn--width-full"]')))
    show_results = driver.find_element(By.XPATH, '//button[@class="jsx-2393269544 btn btn--width-full"]')
    driver.execute_script("arguments[0].click();", show_results)
    time.sleep(10)

    # PRESSING ON A SELECTED VACANCY TO OPEN PAGE FOR MORE IFORMATION
    link_to_selected_vacancy = WebDriverWait(driver, delay_time).until(EC.presence_of_all_elements_located((By.XPATH, '//a[@class="jsx-3024910437 vacancy-item"]')))
    link_to_selected_vacancy = driver.find_element(By.XPATH, '//a[@class="jsx-3024910437 vacancy-item"]')
    list_of_all_links_with_same_class = driver.find_elements(By.XPATH, '//a[@class="jsx-3024910437 vacancy-item"]')
    first_link_to_vacancy = list_of_all_links_with_same_class[0]
    driver.execute_script("arguments[0].click();", first_link_to_vacancy)

    # PRESS ANY BUTTON TO FINNISH :)
    input("Nospiediet jebkuru taustiņu, lai pabeigtu...")
    driver.quit()