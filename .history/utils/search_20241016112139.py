from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import quote
from pprint import pprint
from .objects import Scraper
from .person import Person
import os
import re
import random
import requests


class Search(Scraper):

    def __init__(self, keyword=None, limit=None, driver=None, result=None):
        self.keyword = quote(keyword or "", safe="")
        self.limit = limit or 3600
        self.result = result or []
        self.login = False

        if driver is None:
            try:
                if os.getenv("CHROMEDRIVER") == None:
                    driver_path = os.path.join(
                        os.path.dirname(__file__), "drivers/chromedriver"
                    )
                else:
                    driver_path = os.getenv("CHROMEDRIVER")

                driver = webdriver.Chrome(driver_path)
            except:
                driver = webdriver.Chrome()

        driver.get(
            f"https://www.linkedin.com/search/results/content/?keywords={self.keyword}&origin=FACETED_SEARCH&sid=iBf&sortBy=%22date_posted%22"
        )

        self.driver = driver

        self.scrape()

    def scrape(self):
        if self.is_signed_in():
            self.login = True
            self.scrape_logged_in()
        else:
            self.login = False
            print("登录失败, 请重新登录")
    
    def scrape_logged_in(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "scaffold-layout__main"))
        )
        self.scroll_to_bottom()
        self.get_users()

    def get_time_number(self, text):
        match = re.search(r"\d+", text)
        num = 0
        if match:
            num = int(match.group())
        
        if "年" in text or "yr" in text:
            num = num * 3600 * 24 * 365
        if "月" in text or "mo" in text:
            num = num * 3600 * 24 * 30
        elif "周" in text or "w" in text:
            num = num * 3600 * 24 * 7
        elif "天" in text or "d" in text:
            num = num * 3600 * 24
        elif "小时" in text or "h" in text:
            num = num * 3600
        elif "分钟" in text or "m" in text:
            num = num * 60
        return num

    def get_users(self):
        random_number = random.randint(30, 60)
        print(f"随机等待{random_number}秒")
        self.wait(random_number)
        page_elment = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "search-srp-prompt"))
        )

        page_text = page_elment.text
        matches = re.findall(r"\d+", page_text)
        numbers = [int(match) for match in matches]
        current_page = numbers[1]
        total_page = numbers[2]

        try:
            list_items = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located(
                    (
                        By.CSS_SELECTOR,
                        ".scaffold-layout__main .scaffold-finite-scroll__content li.artdeco-card",
                    )
                )
            )
            last_items = []
            if current_page == 1:
                last_items = list_items
            elif len(list_items) >= 10:
                last_items = list_items[-10:]
            else:
                last_items = list_items

            for li_element in last_items:
                try:
                    element = li_element.find_element(
                        By.CLASS_NAME, "update-components-actor"
                    )
                    user_link = element.find_element(
                        By.CLASS_NAME, "update-components-actor__image"
                    ).get_attribute("href")
                    pattern1 = r'\?.*$'
                    user_link = re.sub(pattern1, "", user_link)
                    user_avatar = element.find_element(
                        By.CLASS_NAME, "ivm-view-attr__img--centered"
                    ).get_attribute("src")
                    user_name = (
                        element.find_element(
                            By.CLASS_NAME, "update-components-actor__name"
                        )
                        .find_element(By.TAG_NAME, "span")
                        .find_element(By.TAG_NAME, "span")
                        .text
                    )
                    user_recent = (
                        element.find_element(
                            By.CLASS_NAME, "update-components-actor__sub-description"
                        )
                        .find_element(By.TAG_NAME, "span")
                        .text
                    )
                    pattern2 = r"[\s\n•]+"
                    user_recent = re.sub(pattern2, "", user_recent)
                    limit_number = self.get_time_number(user_recent)

                    if limit_number <= self.limit:
                        if "framedphoto" in user_avatar and any(obj["link"] == user_link for obj in self.result) == False:
                            self.result.append(
                                {
                                    "name": user_name,
                                    "link": user_link,
                                    "recent": user_recent,
                                }
                            )
                            is_continue = self.get_info(user_link, user_recent)
                            if is_continue == False:
                                return self.login
                    else:
                        print(f"执行搜索{self.keyword}结束")
                        return self.login

                except Exception as e:
                    pass
        except Exception as e:
            print(f"执行搜索{self.keyword}失败")
            return self.login

        if current_page == total_page:
            return self.login
        else:
            self.scroll_to_bottom()
            return self.get_users()

    def get_info(self, link, recent):
        person = Person(link, driver=self.driver)
        person_result = person.to_dict()
        result = True
        if person_result["login"] and person_result["open_to_work"]:
            params = {
                "kh_name": person_result["name"],
                "kh_avatar": person_result["avatar"],
                "kh_guojia": person_result["location"],
                "kh_gz": person_result["job"],
                "kh_time": recent,
                "kh_url": person_result["link"],
                "type": "叶",
                "key_word": self.keyword,
            }
            pprint(params)
            self.submit_user_data(params)
        elif person_result["login"] == False:
            self.login = False
            result = False
        random_number = random.randint(15, 30)
        print(f"随机等待{random_number}秒")
        self.wait(random_number)
        return result

    def submit_user_data(params):
        print(f"上传用户{params["kh_name"]}数据")
        try:
            response = requests.get("http://172.30.20.244/pull-msg", params=params)
            if response.status_code == 200:
                # 请求成功，处理响应数据
                data = response.json()
                print(data)
            else:
                # 请求失败，打印状态码和错误信息
                print(f"上传用户{params["kh_name"]}数据失败，状态码：{response.status_code}")
        except Exception as e:
            print(f"上传用户{params["kh_name"]}数据失败")
            pass

    def to_dict(self):
        """将对象转换为字典"""
        return self.login
