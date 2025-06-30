import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
import time

class SeleniumConnectionChecker:
    def __init__(self, url=None, cookie_name=None, cookie_value=None):
        load_dotenv()
        self.url = url or os.getenv("URL") or (len(sys.argv) > 1 and sys.argv[1])
        self.cookie_name = cookie_name or os.getenv("COOKIE_NAME") or (len(sys.argv) > 2 and sys.argv[2])
        self.cookie_value = cookie_value or os.getenv("COOKIE_VALUE") or (len(sys.argv) > 3 and sys.argv[3])
        if not self.url or not self.cookie_name or not self.cookie_value:
            raise ValueError("Missing URL, COOKIE_NAME, or COOKIE_VALUE.")
        self.driver = None

    def connect_and_check_login(self, email_to_check):
        options = Options()
        # options.add_argument("--headless") 
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        domain = self.url.split("//")[-1].split("/")[0]
        try:
            self.driver.get(self.url)
            self.driver.add_cookie({
                'name': self.cookie_name,
                'value': self.cookie_value,
                'domain': domain,
                'path': '/',
            })
            self.driver.refresh()
            time.sleep(1)
            user_btns = self.driver.find_elements(By.XPATH, f"//button[contains(text(), '{email_to_check}')]")
            if user_btns:
                print(f"Login exitoso")
            else:
                raise Exception(f"No se encontró el correo en la barra de navegación.")
        except Exception as e:
            print(f"Error: {e}")
            self.driver.quit()
            raise
        return self.driver

if __name__ == "__main__":
    email = os.getenv("CORREO") or (len(sys.argv) > 4 and sys.argv[4])
    checker = SeleniumConnectionChecker()
    driver = checker.connect_and_check_login(email)
    print("Driver listo para siguientes pruebas.")
    driver.quit()