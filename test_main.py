import os

import pytest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

load_dotenv()
LOGIN = os.getenv('LOGIN')
PASSWORD = os.getenv('PASSWORD')


@pytest.fixture(scope='module')
def test_setup():
    global driver
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-notifications")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get('https://ru.wikipedia.org/w/index.php?title=Служебная:Вход')
    driver.implicitly_wait(10)
    yield driver


def test_input_fields(test_setup):
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'wpName1')))
    login_field = driver.find_element(By.ID, 'wpName1')
    password_field = driver.find_element(By.ID, 'wpPassword1')

    login_field.send_keys(LOGIN)
    password_field.send_keys(PASSWORD)

    assert LOGIN in login_field.get_attribute('value')
    assert PASSWORD in password_field.get_attribute('value')


def test_submit_button(test_setup):
    login_submit_button = driver.find_element(By.XPATH, '//*[@id="wpLoginAttempt"]')
    login_submit_button.click()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'Добро_пожаловать_в_Википедию,')))
    assert 'Добро пожаловать' in driver.find_element(By.ID, 'Добро_пожаловать_в_Википедию,').text


def test_logout(test_setup):
    logout_button = driver.find_element(By.ID, 'pt-logout')
    logout_button.click()
    WebDriverWait(driver, 10).until(EC.title_contains('Завершение сеанса'))
    assert 'Завершение сеанса' in driver.title
    driver.quit()