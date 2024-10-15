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
    ):
        self.keyword = keyword or ""

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
        
        link = "https://www.linkedin.com/search/results/content/?keywords={keyword}&origin=FACETED_SEARCH&sid=iBf&sortBy=%22date_posted%22"
        print(link)

        driver.get("https://www.linkedin.com/search/results/content/?keywords={keyword}&origin=FACETED_SEARCH&sid=iBf&sortBy=%22date_posted%22")

        self.driver = driver

        self.scrape()

    def scrape(self):
        if self.is_signed_in():
            self.scrape_logged_in()
        else:
            print("登录失败")
            self.driver.quit()

    def scrape_logged_in(self):
        print("开始搜索")
        page_elment = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "search-srp-prompt"))
        )
        page_text = page_elment.text
        matches = re.findall(r'\d+', page_text)
        numbers = [int(match) for match in matches]
        current_page = numbers[1]
        total_page = numbers[2]
        print(current_page)
        print(total_page)

        list_items = self.driver.find_elements(By.CLASS_NAME, "artdeco-card")
        print(len(list_items))
