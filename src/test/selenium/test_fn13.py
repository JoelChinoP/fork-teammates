from check_connection import SeleniumConnection
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time, json
from utils import Utils

class TestFn13:
    def __init__(self, driver, url):
        self.driver, self.url, self.path = driver, url, "/web/instructor/courses"
        self.locators = {
            "course_id": (By.ID, "course-id"),
            "course_name": (By.ID, "course-name"),
            "institute": (By.ID, "course-institute"),
            "timezone": (By.ID, "time-zone"),
            "add_course_btn": (By.ID, "btn-add-course"),
            "submit_btn": (By.ID, "btn-submit-course")
        }
        with open("data/fn13.json") as f:
            self.cases = json.load(f)

    def go_to_form(self):
        self.driver.get(self.url + self.path)
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.locators["add_course_btn"])
            ).click()

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.locators["course_id"])
            )
        except TimeoutException:
            print("No se pudo cargar el formulario de cursos")

    def fill_form(self, fields):
        for key, value in fields.items():
            if key in self.locators:
                el = self.driver.find_element(*self.locators[key])
                el.clear()
                el.send_keys(value)

    def submit(self):
        self.driver.find_element(*self.locators["submit_btn"]).click()

    def get_message(self, locator):
        try:
            el = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located((By.XPATH, locator))
            )
            return el.text.strip()
        except (TimeoutException, NoSuchElementException):
            return ""

    def run_case(self, case):
        self.go_to_form()
        self.fill_form(case["fields"])
        self.submit()
        time.sleep(1.5)

        obtained = self.get_message(case["element_locator"])
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
        print("******************** RUN TEST-FN13 IN ********************")
        for case in self.cases:
            self.run_case(case)
        print("******************** **************** ********************\n")

if __name__ == "__main__":
    checker = SeleniumConnection()
    driver, url = checker.connect_and_check_login()
    TestFn13(driver, url).run()