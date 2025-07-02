from check_connection import SeleniumConnection
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time, json
from utils import Utils

class TestFn05:
    def __init__(self, driver, url):
        self.driver, self.url, self.path = driver, url, "/web/admin/search"
        self.form_fields = {
            "search": (By.ID, "search-box"),
        }
        with open("data/fn06.json") as f:
            self.cases = json.load(f)

    def go_to_form(self):
        self.driver.get(self.url + self.path)
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, "search-box"))
        )