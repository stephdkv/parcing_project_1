import time
import datetime
import json
import os
import base64

import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO
import pickle
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By



from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

option = webdriver.FirefoxOptions()
option.set_preference('dom.webdriver.enable', False)
option.set_preference('webnotifications.enable', False)
option.set_preference('general.useragent.override', 'firefox142134')

driver = webdriver.Firefox(options=option)

driver.get('https://nb-bet.com/odds-scanner')
# Авторизация по логину и паролю
xpath = '//html/body/div/div[3]/div/div[1]/div/div[3]/a[1]'
button = driver.find_element(By.LINK_TEXT, 'Вход').click()

def download_outcome_details():
    with open('outcome-details.json', 'r') as file:
        json_data = json.load(file)

    parsed_data = json.loads(json_data)
    odds_history = parsed_data['data']['2']['oddsHistory']
    timestamps = [str(entry[0])[:-3] for entry in odds_history]  # Обрезаем последние три символа
    datetime_obj = [datetime.fromtimestamp(int(timestamp)) for timestamp in timestamps]
    formatted_datetimes = [dt.strftime('%Y-%m-%d %H:%M:%S') for dt in datetime_obj]
    odds = [entry[1] for entry in odds_history]

# Построим график
    plt.figure(figsize=(10, 6))
    plt.plot(formatted_datetimes, odds, label='Событие', marker='o', linestyle='-')
    plt.xticks(formatted_datetimes[::4])
# Добавим подписи к осям и легенду
    plt.xlabel('Дата')
    plt.ylabel('Коэффициент')
    plt.legend()

# Отобразим график
    return plt.show()

try:
     input_field_username = WebDriverWait(driver, 10).until(
         EC.visibility_of_element_located((By.CSS_SELECTOR, "input[autocomplete='username']"))
     )
     input_field_username.send_keys("rustammeleuz@mail.ru")
     input_field_pass = WebDriverWait(driver, 10).until(
         EC.visibility_of_element_located((By.CSS_SELECTOR, "input[autocomplete='current-password']"))
     )
     input_field_pass.send_keys("2MX-JsN-zhw-gCf")
     button_login = driver.find_element(By.CSS_SELECTOR, "button.ui.small.green.button").click()
     link_scanner = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//a[text()="Сканер коэффициентов"]'))
     )
     driver.execute_script("arguments[0].click();", link_scanner)
     time.sleep(2)
     button_templates = driver.find_element(By.XPATH, '//button[contains(text(), "Шаблоны фильтрации")]')
     button_templates.click()


     wait = WebDriverWait(driver, 10)
     popup_window = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'sc-38c386b7-1.kxPJfk')))


     button_apply = popup_window.find_element(By.XPATH, '//span[text()="Шаблон 1"]/parent::div/following-sibling::button[contains(text(), "Применить")]')
     button_apply.click()
     time.sleep(2)

     """ select_element = driver.find_element(By.CLASS_NAME, 'match-interval')
     select = Select(select_element)
     select.select_by_value('3')
     time.sleep(2)
     button_more_filters = driver.find_element(By.XPATH, '//button[contains(text(), "Ещё фильтры")]').click()

     select_elements = driver.find_elements(By.CLASS_NAME, 'sc-be4cb0a4-0.jPDJCm')
     for select_element in select_elements: 
        select = Select(select_element)
        options = select.options
        for option in options:
            if option.text == '20%':
                option.click()
                break
     time.sleep(2) 
     select_element_current_kfs = driver.find_element(By.CSS_SELECTOR, '.sc-be4cb0a4-0.jPDJCm')
     for select_element_current_kf in select_element_current_kfs: 
        select = Select(select_element_current_kf)
        options = select.options
        for option in options:
            if option.text == 'Ввести вручную':
                option.click()
                break

     input_element = driver.find_element(By.CSS_SELECTOR, '.sc-be4cb0a4-0.jPDJCm')
     input_element.clear()
     input_element.send_keys('5') """

     
     matches = driver.find_elements(By.CLASS_NAME, 'sc-6bb785d7-6.fSHdDF')
    
     all_matches = []
     
     for match in matches:
         teams = match.find_element(By.CSS_SELECTOR, ".sc-6bb785d7-3.bYIXeR").text.split('\n')
         date = match.find_element(By.XPATH, "/html/body/div/div[3]/div/div[1]/div/div[3]/div[1]/a/div/div[1]/div[1]/div[1]").text
         ishod_match = match.find_element(By.XPATH, "/html/body/div/div[3]/div/div[1]/div/div[3]/div[33]/a/div/div[2]/div[1]").text
         percent_change = match.find_element(By.CSS_SELECTOR, ".fGylKZ span").text
         data = {
        "teams": teams,
        "date": f'{date} {datetime.datetime.today().date()}',
        "ishod_match": ishod_match,
        "percent_change": percent_change,

    }
         all_matches.append(data)
         podrobnee_btn = match.find_element(By.TAG_NAME, 'button').click()
         time.sleep(2)
         canvas_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div/div[3]/div/div[1]/div/div[3]/div[1]/div/div[1]/div/div[3]/canvas')))
         canvas_base64 = driver.execute_script('return arguments[0].toDataURL("image/png").substring(21);', canvas_element)
    
         with open(f'canvas_image_{matches.index(match)}.png', 'wb') as f:
            f.write(base64.b64decode(canvas_base64))
         
         
finally:
    pass
