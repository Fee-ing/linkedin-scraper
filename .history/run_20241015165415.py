from utils import Person, Search, actions
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import requests
from pprint import pprint
from time import sleep
import os
import signal
import subprocess

# 13305899774
email = "kjdsjh@163.com"
password = "Wen3597135"
cookie = ""


def kill_chrome_processes():
    # 查找Chrome或Chromedriver进程
    processes = subprocess.check_output(["ps", "aux"]).decode()
    for line in processes.split("\n"):
        if "chrome" in line or "chromedriver" in line:
            pid = int(line.split()[1])
            print(f"Killing process {pid}")
            os.kill(pid, signal.SIGKILL)


def getKeyword():
    try:
        response = requests.get("http://172.30.20.244/get-key-word")
        if response.status_code == 200:
            data = response.json()
            return data["data"]["key"]
        else:
            print(f"获取关键词失败，状态码：{response.status_code}")
            return None
    except Exception as e:
        print("获取关键词失败")
        return None


def submitData(params):
    try:
        response = requests.get("http://172.30.20.244/pull-msg", params=params)
        if response.status_code == 200:
            # 请求成功，处理响应数据
            data = response.json()
            print(data)
        else:
            # 请求失败，打印状态码和错误信息
            print(f"上传数据失败，状态码：{response.status_code}")
    except Exception as e:
        print("上传数据失败")
        pass


def scrape(driver, keyword, time_limit):
    # 查询关键词
    search = Search(keyword, time_limit, driver=driver)
    search_result = search.to_dict()
    if search_result["login"] == False:
        actions.login(driver, email, password)

    data_list = search_result["result"]

    print(f"共查找出{len(data_list)}条数据")

    for data in data_list:
        person = Person(data["link"], driver=driver)
        person_result = person.to_dict()
        if person_result["login"] and person_result["open_to_work"]:
            params = {
                "kh_name": person_result["name"],
                "kh_avatar": person_result["avatar"],
                "kh_guojia": person_result["location"],
                "kh_gz": person_result["job"],
                "kh_time": data["recent"],
                "kh_url": person_result["link"],
                "type": "叶",
                "key_word": keyword,
            }
            pprint(params)
            submitData(params)
            sleep(2)
        elif person_result["login"] == False:
            actions.login(driver, email, password)


def main():
    kill_chrome_processes()

    try:
        # 配置Chrome选项
        chrome_options = Options()
        # 设置代理服务器信息
        proxy_server = "http://127.0.0.1:7890"
        chrome_options.add_argument(f"--proxy-server={proxy_server}")
        # 设置ChromeDriver的路径
        service = Service(executable_path="/usr/local/bin/chromedriver")
        # 创建WebDriver实例
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # actions._login_with_cookie(driver, cookie)
        actions.login(driver, email, password)

        for i in range(100):
            print(f"这是第 {i + 1} 次执行")

            keyword = getKeyword()

            if keyword:
                print(f"关键词为{keyword}")
                scrape(
                    driver,
                    keyword,
                    24 * 3600,
                )

    finally:
        if driver is not None:
            driver.quit()


if __name__ == "__main__":
    main()
