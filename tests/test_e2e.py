import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = "http://127.0.0.1:5000"


@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    yield driver
    driver.quit()


def test_register_flow(driver):
    driver.get(f"{BASE_URL}/register")
    driver.find_element(By.NAME, "username").send_keys("e2euser")
    driver.find_element(By.NAME, "password").send_keys("pw")
    driver.find_element(By.NAME, "confirm").send_keys("pw")
    driver.find_element(By.CSS_SELECTOR, "button[type=submit]").click()
    time.sleep(1)
    assert "Please log in" in driver.page_source


def test_login_flow(driver):
    driver.get(f"{BASE_URL}/login")
    driver.find_element(By.NAME, "username").send_keys("e2euser")
    driver.find_element(By.NAME, "password").send_keys("pw")
    driver.find_element(By.CSS_SELECTOR, "button[type=submit]").click()
    time.sleep(1)
    assert "Task" in driver.page_source or "Welcome" in driver.page_source


def test_create_task_e2e(driver):
    driver.get(f"{BASE_URL}/login")
    driver.find_element(By.NAME, "username").send_keys("e2euser")
    driver.find_element(By.NAME, "password").send_keys("pw")
    driver.find_element(By.CSS_SELECTOR, "button[type=submit]").click()
    time.sleep(1)

    driver.get(f"{BASE_URL}/tasks/new")
    driver.find_element(By.NAME, "title").send_keys("E2E Task")
    driver.find_element(By.CSS_SELECTOR, "button[type=submit]").click()
    time.sleep(1)

    assert "Task created" in driver.page_source
