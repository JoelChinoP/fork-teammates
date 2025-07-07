from check_connection import SeleniumConnection
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, InvalidElementStateException
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
            "submit_btn": (By.ID, "btn-submit-course"),
            "invalid_course_id": (By.XPATH, "//div[contains(text(),'The field Course ID should not be empty.')]"),
            "invalid_course_name": (By.XPATH, "//div[contains(text(),'The field Course Name should not be empty.')]"),
            "toast": (By.CLASS_NAME, "toast-body")
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
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.locators["add_course_btn"])
            ).click()
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.locators["course_id"])
            )
        except Exception as e:
            print("Error al intentar mostrar el formulario:", e)

        for key, value in fields.items():
            if key in ["course_id", "course_name"]:
                try:
                    el = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located(self.locators[key])
                    )
                    el.clear()
                    el.send_keys(value)
                except InvalidElementStateException:
                    print(f"No se pudo editar el campo {key}")
                except Exception:
                    print(f"Error inesperado al editar el campo {key}")
            elif key in ["institute", "timezone"]:
                try:
                    el = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable(self.locators[key])
                    )
                    matched = False
                    for option in el.find_elements(By.TAG_NAME, "option"):
                        if option.get_attribute("value") == value.strip():
                            option.click()
                            matched = True
                            break
                    if not matched and fields.get("strict_select", False):
                        print(f"Valor no encontrado para {key}: {value}")
                except Exception as e:
                    print(f"Error al seleccionar {key}: {e}")

    def submit(self):
        try:
            btn = self.driver.find_element(*self.locators["submit_btn"])
            if btn.get_attribute("disabled"):
                print("El botón está deshabilitado, no se puede enviar el formulario")
            else:
                WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable(self.locators["submit_btn"])
                ).click()
        except Exception:
            print("No se pudo hacer clic en el botón de submit")

    def get_message(self, locator):
        try:
            if locator.startswith("//"):
                el = WebDriverWait(self.driver, 5).until(
                    EC.visibility_of_element_located((By.XPATH, locator))
                )
            else:
                el = self.driver.find_element(*self.locators[locator])
            return el.get_attribute("value") if locator.startswith("input_") else el.text.strip()
        except (TimeoutException, NoSuchElementException):
            return ""

    def run_case(self, case):
        self.go_to_form()
        self.fill_form(case["fields"])
        self.submit()
        time.sleep(1.5)

        expected_locator = case["element_locator"]
        obtained = self.get_message(expected_locator)

        # Validación adicional para longitud
        if "assert_input_length" in case:
            field_key = expected_locator.replace("input_", "")
            try:
                input_element = self.driver.find_element(*self.locators[field_key])
                obtained_length = len(input_element.get_attribute("value"))
                expected_length = case["assert_input_length"]
                obtained = input_element.get_attribute("value")
                if obtained_length != expected_length:
                    print(f"Longitud esperada: {expected_length}, obtenida: {obtained_length}")
            except Exception as e:
                print(f"Error al verificar longitud del input: {e}")

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
