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

    def scrape_logged_in(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "scaffold-layout__main"))
        )
        page_elment = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "search-srp-prompt"))
        )
        self.wait(2)

        page_text = page_elment.text
        matches = re.findall(r'\d+', page_text)
        numbers = [int(match) for match in matches]
        current_page = numbers[1]
        total_page = numbers[2]

        print(current_page)
        print(total_page)

        try:
          list_items = WebDriverWait(self.driver, 10).until(
              EC.presence_of_all_elements_located(
                  (
                      By.CLASS_NAME,
                      "artdeco-card",
                  )
              )
          )
          for li_element in list_items:
              try:
                  a_element = li_element.find_element(
                      By.CLASS_NAME, "update-components-actor__container"
                  )
                  img_element = a_element.find_element(By.CLASS_NAME, "ivm-view-attr__img--centered")
                  img_src = img_element.get_attribute("src")
                  user_link = a_element.get_attribute("href")
                  if "framedphoto" in img_src:
                      self.result.append(user_link)
              except Exception as e:
                  pass
        except Exception as e:
            print("获取搜索结果失败")
            pass

