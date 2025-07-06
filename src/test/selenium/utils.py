from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

class Utils:
  @staticmethod
  def solve_recaptcha(driver):
    try:
        iframe = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//iframe[@title='reCAPTCHA']"))
        )
        driver.switch_to.frame(iframe)
        checkbox = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "recaptcha-anchor"))
        )
        checkbox.click()
        driver.switch_to.default_content()
        time.sleep(1)
    except Exception as e:
        print("Error reCAPTCHA:", e)
        driver.switch_to.default_content()
  
  @staticmethod
  def shorten(text, maxlen=1000):
    if len(text) <= maxlen:
        return text
    half = maxlen // 2
    return f"{text[:half]} ... {text[-half:]}"
  
  @staticmethod
  def log_test(test_code, input_data, expected, obtained, obs):
    MAX_LEN = 1000
    status = "PASSED" if expected in obtained else "FAILED"
    print(f"::group::[{status}] TEST-{test_code.upper()}")

    print(f"\tInput:")
    if isinstance(input_data, dict):
        for k, v in input_data.items():
            print(f"\t\t{k}: {v}")
    else:
        print(f"\t\t{input_data}")

    print(f"\tExpected:\n\t\t{Utils.shorten(str(expected), MAX_LEN)}")
    print(f"\tObtained:\n\t\t{Utils.shorten(str(obtained), MAX_LEN)}")
    print(f"\tObs:\n\t\t{obs}")
    print("")  # Agregar un salto de línea para mejorar la legibilidad
    print("::endgroup::")
