from check_connection import SeleniumConnection
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time, json
from utils import Utils

class TestFn03:
    def __init__(self, driver, url):
        self.driver, self.url, self.path = driver, url, "/web/admin/home"
        self.form_fields = {
            "input_line": (By.ID, "instructor-details-single-line"),
        }
        with open("data/fn03.json") as f:
            self.cases = json.load(f)

    def go_to_form(self):
        self.driver.get(self.url + self.path)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "add-instructor-single-line"))
        )

    def fill_form(self, fields):
        # Solo hay un textarea para la entrada de múltiples instructores
        el = self.driver.find_element(*self.form_fields["input_line"])
        el.clear()
        el.send_keys(fields.get("input_line", ""))

    def submit(self):
        self.driver.find_element(By.ID, "add-instructor-single-line").click()

    def get_pending_rows(self):
        # Busca las filas de la tabla de resultado de instructores agregados (Result)
        try:
            table = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'card-body')]//table"))
            )
            rows = table.find_elements(By.XPATH, ".//tbody/tr")
            results = []
            for row in rows:
                cols = row.find_elements(By.TAG_NAME, "td")
                # Si se detectan las columnas esperadas
                if len(cols) >= 6:
                    # Accede a los valores: Name, Email, Institution, Status
                    name = cols[0].text.strip()
                    email = cols[1].text.strip()
                    institution = cols[2].text.strip()
                    status = cols[4].text.strip()
                    results.append({
                        "name": name,
                        "email": email,
                        "institution": institution,
                        "status": status
                    })
            return results
        except Exception:
            return []

    def remove_first(self):
        # Elimina el primer instructor de la tabla "Result" si existe
        try:
            remove_btn = self.driver.find_element(By.XPATH, "//button[starts-with(@id,'remove-instructor-')]")
            remove_btn.click()
            time.sleep(0.7)
        except Exception:
            pass

    def run_case(self, case):
        self.go_to_form()
        self.fill_form(case["fields"])
        self.submit()
        time.sleep(1.2)
        
        obtained = ""
        locator = case["element_locator"]

        if case["Obs"] == "f+":
            # Para éxito: Se espera al menos un row en tabla Result con status PENDING y mismos datos ingresados
            rows = self.get_pending_rows()
            # Tomar los datos de entrada
            expected_rows = []
            lines = [x.strip() for x in case["fields"]["input_line"].split("\n") if x.strip()]
            for line in lines:
                parts = [p.strip() for p in line.split("|")]
                if len(parts) == 3:
                    expected_rows.append({
                        "name": parts[0],
                        "email": parts[1],
                        "institution": parts[2],
                        "status": "PENDING"
                    })
            # Se considera que el mensaje esperado es la fila en pending con los datos ingresados (como lo requiere el log)
            obtained = str(rows)
            case_expected = str(expected_rows)
            # Elimina el ejemplo añadido luego del test
            self.remove_first()
        else:
            # Para f-, no debe aparecer ningún mensaje ni tabla agregada
            rows = self.get_pending_rows()
            obtained = str(rows)
            case_expected = "[]"

        # Log detallado
        Utils.log_test(
            case["id"],
            case["fields"],
            case["expected"],
            obtained,
            case["Obs"]
        )
        return {
            "id": case["id"],
            "expected": case_expected,
            "obtained": obtained
        }

    def run(self):
        print(f"******************** RUN TEST-FN03 IN ********************")
        for case in self.cases:
            self.run_case(case)
        print(f"******************** **************** ********************")
        print("")

if __name__ == "__main__":
    checker = SeleniumConnection()
    driver, url = checker.connect_and_check_login()
    TestFn03(driver, url).run()