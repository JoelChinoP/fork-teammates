import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from dotenv import load_dotenv

# Helper to parse command-line args as key=value pairs
def get_arg(key, default=None):
    for arg in sys.argv[1:]:
        if arg.startswith(f"{key}="):
            return arg.split("=", 1)[1]
    return default

class SeleniumConnection:
    def __init__(self, url=None, token_name=None, token_value=None):
        load_dotenv()
        # Prioridad: argumentos>.env  (TOKEN_NAME=TOKEN_VALUE)
        self.url = get_arg("URL") or os.getenv("URL") or url
        self.token_name = get_arg("TOKEN_NAME") or os.getenv("TOKEN_NAME") or token_name
        self.token_value = get_arg("TOKEN_VALUE") or os.getenv("TOKEN_VALUE") or token_value
        if not all([self.url, self.token_name, self.token_value]):
            raise ValueError("Missing URL, TOKEN_NAME, or TOKEN_VALUE.")
        self.driver = None

    def connect_and_check_login(self):
        options = Options()
        options.add_argument("--headless=new")  # Descomentar si se requiere headless

        # Configuración de Chrome
        options.add_argument("--verbose")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        # Comentar si no se quiere usar Brave
        #options.binary_location = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"

        # Fijar versión de ChromeDriver
        service = Service(ChromeDriverManager().install())
        # Comentar la línea anterior y descomentar la siguiente si se quiere usar una versión específica
        #service = Service(ChromeDriverManager(driver_version="138.0.7204.49").install())

        self.driver = webdriver.Chrome(service=service, options=options)
        try:
            self.driver.get(self.url)
            self.driver.add_cookie({'name': self.token_name, 'value': self.token_value})
            self.driver.refresh()

            # Buscar el botón con el correo
            # Correos válidos: @gmail.com o @unsa.edu.pe
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//button["
                    "contains(text(),'@gmail.com') or "
                    "contains(text(),'@unsa.edu.pe')]"))
            )
            print("***Conexión exitosa y usuario autenticado...")
            print("")
        except Exception as e:
            print(f"Error: {e}")
            self.driver.quit()
            raise
        return self.driver, self.url

if __name__ == "__main__":
    checker = SeleniumConnection()
    driver = checker.connect_and_check_login()
    print("***Driver listo para siguientes pruebas...")
    driver.quit()