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
  def log_test(test_code, input_data, expected, obtained, obs):
    status = "PASSED" if expected in obtained else "FAILED" # Si el resultado esperado está contenido en el obtenido
    print(f"::group::[{status}] TEST-{test_code.upper()}")

    print(f"\tInput:\n\t\t{input_data}")
    print(f"\tExpected:\n\t\t{expected}")
    print(f"\tObtained:\n\t\t{obtained}")
    print(f"\tObs:\n\t\t{obs}") #f- or f+
    print("::endgroup::")
