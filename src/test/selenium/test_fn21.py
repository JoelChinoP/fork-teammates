from check_connection import SeleniumConnection
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time, json
from utils import Utils

class TestFn21:
    def __init__(self, driver, url):
        self.driver = driver
        self.url = url
        courseid = "PS-Cigarra-2025"
        fsname = "selenium-test"
        self.path = f"/web/student/sessions/submission?courseid={courseid}&fsname={fsname}"
        # Selector robusto para el iframe del editor de texto
        self.form_fields = {
            "text_area": (By.XPATH, "//iframe[contains(@id, 'tiny-angular') and contains(@id, '_ifr')]"),
        }
        with open("data/fn21.json") as f:
            self.cases = json.load(f)

    def go_to_form(self):
        url = self.url + self.path
        print(f"Navigating to {url}")
        self.driver.get(url)
        # Espera a que cargue el botón de submit para la pregunta 1
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.ID, "btn-submit-qn-1"))
        )

    def fill_textarea(self, text):
        iframe = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.form_fields["text_area"])
        )
        self.driver.switch_to.frame(iframe)
        editable_body = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "tinymce"))
        )
        editable_body.clear()
        editable_body.send_keys(text)
        self.driver.switch_to.default_content()

    def submit(self):
        self.driver.find_element(By.ID, "btn-submit-qn-1").click()

    def get_modal_message(self):
        # Espera el modal de éxito y retorna el texto del mensaje
        modal_title = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".modal-title"))
        )
        message = modal_title.text.strip()
        # Cierra el modal presionando "Don't download proof of submission"
        btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),\"Don't download proof of submission\")]"))
        )
        btn.click()
        return message

    def run_case(self, case):
        self.go_to_form()
        self.fill_textarea(case["fields"]["text"])
        self.submit()
        obtained = self.get_modal_message()
        Utils.log_test(
            case["id"],
            case["fields"],
            case["expected"],
            obtained,
            case["Obs"]
        )
        return {
            "id": case["id"],
            "expected": case["expected"],
            "obtained": obtained
        }

    def run(self):
        print(f"******************** RUN TEST-FN21 IN ********************")
        for case in self.cases:
            self.run_case(case)
        print(f"******************** **************** ********************")
        print("")

if __name__ == "__main__":
    checker = SeleniumConnection()
    driver, url = checker.connect_and_check_login()
    TestFn21(driver, url).run()