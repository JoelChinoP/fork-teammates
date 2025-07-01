from check_connection import SeleniumConnection
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time, json
from utils import Utils

class TestFn02:
    def __init__(self, driver, url):
        self.driver, self.url, self.path = driver, url, "/web/front/help/session-links-recovery"
        self.form_fields = {
            "email": (By.XPATH, "//input[@type='email']"),
        }
        with open("data/fn02.json") as f:
            self.cases = json.load(f)
    
    def go_to_form(self):
        self.driver.get(self.url + self.path)
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
        # El botón "Submit" no tiene un ID, se selecciona por XPATH
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()

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
        
        locator = case["element_locator"]
        obtained_msg = self.get_message(locator)

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
        print(f"******************** RUN TEST-FN02 IN ********************")
        for case in self.cases:
            self.run_case(case)
        print(f"******************** **************** ********************")
        print("")

if __name__ == "__main__":
    checker = SeleniumConnection()
    driver, url = checker.connect_and_check_login()
    TestFn02(driver, url).run()