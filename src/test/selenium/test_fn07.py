from check_connection import SeleniumConnection
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time, json
from utils import Utils

class TestFn07:
    def __init__(self, driver, url):
        self.driver, self.url, self.path = driver, url, "/web/admin/notifications"
        self.form_fields = {
            "title": (By.ID, "notification-title"),
            "message": (By.ID, "notification-message"),
            "group": (By.ID, "notification-target-user"),
            "style": (By.ID, "notification-style"),
            "start_date": (By.XPATH, "//div[@id='notification-start-date']//input"),
            "start_time": (By.XPATH, "//tm-timepicker[@id='notification-start-time']//select"),
            "end_date": (By.XPATH, "//div[@id='notification-end-date']//input"),
            "end_time": (By.XPATH, "//tm-timepicker[@id='notification-end-time']//select"),
        }
        with open("data/fn07.json") as f:
            self.cases = json.load(f)

    def go_to_form(self):
        self.driver.get(self.url + self.path)
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'btn-add-notification'))
            ).click()
        except TimeoutException:
            pass
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'btn-create-notification'))
        )

    def fill_form(self, fields):
        for key, value in fields.items():
            if key in ["title", "group", "style"]:
                el = self.driver.find_element(*self.form_fields[key])
                if el.tag_name == "select":
                    for option in el.find_elements(By.TAG_NAME, 'option'):
                        if value.lower() in option.text.lower():
                            option.click()
                            break
                else:
                    el.clear()
                    el.send_keys(value)
            elif key == "message":
                # Rich text editor handling (TinyMCE)
                iframe = self.driver.find_element(By.CSS_SELECTOR, "iframe.tox-edit-area__iframe")
                self.driver.switch_to.frame(iframe)
                body = self.driver.find_element(By.CSS_SELECTOR, "body")
                body.clear()
                body.send_keys(value)
                self.driver.switch_to.default_content()
            elif key in ["start_date", "end_date"]:
                el = self.driver.find_element(*self.form_fields[key])
                el.clear()
                el.send_keys(value)
            elif key in ["start_time", "end_time"]:
                select = self.driver.find_element(*self.form_fields[key])
                for option in select.find_elements(By.TAG_NAME, 'option'):
                    if value in option.text:
                        option.click()
                        break

    def submit(self):
        self.driver.find_element(By.ID, "btn-create-notification").click()

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
        print(f"******************** RUN TEST-FN07 IN ********************")
        for case in self.cases:
            self.run_case(case)
        print(f"******************** **************** ********************")
        print("")

if __name__ == "__main__":
    checker = SeleniumConnection()
    driver, url = checker.connect_and_check_login()
    TestFn07(driver, url).run()