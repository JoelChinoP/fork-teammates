from check_connection import SeleniumConnection
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time, json
from utils import Utils

class TestFn20:
    def __init__(self, driver, url):
        self.driver, self.url, self.path = driver, url, "/web/student/home"
        self.form_fields = {
            "answer": (By.XPATH, "//iframe[contains(@id, 'tiny-angular') and not(@disabled)]"),
        }
        with open("data/fn20.json") as f:
            self.cases = json.load(f)

    def go_to_form(self):
        self.driver.get(self.url + self.path)
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'start-submit-btn-5'))
            ).click()
        except TimeoutException:
            pass
        print("Start button found.")
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//button[@type='submit']"))
        )
        print("reconocio boton submit")

    def fill_form(self, fields):
        for key, value in fields.items():
            if key in self.form_fields:
                try:
                    # Esperar a que el iframe esté presente
                    WebDriverWait(self.driver, 15).until(
                        EC.presence_of_element_located((By.XPATH, "//iframe[contains(@id, 'tiny-angular')]"))
                    )
                    # Cambiar el contexto al iframe
                    iframe = self.driver.find_element(By.XPATH, "//iframe[contains(@id, 'tiny-angular')]")
                    self.driver.switch_to.frame(iframe)

                    el = self.driver.find_element(*self.form_fields[key])
                    el.clear()
                    el.send_keys(value)
                except NoSuchElementException:
                    print(f"Elemento no encontrado para la clave: {key}")
                    continue
                finally:
                    # Volver al contexto principal después de interactuar con el iframe
                    self.driver.switch_to.default_content()

    def submit(self): 
        self.driver.find_element(By.ID, "btn-submit-qn-1").click()

    def check_modal(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//div[@role='document' and @class='modal-dialog']"))
            )
            return True
        except Exception:
            return False

    def run_case(self, case):
        self.go_to_form()
        self.fill_form(case["fields"])
        # Utils.solve_recaptcha(self.driver)
        self.submit()
        # Mejor usar un wait para la modal, si es posible
        time.sleep(1.5)
        modal_visible = self.check_modal()
        if case["Obs"] == "f+":
            if modal_visible:
                print(f"Test {case['id']} passed: Modal displayed successfully.")
            else:
                print(f"Test {case['id']} failed: Modal not displayed.")
        else:
            if not modal_visible:
                print(f"Test {case['id']} passed: No modal displayed as expected.")
            else:
                print(f"Test {case['id']} failed: Modal displayed unexpectedly.")
        Utils.log_test(
            case["id"],
            case["fields"],
            case["expected"],
            "Modal displayed" if modal_visible else "No modal displayed",
            case["Obs"]
        )

    def run(self):
        print("******************** RUN TEST-FN20 IN ********************")
        for case in self.cases:
            self.run_case(case)
        print("******************** **************** ********************")
        print("")

if __name__ == "__main__":
    checker = SeleniumConnection()
    driver, url = checker.connect_and_check_login()
    TestFn20(driver, url).run()