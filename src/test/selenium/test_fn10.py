from check_connection import SeleniumConnection
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time, json
from utils import Utils

class TestFn10:
    def __init__(self, driver, url):
        self.driver, self.url, self.path = driver, url, "/web/admin/logs"
        with open("data/fn10.json") as f:
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
            
        }

        self.btn_query = (By.ID, "query-button")
        self.btn_clear = (By.XPATH, "//button[contains(text(), 'Clear all')]")

    def go_to_logs(self):
        self.driver.get(self.url + self.path)

        # Espera que el boton de "Advanced filters" sea clickeable
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Advanced filters')]"))
        ).click()

        # Espera a que aparezca el input trace-id despues del click
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "trace-id"))
        )


    def fill_fields(self, fields):
        for key, value in fields.items():
            if key in self.inputs:
                locator = self.inputs[key]
                WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(locator))
                element = self.driver.find_element(*locator)
                tag = element.tag_name.lower()
                if tag == "select":
                    Select(element).select_by_visible_text(value)
                else:
                    element.clear()
                    element.send_keys(value)

    def click_query(self):
        button = self.driver.find_element(*self.btn_query)
        # Click a nivel de DOM
        self.driver.execute_script("arguments[0].click();", button)

    def click_clear(self):
        button = self.driver.find_element(*self.btn_clear)
        # Click a nivel de DOM
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
        
        # Ejecutar precondicion si existe
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
        print("******************** RUN TEST-FN10 IN ********************")
        for case in self.cases:
            self.run_case(case)
        print("******************** ******************* ******************\n")

if __name__ == "__main__":
    checker = SeleniumConnection()
    driver, url = checker.connect_and_check_login()
    TestFn10(driver, url).run()
