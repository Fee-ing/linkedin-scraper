from linkedin_scraper import Person, Search, actions
from selenium import webdriver
import json
import subprocess
import os

def kill_chrome_processes():
    if os.name == 'posix':  # Linux or macOS
        subprocess.run(["pkill", "chrome"])
        subprocess.run(["pkill", "chromedriver"])
    elif os.name == 'nt':  # Windows
        subprocess.run(["taskkill", "/F", "/IM", "chrome.exe"])
        subprocess.run(["taskkill", "/F", "/IM", "chromedriver.exe"])

# 在启动 WebDriver 之前调用此函数
kill_chrome_processes()

driver = webdriver.Chrome()

# email = "some-email@email.address"
# password = "password123"
# actions.login(driver, email, password)

cookie_value = "AQEDAVNZ2TIAVsLEAAABkoijwcsAAAGSrLBFy1YAAHjj7C4lharmsxCLzTR1eT723HRpMR6xEKK7JXyBdbZVsgLA91oKYUd2ihX8M0QCvwDuPMx4qudXeMpoBMmER9i-RCP9Psj7kQoCESyf2uBQ2LzC"
actions._login_with_cookie(driver, cookie_value)

# person = Person("https://www.linkedin.com/in/klaudia-szkopiak-477151308/", driver=driver)
# print(json.dumps(person.to_dict(), indent=4))

search = Search("Sverige", driver=driver)

print(search)
print(search.to_dict())

driver.quit()