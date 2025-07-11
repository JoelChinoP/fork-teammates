from check_connection import SeleniumConnection
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time, json
from utils import Utils


class TestFn18:
    def __init__(self, driver, url, course_id, student_email):
        self.driver, self.url = driver, url
        self.course_id = course_id
        self.student_email = student_email
        self.form_path = "/web/instructor/courses/student/edit"

        self.locators = {
            "student-name": (By.ID, "student-name"),
            "section-name": (By.ID, "section-name"),
            "team-name": (By.ID, "team-name"),
            "new-student-email": (By.ID, "new-student-email"),
            "comments": (By.ID, "comments"),
            "submit": (By.ID, "btn-submit")
        }

        with open("data/fn18.json") as f:
            self.cases = json.load(f)

    def go_to_form(self):
        full_url = (
            f"{self.url}{self.form_path}"
            f"?courseid={self.course_id}&studentemail={self.student_email}"
        )
        print("Navegando a:", full_url)
        self.driver.get(full_url)

        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.locators["student-name"])
            )
        except TimeoutException:
            print("❌ No se cargó el formulario de edición de estudiante")
            print("📄 Título de página:", self.driver.title)
            print("📄 Contenido parcial:", self.driver.page_source[:500])

    def fill_field(self, locator, value):
        try:
            el = self.driver.find_element(*self.locators[locator])
            el.clear()
            if value.strip():
                el.send_keys(value)
        except Exception as e:
            print(f"⚠️ Error llenando campo {locator}: {e}")

    def fill_form(self, data):
        for field in self.locators:
            if field != "submit":
                self.fill_field(field, data.get(field, ""))

    def click_submit(self):
        try:
            btn = self.driver.find_element(*self.locators["submit"])
            if btn.is_enabled():
                btn.click()
        except Exception as e:
            print(f"⚠️ No se pudo hacer clic en 'Save Changes': {e}")

    def get_message(self, case):
        locator = case.get("element_locator")
        try:
            el = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, locator))
            )
            return el.text.strip()
        except (TimeoutException, NoSuchElementException):
            return "Elemento no encontrado"

    def run_case(self, case):
        self.go_to_form()
        self.fill_form(case["input"])
        time.sleep(1.2)

        if case.get("check_button_disabled"):
            try:
                btn = self.driver.find_element(By.ID, "btn-submit")
                disabled = not btn.is_enabled()
                obtained = "Botón deshabilitado" if disabled else "Botón habilitado"
            except Exception as e:
                obtained = f"Error al verificar botón: {e}"
        else:
            self.click_submit()
            time.sleep(1.5)
            obtained = self.get_message(case)

        Utils.log_test(
            case["id"],
            case["input"],
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
        print("********** RUNNING TEST-FN18 **********")
        for case in self.cases:
            self.run_case(case)
        print("********** END TEST-FN18 **********\n")


if __name__ == "__main__":
    checker = SeleniumConnection()
    driver, url = checker.connect_and_check_login()

    course_id = "CS123"
    student_email = "jean@example.com"

    TestFn18(driver, url, course_id, student_email).run()
