from linkedin_scraper import Person, Search, actions
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import requests
from pprint import pprint
from time import sleep

# 指定ChromeDriver的路径
chromedriver_path = '/path/to/chromedriver'

# 设置端口号
port_number = 23333

# 创建Service对象，并指定端口
service = Service(executable_path=chromedriver_path)
service.port = port_number

# 创建ChromeOptions对象
options = Options()

email = "jegxijibboa@mail.ru"
password = "hGMaO86w9H?"
cookie = "AQEDAVNZ5AAFAADiAAABko2rRf4AAAGSsbfJ_lYAcpe9Ev_lcBskOnZrgUxxHFyGmKiSXwqQlX8pEBx3D9PDB0XUfVDDDbq2Ub-bmhipSgaHWhfNrmlh99ZUB6R2aTeZfJ5YzY2OIu5ccojrZ4PBrkpE"


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

    print(search_result)

    for data in search_result:
        person = Person(data["link"], driver=driver)
        person_result = person.to_dict()
        params = {
            "kh_name": person_result["name"],
            "kh_avatar": person_result["avatar"],
            "kh_guojia": person_result["location"],
            "kh_gz": person_result["job"],
            "kh_time": data["recent"],
            "kh_url": person_result["link"],
            "type": "叶",
        }
        pprint({**person_result, **{"recent": data["recent"]}})
        if person_result["open_to_work"]:
            submitData(params)
            sleep(2)

    driver.quit()


def run():
    driver = webdriver.Chrome(service=service, options=options)

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

run()