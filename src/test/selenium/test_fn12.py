from check_connection import SeleniumConnection
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time, json
from utils import Utils

class TestFn12:
    def __init__(self, driver, url):
        self.driver, self.url, self.path = driver, url, "/web/instructor/search"
        self.input_locator = (By.ID, "search-keyword")
        self.search_btn = (By.ID, "btn-search")

        with open("data/fn12.json") as f:
            self.cases = json.load(f)

    def go_to_form(self):
        self.driver.get(self.url + self.path)
        try:
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(self.input_locator)
            )
        except TimeoutException:
            print("No se cargó el campo de búsqueda")

    def fill_input(self, text):
        el = self.driver.find_element(*self.input_locator)
        el.clear()
        el.send_keys(text)

    def click_search(self):
        try:
            btn = self.driver.find_element(*self.search_btn)
            if btn.is_enabled():
                btn.click()
        except Exception as e:
            print(f"No se pudo hacer clic en Buscar: {e}")

    def get_message(self, locator):
        try:
            el = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, locator))
            )
            return el.text.strip()
        except:
            return ""

    def run_case(self, case):
        self.go_to_form()
        self.fill_input(case["input"])
        time.sleep(1)  # para permitir actualizaciones dinámicas
        self.click_search()
        time.sleep(1.5)

        obtained = self.get_message(case["element_locator"])
        Utils.log_test(
            case["id"],
            {"input": case["input"]},
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
        print(f"******************** RUN TEST-FN12 IN ********************")
        for case in self.cases:
            self.run_case(case)
        print(f"******************** **************** ********************")
        print("")

if __name__ == "__main__":
    checker = SeleniumConnection()
    driver, url = checker.connect_and_check_login()
    TestFn12(driver, url).run()
