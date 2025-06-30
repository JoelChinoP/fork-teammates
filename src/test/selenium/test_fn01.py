from check_connection import SeleniumConnection
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time, json
from utils import Utils

ERROR_MESSAGES = {
    "error_name": "Name must be shorter than 100 characters.",
    "error_institution": "Institution name must be shorter than 86 characters.",
    "error_country": "Country name must be shorter than 40 characters.",
    "error_email": "Email address must be shorter than 254 characters."
}

class TestFn01:
    def __init__(self, driver, url, cases):
        self.driver, self.url, self.path = driver, url, "/web/front/request"
        self.form_fields = {
            "name": (By.ID, "name"),
            "institution": (By.ID, "institution"),
            "country": (By.ID, "country"),
            "email": (By.ID, "email"),
            "comments": (By.ID, "comments"),
        }
        self.cases = cases

    def go_to_form(self):
        self.driver.get(self.url + self.path)
        try:
            WebDriverWait(self.driver, 5).until(
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
                el.clear(), el.send_keys(value)

    def submit(self): self.driver.find_element(By.ID, "submit-button").click()

    def detect_success(self):
        # Se detecta éxito si aparece el banner de éxito o el DOM cambia claramente (ajustar según implementación real)
        try:
            return WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Your instructor account request has been sent.')]"))
            ) is not None
        except TimeoutException:
            return False

    def get_errors(self):
        errors = []
        for msg in ERROR_MESSAGES.values():
            try:
                if self.driver.find_element(By.XPATH, f"//*[contains(text(), '{msg}')]").is_displayed():
                    errors.append(msg)
            except NoSuchElementException:
                pass
        return errors

    def run_case(self, case):
        self.go_to_form()
        self.fill_form(case["fields"])
        Utils.solve_recaptcha(self.driver)
        self.submit()
        time.sleep(1.2)
        errors = self.get_errors()
        success = self.detect_success()
        expected, obs = case["expected"], "f+"
        # Lógica de aserción tipo catálogo
        if expected == "success":
            obtained = "f+" if success and not errors else "f-"
        else:
            msg = ERROR_MESSAGES.get(expected, "")
            obtained = "f+" if msg and msg in errors and not success else "f-"
        # Log tras cada caso
        Utils.log_test(case["id"], case["fields"], expected, obtained, obs)
        return {"id": case["id"], "result": obtained, "errors": errors}

    def run(self):
        for case in self.cases:
            self.run_case(case)

if __name__ == "__main__":
    with open("data/fn01.json") as f:
        cases = json.load(f)
    checker = SeleniumConnection()
    driver, url = checker.connect_and_check_login()
    TestFn01(driver, url, cases).run()