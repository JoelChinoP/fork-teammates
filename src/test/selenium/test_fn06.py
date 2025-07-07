import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time, json
from utils import Utils


class TestFn06:
    def __init__(self, driver, url):
        self.driver, self.url = driver, url
        self.home_path = "/web/admin/home"
        self.search_path = "/web/admin/search"
        self.form_fields = {
            "search": (By.ID, "search-box"),
            "submit": (By.ID, "search-button")
        }
        with open("data/fn06.json") as f:
            self.cases = json.load(f)

    def go_to_form(self):
        self.driver.get(self.url + self.home_path)
        search_link = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Search"))
        )
        search_link.click()
        time.sleep(5)
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(self.form_fields["submit"])
        )

    def run(self):
        for case in self.cases:
            print(f"\n Ejecutando caso: {case['id']} - {case['description']}")
            try:
                self.go_to_form()
                search_box = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.ID, "search-box"))
                )
                self.driver.execute_script("arguments[0].value = '';", search_box)
                self.driver.execute_script("""
                    const input = arguments[0];
                    const value = arguments[1];
                    input.value = value;
                    input.dispatchEvent(new Event('input', { bubbles: true }));
                    input.dispatchEvent(new Event('change', { bubbles: true }));
                """, search_box, case["input"])
                print(f"  > Valor ingresado: {case['input']}")
                time.sleep(1.5)
                submit_btn = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.ID, "search-button"))
                )
                submit_btn.click()
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//*[contains(text(), 'Instructors Found')]")
                    )
                )
                time.sleep(3)
                if case["expected_result"] and case["expected_result"] not in self.driver.page_source:
                    print(f"  Resultado '{case['expected_result']}' no encontrado.")
                else:
                    print("  Resultado conforme a lo esperado.")
            except Exception as e:
                print(f"Error en el caso {case['id']}: {e}")

    def set_token(self, token_value):
        self.driver.get(self.url)
        self.driver.add_cookie({
            'name': 'AUTH-TOKEN',
            'value': token_value
        })
        self.driver.refresh()


if __name__ == "__main__":
    from selenium import webdriver

    driver = webdriver.Chrome()
    driver.maximize_window()
    url = os.getenv("URL", "https://cigarra-teammates.appspot.com")
    token = os.getenv("TOKEN_VALUE", "")
    test = TestFn06(driver, url)
    test.set_token(token)
    test.run()
    driver.quit()
