from utils import Search, actions
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import requests
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
                # 查询关键词
                search = Search(keyword, 24 * 3600, driver=driver)
                search_result = search.to_dict()
                if search_result["login"] == False:
                    actions.login(driver, email, password)

                print("等待10分钟后再次执行")
                sleep(600)

    finally:
        if driver is not None:
            driver.quit()


if __name__ == "__main__":
    main()
