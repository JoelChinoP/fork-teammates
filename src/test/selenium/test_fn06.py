from check_connection import SeleniumConnection
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time, json, sys
from utils import Utils

class TestFn06:
    def __init__(self, driver, url):
        self.driver = driver
        self.url = url
        self.path = "/web/admin/search"

        self.form_fields = {
            "search": (By.ID, "search-box"),
            "submit": (By.ID, "search-button")
        }

        with open("data/fn06.json", encoding="utf-8") as f:
            self.cases = json.load(f)

    def go_to_form(self):
        self.driver.get(self.url + "/web/admin/home")
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//a[@href="/web/admin/search"]'))
            )
        except TimeoutException:
            print(" No se pudo cargar el enlace de búsqueda.")
            self.driver.quit()
            sys.exit(1)

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.form_fields["submit"])
        )

    def fill_form(self, value):
        search_box = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(self.form_fields["search"])
        )

        self.driver.execute_script("arguments[0].value = '';", search_box)
        self.driver.execute_script("""
            const input = arguments[0];
            const value = arguments[1];
            input.value = value;
            input.dispatchEvent(new Event('input', { bubbles: true }));
            input.dispatchEvent(new Event('change', { bubbles: true }));
        """, search_box, value)

        time.sleep(1.5)

    def submit(self):
        self.driver.find_element(*self.form_fields["submit"]).click()

    def get_result(self):
        try:
            # Espera hasta que aparezca el toast
            toast = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, "tm-toast ngb-toast .toast-body")
                )
            )
            toast_text = toast.text.strip()
    
            if "No results found." in toast_text:
                return "No results found."
            elif "Instructors Found" in toast_text:
                return "Instructors Found"
            elif "The [searchkey] HTTP parameter is null." in toast_text:
                return "The [searchkey] HTTP parameter is null."
            else:
                return toast_text
        except TimeoutException:
            return "No encontrado"


    def print_result(self, status, code, input_data, expected, obtained, obs):
        print(f"[{status}] {code}")
        print(f"\tInput:")
        print(f"\t\tsearch: {input_data}")
        print(f"\tExpected:")
        print(f"\t\t{expected}")
        print(f"\tObtained:")
        print(f"\t\t{obtained}")
        print(f"\tObs:")
        print(f"\t\t{obs}\n")

    def run_case(self, case):
        code = case["id"]
        input_value = case["input"]
        expected = case["expected_result"]
        obs = case["observation"]

        try:
            self.go_to_form()
            self.fill_form(input_value)
            self.submit()

            obtained = self.get_result()
            success = obtained == expected
            status = "PASSED" if success == case["expect_found"] else "FAILED"

        except Exception as e:
            obtained = str(e).splitlines()[0]
            status = "FAILED"

        self.print_result(
            status=status,
            code=code,
            input_data=input_value,
            expected=expected,
            obtained=obtained,
            obs=obs
        )

        return status

    def run(self):
        print("\n***Conexión exitosa y usuario autenticado...\n")
        print("******************** RUNNING TEST-FN06 ********************")

        passed = failed = 0

        for case in self.cases:
            status = self.run_case(case)
            if status == "PASSED":
                passed += 1
            else:
                failed += 1

        print("******************** ******************* ******************\n")
        print("=============== RESUMEN ===============")
        print(f" {passed} PASSED")
        print(f" {failed} FAILED")
        print("=======================================\n")


if __name__ == "__main__":
    checker = SeleniumConnection(
        url="https://cigarra-teammates.appspot.com",
        token_name="AUTH-TOKEN",
        token_value="1B1B06046B395211D57F5828006C3610BE17EECB47F8DC12BCEE6A33A37E0DABD81916DAF5FAFCBED27C731B91BB86C9F437287D590E166029F36FFFF21C083F04C5DABCBEA439FDCF03E6855E9CE1C6F4811919562D69514C1BA9B054532985254A23676E229009AE497535A3675AE0E363B0905C7A874AC5454A81DC1D8F07"
    )
    driver, url = checker.connect_and_check_login()
    TestFn06(driver, url).run()
