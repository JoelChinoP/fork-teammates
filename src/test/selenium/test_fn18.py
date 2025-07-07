from check_connection import SeleniumConnection
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time, json, sys
from utils import Utils

class TestFn18:
    def __init__(self, driver, url):
        self.driver, self.url = driver, url
        self.path = "/web/instructor/courses/student/edit"
        self.form_fields = {
            "student-name": (By.ID, "student-name"),
            "section-name": (By.ID, "section-name"),
            "team-name": (By.ID, "team-name"),
            "new-student-email": (By.ID, "new-student-email"),
            "comments": (By.ID, "comments"),
        }
        self.submit_button = (By.ID, "btn-submit")

        with open("data/fn18.json") as f:
            self.cases = json.load(f)

    def go_to_form(self):
        course_id_test = "CS123"
        student_email_test = "jean@example.com"

        self.driver.get(f"{self.url}{self.path}?courseid={course_id_test}&studentemail={student_email_test}")

        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.form_fields["student-name"])
            )
            for case in self.cases:
                if case["id"] == "FN18-CP-012":
                    try:
                        original_name = self.driver.find_element(*self.form_fields["student-name"]).get_attribute("value")
                        original_section = self.driver.find_element(*self.form_fields["section-name"]).get_attribute("value")
                        original_team = self.driver.find_element(*self.form_fields["team-name"]).get_attribute("value")
                        original_email = self.driver.find_element(*self.form_fields["new-student-email"]).get_attribute("value")
                        original_comments = self.driver.find_element(*self.form_fields["comments"]).get_attribute("value")

                        case["fields"]["student-name"] = original_name
                        case["fields"]["section-name"] = original_section
                        case["fields"]["team-name"] = original_team
                        case["fields"]["new-student-email"] = original_email
                        case["fields"]["comments"] = original_comments
                    except NoSuchElementException:
                        print("Advertencia: No se encontraron todos los campos originales para FN18-CP-012.")
                    break

        except TimeoutException:
            print("No se cargó la página de edición de estudiante.")
            self.driver.quit()
            sys.exit(1)
        except Exception as e:
            print(f"Error al intentar acceder al formulario de edición: {e}")
            self.driver.quit()
            sys.exit(1)

    def fill_form(self, fields):
        for key, value in fields.items():
            if key in self.form_fields:
                try:
                    el = self.driver.find_element(*self.form_fields[key])
                    el.clear()
                    el.send_keys(value)
                except NoSuchElementException:
                    print(f"Campo '{key}' no encontrado.")
                except Exception as e:
                    print(f"Error al llenar el campo '{key}': {e}")

    def submit_form(self):
        try:
            btn = self.driver.find_element(*self.submit_button)
            if btn.is_enabled():
                btn.click()
        except NoSuchElementException:
            print("Botón de submit no encontrado.")
        except Exception as e:
            print(f"No se pudo hacer clic en el botón de guardar: {e}")

    def get_message_or_check_button(self, case):
        time.sleep(1)

        if case["validation_type"] == "alert":
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.TAG_NAME, "tm-toast"))
                )

                alert_locator = (By.XPATH, case["element_locator"])
                el = WebDriverWait(self.driver, 15).until(
                    EC.visibility_of_element_located(alert_locator)
                )
                WebDriverWait(self.driver, 5).until(
                    EC.text_to_be_present_in_element(alert_locator, case["expected"])
                )
                return el.text.strip()
            except TimeoutException:
                try:
                    any_toast = self.driver.find_element(By.XPATH, "//div[@class='toast-body']")
                    return any_toast.text.strip()
                except NoSuchElementException:
                    return ""
            except NoSuchElementException:
                return ""
            except Exception as e:
                return f"Error al buscar alerta: {e}"

        elif case["validation_type"] == "button_disabled":
            try:
                locator = (By.XPATH, case["element_locator"])
                WebDriverWait(self.driver, 3).until(
                    EC.presence_of_element_located(locator)
                )
                return "Botón deshabilitado"
            except TimeoutException:
                return "Botón habilitado cuando no debería"
            except Exception as e:
                return f"Error verificando el botón: {e}"

        return ""

    def run_case(self, case):
        self.go_to_form()
        self.fill_form(case["fields"])

        if case["validation_type"] != "button_disabled":
            self.submit_form()

        if "Student has been updated" in case["expected"]:
            try:
                WebDriverWait(self.driver, 15).until(
                    EC.url_contains("/web/instructor/courses/details?courseid=CS123")
                )
            except TimeoutException:
                print(f"Redirección fallida en caso {case['id']}.")

        self.driver.save_screenshot(f"screenshot_after_action_{case['id']}.png")
        obtained_msg = self.get_message_or_check_button(case)

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
        print("******************** RUN TEST-FN18 ********************")
        for case in self.cases:
            try:
                self.run_case(case)
            except Exception as e:
                print(f"Error inesperado en caso {case['id']}: {e}")
                self.driver.save_screenshot(f"screenshot_error_{case['id']}.png")
        print("******************** END TEST-FN18 ********************\n")

if __name__ == "__main__":
    checker = SeleniumConnection()
    driver, url = checker.connect_and_check_login()
    test_fn18 = TestFn18(driver, url)
    test_fn18.run()
    driver.quit()
