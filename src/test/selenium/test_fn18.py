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
            else:
                print("El botón de guardar está deshabilitado.")
        except NoSuchElementException:
            print("Botón de submit no encontrado.")
        except Exception as e:
            print(f"No se pudo hacer clic en el botón de guardar: {e}")

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
        self.submit_form()
        time.sleep(2)

        obtained_msg = self.get_message(case["element_locator"])

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
        print(f"******************** RUN TEST-FN18 IN ********************")
        for case in self.cases:
            self.run_case(case)
        print(f"******************** **************** ********************")
        print("")

if __name__ == "__main__":
    checker = SeleniumConnection()
    driver, url = checker.connect_and_check_login()
    test_fn18 = TestFn18(driver, url)
    test_fn18.run()
    driver.quit()