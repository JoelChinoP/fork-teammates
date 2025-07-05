from check_connection import SeleniumConnection
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time, json
from utils import Utils

class TestFn11:
    def __init__(self, driver, url):
        self.driver, self.url, self.path = driver, url, "/web/admin/stats"
        with open("data/fn11.json") as f:
            self.cases = json.load(f)

        self.inputs = {
            "from": (By.ID, "search-from-datepicker"),
            "to": (By.ID, "search-to-datepicker"),
        }

        self.btn_query = (By.ID, "query-button")

    def go_to_stats(self):
        self.driver.get(self.url + self.path)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "search-from-datepicker"))
        )

    def fill_dates(self, from_date, to_date):
        from_field = self.driver.find_element(*self.inputs["from"])
        to_field = self.driver.find_element(*self.inputs["to"])
        from_field.clear()
        to_field.clear()
        from_field.send_keys(from_date)
        to_field.send_keys(to_date)

    def click_query(self):
        button = self.driver.find_element(*self.btn_query)
        self.driver.execute_script("arguments[0].click();", button)

    def get_message(self, locator):
        try:
            # Primero intenta capturar un mensaje de error 
            el = WebDriverWait(self.driver, 4).until(
                EC.visibility_of_element_located((By.XPATH, locator))
            )
            text = el.text.strip()
            if text:
                return text
        except (TimeoutException, NoSuchElementException):
            pass

        # Si no hay mensaje de error, es porque se genero correctamente el grafico
        return "Success: busqueda realizada"

    def run_case(self, case):
        self.go_to_stats()
        self.fill_dates(case["from"], case["to"])
        self.click_query()
        time.sleep(3)

        result = self.get_message(case["element_locator"])

        Utils.log_test(
            case["id"],
            {"from": case["from"], "to": case["to"]},
            case["expected"],
            result,
            case.get("Obs", "")
        )

        return {
            "id": case["id"],
            "expected": case["expected"],
            "obtained": result
        }

    def run(self):
        print("******************** RUN TEST-FN11 IN ********************")
        for case in self.cases:
            self.run_case(case)
        print("******************** ******************* ******************\n")

if __name__ == "__main__":
    checker = SeleniumConnection()
    driver, url = checker.connect_and_check_login()
    TestFn11(driver, url).run()
