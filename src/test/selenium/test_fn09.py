from check_connection import SeleniumConnection
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time, json
from utils import Utils

class TestFn09:
    def __init__(self, driver, url):
        self.driver, self.url, self.path = driver, url, "/web/admin/logs"
        with open("data/fn09.json") as f:
            self.cases = json.load(f)

        self.inputs = {
            "trace-id": (By.ID, "trace-id"),
            "google-id": (By.ID, "google-id"),
            "source-file": (By.ID, "source-file"),
            "regkey": (By.ID, "regkey"),
            "source-function": (By.ID, "source-function"),
            "email": (By.ID, "email"),
            "action-class": (By.ID, "action-class"),
            "exception-class": (By.ID, "exception-class"),
            "latency": (By.ID, "latency"),
            "status": (By.ID, "status"),
            "version": (By.ID, "version"),
            "extra-filters": (By.ID, "extra-filters"),

            # Nuevos campos añadidos
            "logs-from-datepicker": (By.ID, "logs-from-datepicker"),
            "logs-to-datepicker": (By.ID, "logs-to-datepicker"),
            "from-hour": (By.XPATH, "//input[@placeholder='HH'][1]"),
            "from-minute": (By.XPATH, "//input[@placeholder='MM'][1]"),
            "to-hour": (By.XPATH, "(//input[@placeholder='HH'])[2]"),
            "to-minute": (By.XPATH, "(//input[@placeholder='MM'])[2]"),

            "min-severity-radio": (By.ID, "min-severity"),
            "event-radio": (By.ID, "event"),
            "severity-radio": (By.ID, "severity"),

            "log-type": (By.XPATH, "//select[option[@value='REQUEST_LOG']]"),
            "severity-select": (By.XPATH, "//select[option[@value='INFO']]"),
        }

        self.btn_query = (By.ID, "query-button")
        self.btn_clear = (By.XPATH, "//button[contains(text(), 'Clear all')]")

    def go_to_logs(self):
        self.driver.get(self.url + self.path)

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Advanced filters')]"))
        ).click()

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "trace-id"))
        )

    def fill_fields(self, fields):
        for key, value in fields.items():
            if key in self.inputs:
                locator = self.inputs[key]
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(locator))
                element = self.driver.find_element(*locator)
                tag = element.tag_name.lower()

                if tag == "select":
                    Select(element).select_by_visible_text(value)
                elif tag == "input" and element.get_attribute("type") == "radio":
                    if not element.is_selected():
                        self.driver.execute_script("arguments[0].click();", element)
                else:
                    element.clear()
                    element.send_keys(value)

    def click_query(self):
        button = self.driver.find_element(*self.btn_query)
        self.driver.execute_script("arguments[0].click();", button)

    def click_clear(self):
        button = self.driver.find_element(*self.btn_clear)
        self.driver.execute_script("arguments[0].click();", button)

    def get_element_text(self, locator):
        try:
            el = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located((By.XPATH, locator))
            )
            return el.text.strip()
        except (TimeoutException, NoSuchElementException):
            return ""

    def run_case(self, case):
        self.go_to_logs()

        if "pre" in case:
            self.fill_fields(case["pre"].get("fields", {}))
            if case["pre"].get("action") == "query":
                self.click_query()
            elif case["pre"].get("action") == "clear":
                self.click_clear()
            time.sleep(1.2)

        if "fields" in case:
            self.fill_fields(case["fields"])

        if case.get("action") == "query":
            self.click_query()
        elif case.get("action") == "clear":
            self.click_clear()

        time.sleep(15)
        obtained = self.get_element_text(case["element_locator"])

        Utils.log_test(
            case["id"],
            case.get("fields", {}),
            case["expected"],
            obtained,
            case.get("Obs", "")
        )

        return {
            "id": case["id"],
            "expected": case["expected"],
            "obtained": obtained
        }

    def run(self):
        print("******************** RUN TEST-FN09 IN ********************")
        for case in self.cases:
            self.run_case(case)
        print("******************** ******************* ******************\n")

if __name__ == "__main__":
    checker = SeleniumConnection()
    driver, url = checker.connect_and_check_login()
    TestFn09(driver, url).run()
