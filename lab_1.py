from selenium import webdriver
from selenium.webdriver.common.by import By
from math import log, sin
from time import sleep


def get_function_result(x_value):
    return log(abs(12 * sin(float(x_value))))


driver = webdriver.Chrome()
driver.get('http://suninjuly.github.io/math.html')

x = driver.find_element(By.ID, 'input_value').text

input_form = driver.find_element(By.XPATH, "//input")
input_form.send_keys(get_function_result(x))

driver.find_element(By.ID, 'robotCheckbox').click()
driver.find_element(By.ID, 'robotsRule').click()

driver.find_element(By.XPATH, "//button").click()

sleep(5)
driver.quit()
