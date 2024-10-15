from linkedin_scraper import Person, Search, actions
from selenium import webdriver
import subprocess
import os
import json
import requests

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

# 第一个参数是关键词，第二个参数是时间范围，单位是秒，表示筛选多少秒内的结果
search = Search("#opentowork american inc", 18000, driver=driver)
search_result = search.to_dict()

for data in search_result:
    person = Person(data["link"], driver=driver)
    person_result = person.to_dict()
    params = {
        "kh_name": person_result["name"],
        "kh_avatar": person_result["avatar"],
        "kh_guojia": person_result["location"],
        "kh_gz": person_result["job"],
        "kh_tune": data["recent"],
        "kh_url": person_result["link"],
    }
    print(json.dumps(params.to_dict(), indent=4))
    response = requests.get("/pull-msg", params=params)
    if response.status_code == 200:
        # 请求成功，处理响应数据
        data = response.json()
        print(data)
    else:
        # 请求失败，打印状态码和错误信息
        print(f"请求失败，状态码：{response.status_code}")

driver.quit()