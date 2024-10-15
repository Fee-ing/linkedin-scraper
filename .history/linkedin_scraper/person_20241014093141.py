from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from .objects import Scraper
import os
import random

class Person(Scraper):

    __TOP_CARD = "scaffold-layout__main"
    __WAIT_FOR_ELEMENT_TIMEOUT = 5

    def __init__(
        self,
        linkedin_url=None,
        name=None,
        avatar=None,
        tags=None,
        location=None,
        job=None,
        open_to_work=False,
        may_know_job=None,
        may_know_normal=None,
        driver=None,
        get=True,
        scrape=True,
        close_on_complete=False,
    ):
        self.linkedin_url = linkedin_url
        self.name = name
        self.avatar = avatar
        self.tags = tags
        self.location = location
        self.job = job
        self.open_to_work = open_to_work
        self.may_know_job = may_know_job or []
        self.may_know_normal = may_know_normal or []

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

        if get:
            driver.get(linkedin_url)

        self.driver = driver

        if scrape:
            self.scrape(close_on_complete)

    def scrape(self, close_on_complete=True):
        if self.is_signed_in():
            self.scrape_logged_in(close_on_complete=close_on_complete)
        else:
            print("登录失败")
            self.driver.quit()
    
    def get_base_user_info(self):
        self.focus()
        print("获取个人基础信息")
        random_number = random.randint(4, 10)
        print("随机等待{random_number}秒")
        self.wait(random_number)

        main_block = self.driver.find_element(By.CLASS_NAME, "scaffold-layout__main")
        section_top = main_block.find_element(By.TAG_NAME, "section")
        self.name = section_top.find_element(By.TAG_NAME, "h1").text
        self.avatar = section_top.find_element(By.CLASS_NAME, "pv-top-card-profile-picture__image--show").get_attribute("src")
        self.tags = section_top.find_element(By.CLASS_NAME, "ph5").find_element(By.CLASS_NAME, "mt2").find_element(By.TAG_NAME, "div").find_element(By.CLASS_NAME, "text-body-medium").text
        self.location = section_top.find_element(By.CLASS_NAME, "ph5").find_element(By.CLASS_NAME, "mt2").find_element(By.TAG_NAME, "div").find_element(By.TAG_NAME, "span").text
        self.job = section_top.find_element(By.CLASS_NAME, "pv-open-to-carousel").find_element(By.CLASS_NAME, "pv-open-to-carousel-card__content").find_element(By.TAG_NAME, "p").text
        self.open_to_work = "#OPEN_TO_WORK" in section_top.find_element(By.CLASS_NAME, "pv-top-card-profile-picture__image--show").get_attribute("title")

    def get_may_know(self):
        random_number1 = random.randint(4, 10)
        print("随机等待{random_number1}秒")
        self.wait(random_number1)

        more_link = self.driver.find_element(By.ID, "navigation-overlay-section-pymk-education-see-more").get_attribute("href")
        print("打开可能认识的人")
        self.driver.get(more_link)
        self.focus()
        
        link_sources1 = []
        link_sources2 = []
        try:
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".artdeco-modal--layer-default"))
            )
            list_items = WebDriverWait(self.driver, 15).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".artdeco-modal--layer-default .artdeco-modal__content ul .artdeco-list__item"))
            )
            for li_element in list_items:
                try:
                    img_element = li_element.find_element(By.CLASS_NAME, "ivm-view-attr__img--centered")
                    img_src = img_element.get_attribute("src")
                    user_link = li_element.find_element(By.CLASS_NAME, "optional-action-target-wrapper").get_attribute("href")
                    if "framedphoto" in img_src:
                        link_sources1.append(user_link)
                    if "displayphoto" in img_src:
                        link_sources2.append(user_link)
                except Exception as e:
                    pass
            
            self.may_know_job = link_sources1
            self.may_know_normal = link_sources2
        except Exception as e:
            pass
        
        print("获取可能认识的人")
        random_number2 = random.randint(4, 10)
        print("随机等待{random_number2}秒")
        self.wait(random_number2)
        print("返回个人主页")
        self.driver.get(self.linkedin_url)
        self.focus()

    def scrape_logged_in(self, close_on_complete=True):
        driver = self.driver

        print("打开个人主页")
        WebDriverWait(driver, self.__WAIT_FOR_ELEMENT_TIMEOUT).until(
            EC.presence_of_element_located((By.CLASS_NAME, self.__TOP_CARD))
        )

        self.get_base_user_info()
        
        self.get_may_know()

        if close_on_complete:
            driver.quit()
    
    def to_dict(self):
        """将对象转换为字典"""
        return {
            'name': self.name,
            'linkedin_url': self.linkedin_url,
            'avatar': self.avatar,
            'tags': self.tags,
            'location': self.location,
            'job': self.job,
            'open_to_work': self.open_to_work,
            'may_know_job': self.may_know_job
        }
