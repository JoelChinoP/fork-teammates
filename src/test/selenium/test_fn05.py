from check_connection import SeleniumConnection
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time, json, sys
from utils import Utils

class TestFn05:
    def __init__(self, driver, url):
        self.driver, self.url, self.path = driver, url, "/web/admin/home"
        self.form_fields = {
            "name": (By.ID, "request-name"),
            "email": (By.ID, "request-email"),
            "institution": (By.ID, "request-institution"),
            "comments": (By.ID, "request-comments"),
        }
        with open("data/fn05.json") as f:
            self.cases = json.load(f)

    def go_to_form(self):
        self.driver.get(self.url + self.path)
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, "search-table-account-request"))
        )
        rows = self.driver.find_elements(By.XPATH, "//table[@id='search-table-account-request']/tbody/tr")
        if not rows:
            print("No hay solicitudes pendientes para editar."); self.driver.quit(); sys.exit(0)
        self.driver.find_element(By.ID, "edit-account-request-0").click()
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, "btn-confirm-edit-request"))
        )

    def fill_form(self, fields):
        for key, value in fields.items():
            if key in self.form_fields:
                el = self.driver.find_element(*self.form_fields[key])
                el.clear()
                el.send_keys(value)

    def submit(self):
        self.driver.find_element(By.ID, "btn-confirm-edit-request").click()

    def get_message(self, locator):
        try:
            el = WebDriverWait(self.driver, 12).until(
                EC.visibility_of_element_located((By.XPATH, locator))
            )
            return el.text.strip()
        except (TimeoutException, NoSuchElementException):
            return ""

    def run_case(self, case):
        self.go_to_form()
        self.fill_form(case["fields"])
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
        print(f"******************** RUN TEST-FN05 IN ********************")
        for case in self.cases:
            self.run_case(case)
        print(f"******************** **************** ********************")
        print("")

if __name__ == "__main__":
    checker = SeleniumConnection()
    driver, url = checker.connect_and_check_login()
    TestFn05(driver, url).run()