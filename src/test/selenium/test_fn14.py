from check_connection import SeleniumConnection
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time, json
from utils import Utils

class TestFn14:
    def __init__(self, driver, url):
        self.driver, self.url, self.path = driver, url, "/web/instructor/sessions"
        self.form_fields = {
            "course": (By.ID, "add-course-id"),
            "session_name": (By.ID, "add-session-name"),
            "instructions_iframe": (By.CSS_SELECTOR, "iframe.tox-edit-area__iframe"),
            "start_date": (By.CSS_SELECTOR, "input[ngbdatepicker]:not([disabled])"),
            "start_time": (By.CSS_SELECTOR, "tm-timepicker#submission-start-time select"),
            "end_date": (By.CSS_SELECTOR, "input[ngbdatepicker]:not([disabled])"),
            "end_time": (By.CSS_SELECTOR, "tm-timepicker#submission-end-time select"),
            "grace_period": (By.ID, "grace-period")
        }
        with open("data/fn14.json") as f:
            self.cases = json.load(f)

    def go_to_form(self):
        self.driver.get(self.url + self.path)
        time.sleep(4)

        try:
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.ID, "btn-add-session"))
            )
            button = self.driver.find_element(By.ID, "btn-add-session")
            
            if button.is_displayed() and button.is_enabled():
                try:
                    button.click()
                except:
                    self.driver.execute_script("arguments[0].click();", button)
        except TimeoutException:
            print("[ERROR] No se encontró el botón 'Add Feedback Session'.")
            raise

        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.ID, "btn-create-session"))
        )

    def fill_form(self, fields):
        # Seleccionar curso
        Select(self.driver.find_element(*self.form_fields["course"])).select_by_visible_text(fields["course"])

        # Nombre de la sesión
        self.driver.find_element(*self.form_fields["session_name"]).clear()
        self.driver.find_element(*self.form_fields["session_name"]).send_keys(fields["session_name"])

        # Instrucciones (TinyMCE iframe)
        try:
            WebDriverWait(self.driver, 15).until(
                EC.frame_to_be_available_and_switch_to_it(self.form_fields["instructions_iframe"])
            )

            self.driver.find_element(By.TAG_NAME, "body").clear()
            self.driver.find_element(By.TAG_NAME, "body").send_keys(fields["instructions"])
            self.driver.switch_to.default_content()
        except TimeoutException:
            print("[WARNING] El iframe de instrucciones no fue encontrado. Se omitirá este campo.")

        # Fecha de inicio
        self.driver.execute_script(
            "arguments[0].value = arguments[1]",
            self.driver.find_element(*self.form_fields["start_date"]),
            fields["start_date"]
        )

        # Hora de inicio
        Select(self.driver.find_element(*self.form_fields["start_time"])).select_by_visible_text(fields["start_time"])

        # Fecha de fin
        self.driver.execute_script(
            "arguments[0].value = arguments[1]",
            self.driver.find_element(*self.form_fields["end_date"]),
            fields["end_date"]
        )

        # Hora de fin
        Select(self.driver.find_element(*self.form_fields["end_time"])).select_by_visible_text(fields["end_time"])

        # Período de gracia
        Select(self.driver.find_element(*self.form_fields["grace_period"])).select_by_visible_text(fields["grace_period"])


    def submit(self):
        self.driver.find_element(By.ID, "btn-create-session").click()

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
       
        self.submit()
        time.sleep(2)
        obtained_msg = self.get_message(case["element_locator"])
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
        print(f"******************** RUN TEST-FN14 ********************")
        for case in self.cases:
            self.run_case(case)
        print(f"*********************************************************\n")

if __name__ == "__main__":
    checker = SeleniumConnection()
    driver, url = checker.connect_and_check_login()
    TestFn14(driver, url).run()
