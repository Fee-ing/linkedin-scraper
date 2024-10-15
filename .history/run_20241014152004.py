from linkedin_scraper import Person, Search, actions
from selenium import webdriver
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

cookie_value = "AQEDAVNZ2TIAVsLEAAABkoijwcsAAAGSrLBFy1YAAHjj7C4lharmsxCLzTR1eT723HRpMR6xEKK7JXyBdbZVsgLA91oKYUd2ihX8M0QCvwDuPMx4qudXeMpoBMmER9i-RCP9Psj7kQoCESyf2uBQ2LzC"
actions._login_with_cookie(driver, cookie_value)

result = []

# 第一个参数是关键词，第二个参数是时间范围，单位是秒，表示筛选多少秒内的结果
search = Search("#opentowork american inc", 18000, driver=driver)
search_result = search.to_dict()
print(search_result)

for data in search_result:
    print(data["link"])
    person = Person(data["link"], driver=driver)
    person_result = person.to_dict()
    result.append({**person_result, **{"recent": data["recent"]}})

print(result)

driver.quit()