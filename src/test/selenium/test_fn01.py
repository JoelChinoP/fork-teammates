from check_connection import SeleniumConnection
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time, json
from utils import Utils

class TestFn01:
    def __init__(self, driver, url):
        self.driver, self.url, self.path = driver, url, "/web/front/request"
        self.form_fields = {
            "name": (By.ID, "name"),
            "institution": (By.ID, "institution"),
            "country": (By.ID, "country"),
            "email": (By.ID, "email"),
            "comments": (By.ID, "comments"),
        }
        with open("data/fn01.json") as f:
            self.cases = json.load(f)

    def go_to_form(self):
        self.driver.get(self.url + self.path)
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'btn-am-instructor'))
            ).click()
        except TimeoutException:
            pass
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@type='submit']"))
        )

    def fill_form(self, fields):
        for key, value in fields.items():
            if key in self.form_fields:
                el = self.driver.find_element(*self.form_fields[key])
                el.clear()
                el.send_keys(value)

    def submit(self): 
        self.driver.find_element(By.ID, "submit-button").click()

    def get_message(self, locator):
        try:
            el = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, locator))
            )
            return el.text.strip()
        except (TimeoutException, NoSuchElementException):
            return ""

    def run_case(self, case):
        self.go_to_form()
        self.fill_form(case["fields"])
        Utils.solve_recaptcha(self.driver)
        self.submit()
        time.sleep(1.2)
        
        # Mensaje obtenido del DOM
        locator = case["element_locator"]
        obtained_msg = self.get_message(locator)

        # Log detallado (incluye esperado y obtenido)
        Utils.log_test(
            case["id"], 
            case["fields"], 
            case["expected"], 
            obtained_msg, 
            case["Obs"]
        )
        return {
            "id": case["id"],
            "expected": case["expected"],
            "obtained": obtained_msg
        }

    def run(self):
        print(f"******************** RUN TEST-FN01 IN ********************")
        for case in self.cases:
            self.run_case(case)
        print(f"******************** **************** ********************")
        print("")

if __name__ == "__main__":
    checker = SeleniumConnection()
    driver, url = checker.connect_and_check_login()
    TestFn01(driver, url).run()