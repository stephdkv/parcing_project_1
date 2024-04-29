import time
from PIL import Image
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

driver = webdriver.Firefox()

driver.get('https://nb-bet.com/odds-scanner')
# Авторизация по логину и паролю
xpath = '//html/body/div/div[3]/div/div[1]/div/div[3]/a[1]'
button = driver.find_element(By.LINK_TEXT, 'Вход').click()
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
     button = driver.find_element(By.XPATH, "/html/body/div/div[4]/div/div[1]/div/div[3]/div[1]/div/button").click()
     time.sleep(1)
     
    # Ждем, пока элемент с изображением загрузится
     canvas_element = driver.find_element(By.CSS_SELECTOR, "canvas.chartjs-render-monitor")
     canvas_location = canvas_element.location

    # Получаем снимок экрана
     screenshot = driver.get_screenshot_as_png()
     screenshot_img = Image.open(BytesIO(screenshot))

    # Вырезаем область с изображением
     image = screenshot_img.crop((
         canvas_location['x'],
         canvas_location['y'],
         canvas_location['x'] + canvas_element.size['width'],
         canvas_location['y'] + canvas_element.size['height']
     ))
 
    # Сохраняем изображение
     image.save("image.png")

finally:
    pass
