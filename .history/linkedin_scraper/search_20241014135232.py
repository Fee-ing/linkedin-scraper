from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from .objects import Scraper
import os
import re
import random

class Search(Scraper):

    def __init__(
        self,
        keyword=None,
        driver=None,
        result=None
    ):
        self.keyword = keyword or ""
        self.result = result or []

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

        driver.get(f"https://www.linkedin.com/search/results/content/?keywords={self.keyword}&origin=FACETED_SEARCH&sid=iBf&sortBy=%22date_posted%22")

        self.driver = driver

        self.scrape()

    def scrape(self):
        if self.is_signed_in():
            self.scrape_logged_in()
        else:
            print("登录失败")
            self.driver.quit()

    def get_time_number(text):
        match = re.search(r'\d+', text)
        num = 0
        if match:
            num = int(match.group())
        elif "分钟" in text or "m" in text:
            num = num * 60
        elif "小时" in text or "h" in text:
            num = num * 3600
        return num

    def get_users(self):
        random_number = random.randint(4, 10)
        print(f"随机等待{random_number}秒")
        self.wait(random_number)
        page_elment = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "search-srp-prompt"))
        )

        page_text = page_elment.text
        matches = re.findall(r'\d+', page_text)
        numbers = [int(match) for match in matches]
        current_page = numbers[1]
        total_page = numbers[2]

        print(f"{total_page}中的第{current_page}页")

        try:
          list_items = WebDriverWait(self.driver, 10).until(
              EC.presence_of_all_elements_located(
                  (
                      By.CLASS_NAME,
                      "artdeco-card",
                  )
              )
          )
          if current_page == 1:
              last_six_items = list_items
          else:
              last_six_items = list_items[-6:]
          for li_element in last_six_items:
              try:
                  a_element = li_element.find_element(
                      By.CLASS_NAME, "update-components-actor__container"
                  )
                  img_element = a_element.find_element(By.CLASS_NAME, "ivm-view-attr__img--centered")
                  img_src = img_element.get_attribute("src")
                  user_link = a_element.get_attribute("href")
                  user_name = a_element.find_element(By.CLASS_NAME, "update-components-actor__name").text
                  user_recent = a_element.find_element(By.CLASS_NAME, "update-components-actor__sub-description").find_element(By.TAG_NAME, "span").text
                  if "framedphoto" in img_src:
                      self.result.append({ "name": user_name, "link": user_link, "recent": user_recent })
                      
              except Exception as e:
                  pass
        except Exception as e:
            print("获取搜索结果失败")
            return self.result
        
        if current_page == total_page:
            return self.result
        else:
            self.scroll_to_bottom()
            return self.get_users()

    def scrape_logged_in(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "scaffold-layout__main"))
        )
        
        self.get_users()

    def to_dict(self):
        """将对象转换为字典"""
        return self.result
