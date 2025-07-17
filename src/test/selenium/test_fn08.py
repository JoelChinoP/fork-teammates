from check_connection import SeleniumConnection
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, json, random, sys
from utils import Utils
import contextlib
import io

class TestFn08:
    def __init__(self, driver, url):
        self.driver = driver
        self.url = url
        self.path = "/web/admin/notifications"

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

        with open("data/fn08.json", encoding="utf-8") as f:
            self.cases = json.load(f)

    def go_to_edit_form(self, notification_id):
        self.driver.get(self.url + self.path)
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, notification_id))
            )
            row = self.driver.find_element(By.ID, notification_id)
            edit_button = row.find_element(By.XPATH, ".//button[contains(text(), 'Edit')]")
            edit_button.click()

            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "btn-edit-notification"))
            )

        except Exception as e:
            print(f"[ERROR] No se pudo acceder al formulario de edición: {e}")
            self.driver.quit()
            sys.exit(1)

    def fill_form(self, fields):
        for key, value in fields.items():
            if key in ["title", "group", "style"]:
                el = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located(self.form_fields[key])
                )
                if el.tag_name == "select":
                    for option in el.find_elements(By.TAG_NAME, 'option'):
                        if value.lower() in option.text.lower():
                            option.click()
                            break
                else:
                    if el.is_enabled():
                        self.driver.execute_script("arguments[0].value = '';", el)
                        el.send_keys(value)

            elif key == "message":
                iframe = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "iframe.tox-edit-area__iframe"))
                )
                self.driver.switch_to.frame(iframe)
                body = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
                )
                self.driver.execute_script("arguments[0].innerHTML = '';", body)
                body.send_keys(value)
                self.driver.switch_to.default_content()

            elif key in ["start_date", "end_date"]:
                el = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located(self.form_fields[key])
                )
                self.driver.execute_script("arguments[0].removeAttribute('readonly')", el)
                self.driver.execute_script("arguments[0].value = arguments[1];", el, value)

            elif key in ["start_time", "end_time"]:
                select = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located(self.form_fields[key])
                )
                for option in select.find_elements(By.TAG_NAME, 'option'):
                    if value in option.text:
                        option.click()
                        break

    def submit(self):
        self.driver.find_element(By.ID, "btn-edit-notification").click()

    def get_message(self, locator):
        try:
            if locator.startswith("//"):
                msg_element = WebDriverWait(self.driver, 7).until(
                    EC.visibility_of_element_located((By.XPATH, locator))
                )
            else:
                msg_element = WebDriverWait(self.driver, 7).until(
                    EC.visibility_of_element_located((By.ID, locator))
                )
            return msg_element.text.strip()
        except Exception as e:
            print(f"[ERROR] No se pudo obtener el mensaje con locator {locator}: {e}")
            return ""

    def run_case(self, case):
        print(f"Ejecutando caso: {case['id']}")
        try:
            self.go_to_edit_form(case["notification_id"])
            self.fill_form(case["fields"])
            time.sleep(random.uniform(2.5, 4.5))

            try:
                with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                    Utils.solve_recaptcha(self.driver)
            except Exception:
                pass

            self.submit()
            time.sleep(2)

            obtained_msg = self.get_message(case["element_locator"])
            status = "PASSED" if case["expected"] in obtained_msg else "FAILED"

            Utils.log_test(
                case["id"],
                case["fields"],
                case["expected"],
                obtained_msg,
                case["Obs"]
            )

            print(f"{'.' if status == 'PASSED' else '.'} {case['id']} - {status}")
            return status

        except Exception as e:
            print(f" {case['id']} - EXCEPTION: {str(e).splitlines()[0]}")
            return "FAILED"

    def run(self):
        print("\n******************** RUNNING TEST-FN08 ********************")
        passed = failed = 0

        for case in self.cases:
            status = self.run_case(case)
            if status == "PASSED":
                passed += 1
            else:
                failed += 1

        print("\n=============== RESUMEN ===============")
        print(f" {passed} PASSED")
        print(f" {failed} FAILED")
        print("=======================================\n")


if __name__ == "__main__":
    checker = SeleniumConnection()
    driver, url = checker.connect_and_check_login()
    TestFn08(driver, url).run()
