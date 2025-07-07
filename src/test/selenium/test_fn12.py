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
        self.locators = {
            "input": (By.ID, "search-keyword"),
            "btn": (By.ID, "btn-search"),
            "toast": (By.CLASS_NAME, "toast-body"),
            "result_partial": (By.XPATH, "//table//span[contains(@class, 'highlighted-text')]"),
            "result_exact": (By.XPATH, "//table//td[normalize-space(text())='Alice Betsy']")
        }
        with open("data/fn12.json") as f:
            self.cases = json.load(f)

    def go_to_form(self):
        self.driver.get(self.url + self.path)
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.locators["input"])
            )
        except TimeoutException:
            print("No se cargó el campo de búsqueda")

    def fill_input(self, text):
        try:
            el = self.driver.find_element(*self.locators["input"])
            el.clear()
            el.send_keys(text)
        except Exception as e:
            print(f"Error al llenar el input: {e}")

    def click_search(self):
        try:
            btn = self.driver.find_element(*self.locators["btn"])
            if btn.is_enabled():
                btn.click()
        except Exception as e:
            print(f"No se pudo hacer clic en Buscar: {e}")

    def get_message(self, case):
        expected = case["expected"]
        try:
            # Validación del estado del botón
            if "Botón" in expected:
                btn = self.driver.find_element(*self.locators["btn"])
                return "Botón habilitado" if btn.is_enabled() else "Botón deshabilitado"

            # Validación de truncamiento del input
            if "Input truncado" in expected:
                el = self.driver.find_element(*self.locators["input"])
                return "Input truncado o bloqueado" if len(el.get_attribute("value")) <= 100 else "Input excede longitud"

            # Validación de resultados visibles en tabla
            if "Resultado parcial" in expected:
                el = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located(self.locators["result_partial"])
                )
                return "Resultado parcial visible"

            if "Resultado exacto" in expected:
                el = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located(self.locators["result_exact"])
                )
                return "Resultado exacto visible"

            # Validación del mensaje tipo toast
            if "No results found" in expected:
                toast = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located(self.locators["toast"])
                )
                return toast.text.strip()
            if "Resultado exacto" in expected:
                names = case["input"].replace('"', '').split()
                xpath = "//table//td" + ''.join(
                    [f"[.//span[@class='highlighted-text' and text()='{n}']]" for n in names]
                )
                el = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, xpath))
                )
                return "Resultado exacto visible"

            # Fallback: usar locator definido por el caso
            el = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, case["element_locator"]))
            )
            return el.text.strip()

        except (TimeoutException, NoSuchElementException):
            return "Elemento no encontrado"

    def run_case(self, case):
        self.go_to_form()
        self.fill_input(case["input"])
        time.sleep(1)  # permitir que se active el botón
        self.click_search()
        time.sleep(1.5)  # esperar los resultados

        obtained = self.get_message(case)

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
        print("******************** RUN TEST-FN12 IN ********************")
        for case in self.cases:
            self.run_case(case)
        print("******************** **************** ********************\n")

if __name__ == "__main__":
    checker = SeleniumConnection()
    driver, url = checker.connect_and_check_login()
    TestFn12(driver, url).run()
