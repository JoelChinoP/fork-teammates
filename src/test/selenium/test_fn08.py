from check_connection import SeleniumConnection
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time, json
from utils import Utils

class TestFn08:
    def __init__(self, driver, url):
        self.driver, self.url, self.path = driver, url, "/web/admin/notifications"
        self.form_fields = {
            "group": (By.ID, "notification-target-user"),
            "style": (By.ID, "notification-style"),
            "title": (By.ID, "notification-title"),
            "start_time": (By.ID, "notification-start-time"),
            "end_time": (By.ID, "notification-end-time"),
            # Los pickers de fecha son componentes Angular, no inputs HTML nativos
        }
        with open("data/fn08.json") as f:
            self.cases = json.load(f)

    def go_to_form(self):
        self.driver.get(self.url)

        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "notifications-table"))
            )
        except TimeoutException:
            print("No se cargó la tabla de notificaciones")
            return

        try:
            first_edit_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Edit')]"))
            )
            first_edit_btn.click()

            # Esperar el campo title (para asegurar que se abrió bien el formulario)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "notification-title"))
            )

        except Exception as e:
            print(f"Error al hacer clic en Edit: {e}")

    def fill_form(self, fields):
        for key, value in fields.items():
            if key in self.form_fields:
                el = self.driver.find_element(*self.form_fields[key])
                el.clear()
                el.send_keys(value)

        # Rich Text Editor (TinyMCE)
        if "message" in fields:
            self.driver.execute_script(
                f"tinymce.get('notification-message').setContent(`{fields['message']}`);"
            )

        # Fechas (componentes Angular: tm-datepicker)
        if "start_date" in fields:
            self.driver.execute_script(f"""
                document.querySelector('#notification-start-date input')?.value = '{fields["start_date"]}';
                document.querySelector('#notification-start-date input')?.dispatchEvent(new Event('input', {{ bubbles: true }}));
            """)
        if "end_date" in fields:
            self.driver.execute_script(f"""
                document.querySelector('#notification-end-date input')?.value = '{fields["end_date"]}';
                document.querySelector('#notification-end-date input')?.dispatchEvent(new Event('input', {{ bubbles: true }}));
            """)

    def submit(self):
        self.driver.find_element(By.ID, "btn-edit-notification").click()

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
        time.sleep(1.5)

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
        print(f"******************** RUN TEST-FN08 IN ********************")
        for case in self.cases:
            self.run_case(case)
        print(f"******************** **************** ********************")
        print("")

if __name__ == "__main__":
    checker = SeleniumConnection()
    driver, url = checker.connect_and_check_login()
    TestFn08(driver, url).run()
