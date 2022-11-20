from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from math import log, sin
from time import sleep


def get_function_result(x_value):
    return log(abs(12 * sin(float(x_value))))


driver = webdriver.Chrome()
driver.get('http://suninjuly.github.io/explicit_wait2.html')

try:
    WebDriverWait(driver, 20).until(
        ec.text_to_be_present_in_element((By.ID, "price"), '100')
    )
    driver.find_element(By.ID, 'book').click()

    x = driver.find_element(By.ID, 'input_value').text
    input_form = driver.find_element(By.XPATH, "//input")
    input_form.send_keys(get_function_result(x))

    driver.find_element(By.ID, 'solve').click()

    sleep(5)

finally:
    driver.quit()
