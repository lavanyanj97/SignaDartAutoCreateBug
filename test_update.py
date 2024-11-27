import json
import random
import string
import time
from time import sleep
import inspect
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pytest

def click(driver, xpath, retries=3, error_message="Element click failed"):
    for attempt in range(retries):
        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
            return
        except Exception as e:
            if attempt == retries - 1:
                caller_function_name = inspect.stack()[1].function
                raise AssertionError(
                    f"{error_message} in function '{caller_function_name}': Could not click element with XPath: {xpath}. Error: {str(e)}"
                )

def send_keys(driver, xpath, keys):
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath))).send_keys(keys)
    except Exception as e:
        raise AssertionError(f"Failed to send keys to {xpath}: {str(e)}")

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument("--headless")  # Run Chrome in headless mode
    options.add_argument("--start-maximized")  # Optional: Start with maximized window
    options.add_argument("--disable-gpu")  # Disable GPU acceleration (necessary for headless mode)
    service = Service(ChromeDriverManager().install())  # Automatically installs the correct version of ChromeDriver
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_login(driver):
    driver.get("https://signadart.ai/")
    click(driver, "//span[@class='block text-inherit w-full h-full rounded-md text-sm md:text-lg font-chivo font-semibold']")
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h3[text()='Sign Up']"))
        )
    except TimeoutException:
        pytest.fail("Element with text 'Sign Up' not found.")

def test_signup(driver):
    send_keys(driver, "//input[@name='firstName']", "test")
    click(driver, "//button[text()='Sign Up']")
