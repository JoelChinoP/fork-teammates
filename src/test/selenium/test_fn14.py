from check_connection import SeleniumConnection
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
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
            "instructions": (By.CLASS_NAME, "tox-edit-area__iframe"),  # Edita esto si tienes el ID exacto
            "start_date": (By.XPATH, "(//input[@ngbdatepicker])[1]"),
            "start_time": (By.XPATH, "(//select[@class='form-control form-select'])[1]"),
            "end_date": (By.XPATH, "(//input[@ngbdatepicker])[2]"),
            "end_time": (By.XPATH, "(//select[@class='form-control form-select'])[2]"),
            "grace_period": (By.ID, "grace-period")
        }
        with open("data/fn14.json") as f:
            self.cases = json.load(f)

    def go_to_form(self):
        self.driver.get(self.url)
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "btn-create-session"))
        )

    def fill_form(self, fields):
        # Select course
        Select(self.driver.find_element(*self.form_fields["course"])).select_by_visible_text(fields["course"])
        # Session name
        self.driver.find_element(*self.form_fields["session_name"]).clear()
        self.driver.find_element(*self.form_fields["session_name"]).send_keys(fields["session_name"])
        # Instructions (dentro del iframe de TinyMCE)
        self.driver.switch_to.frame(self.driver.find_element(*self.form_fields["instructions"]))
        self.driver.find_element(By.TAG_NAME, "body").clear()
        self.driver.find_element(By.TAG_NAME, "body").send_keys(fields["instructions"])
        self.driver.switch_to.default_content()
        # Set start date (readonly, vía JS)
        self.driver.execute_script("arguments[0].value = arguments[1]", self.driver.find_element(*self.form_fields["start_date"]), fields["start_date"])
        # Start time
        Select(self.driver.find_element(*self.form_fields["start_time"])).select_by_visible_text(fields["start_time"])
        # End date
        self.driver.execute_script("arguments[0].value = arguments[1]", self.driver.find_element(*self.form_fields["end_date"]), fields["end_date"])
        # End time
        Select(self.driver.find_element(*self.form_fields["end_time"])).select_by_visible_text(fields["end_time"])
        # Grace period
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
        Utils.solve_recaptcha(self.driver)
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
        print(f"******************** ******************* ********************\n")

if __name__ == "__main__":
    checker = SeleniumConnection()
    driver, url = checker.connect_and_check_login()
    TestFn14(driver, url).run()

