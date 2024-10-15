import getpass
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver

driver = webdriver.Chrome()

VERIFY_LOGIN_ID = "global-nav__primary-link"
REMEMBER_PROMPT = 'remember-me-prompt__form-primary'
email = "some-email@email.address"
password = "password123"

def _login_with_cookie(driver, cookie):
    driver.get("https://www.linkedin.com/login")
    driver.add_cookie({
      "name": "li_at",
      "value": cookie
    })

# actions.login(driver, email, password) # if email and password isnt given, it'll prompt in terminal
# person = Person("https://www.linkedin.com/in/joey-sham-aa2a50122", driver=driver)

_login_with_cookie(driver, "")