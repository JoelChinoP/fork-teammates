from check_connection import SeleniumConnection
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time, json, sys
from utils import Utils

class TestFn16:
    def __init__(self, driver, url):
        self.driver, self.url, self.path = driver, url, "/web/instructor/sessions/edit"
        self.wait = WebDriverWait(self.driver, 10)

        courseid = "PS-Cigarra-2025"
        fsname = "selenium-test"
        self.path += f"?courseid={courseid}&fsname={fsname}&editingMode=true"

        self.form_fields = {
            "question": (By.XPATH, "//textarea[@id='question-brief' and not(@disabled)]"),
            "description": (By.XPATH, "//iframe[contains(@id, 'tiny-angular') and not(@disabled)]"),
        }
        with open("data/fn16.json") as f:
            self.cases = json.load(f)

    def go_to_form(self):
        self.driver.get(self.url + self.path)
        self.wait.until(
            EC.presence_of_element_located((By.ID, "btn-new-question"))
        )

    def select_new_question(self):
        time.sleep(1)  # Espera a que la página cargue completamente
        self.wait.until(
            EC.element_to_be_clickable((By.ID, "btn-new-question"))
        ).click()
        self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(@class, 'dropdown-item') and normalize-space(text())='Essay question']")
            )
        ).click()
        self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//span[@id='btn-save-new']/ancestor::button"))
        )

    def fill_form(self, fields):
        time.sleep(0.5)  # Breve espera para que el formulario esté listo

        # Campo "question"
        if "question" in fields:
            by, value = self.form_fields["question"]
            el = self.wait.until(EC.presence_of_element_located((by, value)))
            self.driver.execute_script("arguments[0].scrollIntoView();", el)
            el.clear()
            el.send_keys(fields["question"])

        # Campo "description"
        if "description" in fields:
            by, value = self.form_fields["description"]
            iframe = self.wait.until(EC.presence_of_element_located((by, value)))
            self.driver.switch_to.frame(iframe)
            body = self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            # Limpiar el body correctamente para TinyMCE
            self.driver.execute_script("arguments[0].innerHTML = '';", body)
            body.send_keys(fields["description"])
            self.driver.switch_to.default_content()

    def submit(self):
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[@id='btn-save-new']/ancestor::button"))
        ).click()

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
        self.select_new_question()
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
        print(f"******************** RUN TEST-FN16 IN ********************")
        for case in self.cases:
            self.run_case(case)
        print(f"******************** **************** ********************")
        print("")

if __name__ == "__main__":
    checker = SeleniumConnection()
    driver, url = checker.connect_and_check_login()
    TestFn16(driver, url).run()