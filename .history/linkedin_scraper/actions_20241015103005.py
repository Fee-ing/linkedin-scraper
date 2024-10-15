import getpass
from . import constants as c
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


def __prompt_email_password():
    u = input("Email: ")
    p = getpass.getpass(prompt="Password: ")
    return (u, p)


def page_has_loaded(driver):
    page_state = driver.execute_script("return document.readyState;")
    return page_state == "complete"

def judge_is_in_check(driver):
    if "checkpoint" in driver.current_url:
        print("进行快速安全验证")
        sleep(5)
        return judge_is_in_check(driver)
    else:
        print("安全验证通过")
        return True


def login(driver, email=None, password=None, cookie=None, timeout=10):
    if cookie is not None:
        return _login_with_cookie(driver, cookie)

    if not email or not password:
        email, password = __prompt_email_password()

    driver.get("https://www.linkedin.com/login")
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "username"))
    )

    email_elem = driver.find_element(By.ID, "username")
    email_elem.send_keys(email)

    password_elem = driver.find_element(By.ID, "password")
    password_elem.send_keys(password)
    password_elem.submit()

    judge_is_in_check(driver)

    print("11111")

    # if driver.current_url == "https://www.linkedin.com/checkpoint/lg/login-submit":
    #     remember = driver.find_element(By.ID, c.REMEMBER_PROMPT)
    #     if remember:
    #         remember.submit()

    # element = WebDriverWait(driver, timeout).until(
    #     EC.presence_of_element_located((By.CLASS_NAME, c.VERIFY_LOGIN_ID))
    # )


def _login_with_cookie(driver, cookie):
    print("使用cookie登录")
    driver.get("https://www.linkedin.com/login")
    driver.add_cookie({"name": "li_at", "value": cookie})
