from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .objects import Scraper
import os
import random
import re


class Person(Scraper):

    __TOP_CARD = "scaffold-layout__main"
    __WAIT_FOR_ELEMENT_TIMEOUT = 5

    def __init__(
        self,
        link=None,
        driver=None,
        name=None,
        avatar=None,
        tags=None,
        location=None,
        job=None,
        recent=None,
        open_to_work=False,
        may_know_job=None,
        may_know_normal=None,
        login=False
    ):
        pattern = r'\?.*$'
        self.link = re.sub(pattern, "", link)
        self.name = name
        self.avatar = avatar
        self.tags = tags
        self.location = location
        self.job = job
        self.recent = recent
        self.open_to_work = open_to_work
        self.may_know_job = may_know_job or []
        self.may_know_normal = may_know_normal or []
        self.login = login

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

        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        driver.get(link)

        self.driver = driver

        self.scrape()

    def scrape(self):
        if self.is_signed_in():
            self.login = True
            self.scrape_logged_in()
        else:
            self.login = False
            print("登录失败")
            # self.driver.quit()

    def get_base_user_info(self):
        self.focus()
        print("获取个人基础信息")
        random_number = random.randint(90, 150)
        print(f"随机等待{random_number}秒")
        self.wait(random_number)

        main_block = self.driver.find_element(By.CLASS_NAME, "scaffold-layout__main")
        section_top = main_block.find_element(By.TAG_NAME, "section")
        self.name = section_top.find_element(By.TAG_NAME, "h1").text
        self.avatar = section_top.find_element(
            By.CLASS_NAME, "pv-top-card-profile-picture__image--show"
        ).get_attribute("src")
        # self.tags = (
        #     section_top.find_element(By.CLASS_NAME, "ph5")
        #     .find_element(By.CLASS_NAME, "mt2")
        #     .find_element(By.TAG_NAME, "div")
        #     .find_element(By.CLASS_NAME, "text-body-medium")
        #     .text
        # )
        self.location = (
            section_top.find_element(By.CLASS_NAME, "ph5")
            .find_element(By.CLASS_NAME, "mt2")
            .find_element(By.CLASS_NAME, "mt2")
            .find_element(By.TAG_NAME, "span")
            .text
        )
        self.job = (
            section_top.find_element(By.CLASS_NAME, "pv-open-to-carousel")
            .find_element(By.CLASS_NAME, "pv-open-to-carousel-card__content")
            .find_element(By.TAG_NAME, "p")
            .text
        )
        self.open_to_work = "#OPEN_TO_WORK" in section_top.find_element(
            By.CLASS_NAME, "pv-top-card-profile-picture__image--show"
        ).get_attribute("title")

        # print("成功获取个人基础信息")

    def get_recent_time(self):
        print("获取最近活跃时间")

        try:
            current_element = self.driver.find_element(By.ID, "content_collections")
            div_element = current_element.find_element(
                By.XPATH, "./following-sibling::*[contains(@class, 'ph5')]"
            )
            self.recent = (
                div_element.find_element(
                    By.CLASS_NAME, "feed-mini-update-contextual-description__text"
                )
                .find_element(By.CLASS_NAME, "visually-hidden")
                .text
            )
        except Exception as e:
            print("获取最近活跃时间失败")
            pass

    def get_may_know(self):
        random_number1 = random.randint(90, 120)
        print(f"随机等待{random_number1}秒")
        self.wait(random_number1)

        more_link = self.driver.find_element(
            By.ID, "navigation-overlay-section-pymk-education-see-more"
        ).get_attribute("href")
        print("打开可能认识的人")
        self.driver.get(more_link)
        self.focus()

        link_sources1 = []
        link_sources2 = []
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, ".artdeco-modal--layer-default")
                )
            )
            list_items = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located(
                    (
                        By.CSS_SELECTOR,
                        ".artdeco-modal--layer-default .artdeco-modal__content ul .artdeco-list__item",
                    )
                )
            )
            for li_element in list_items:
                try:
                    img_element = li_element.find_element(
                        By.CLASS_NAME, "ivm-view-attr__img--centered"
                    )
                    img_src = img_element.get_attribute("src")
                    user_link = li_element.find_element(
                        By.CLASS_NAME, "optional-action-target-wrapper"
                    ).get_attribute("href")
                    if "framedphoto" in img_src:
                        link_sources1.append(user_link)
                    if "displayphoto" in img_src:
                        link_sources2.append(user_link)
                except Exception as e:
                    pass

            self.may_know_job = link_sources1
            self.may_know_normal = link_sources2
        except Exception as e:
            print("打开可能认识的人失败")
            pass

        print("成功获取可能认识的人")
        self.driver.get(self.link)
        self.focus()
        random_number2 = random.randint(30, 60)
        print(f"随机等待{random_number2}秒")
        self.wait(random_number2)

    def scrape_logged_in(self):
        driver = self.driver

        WebDriverWait(driver, self.__WAIT_FOR_ELEMENT_TIMEOUT).until(
            EC.presence_of_element_located((By.CLASS_NAME, self.__TOP_CARD))
        )

        self.get_base_user_info()

        # self.get_recent_time()

        # self.get_may_know()

        # random_number = random.randint(60, 90)
        # print(f"随机等待{random_number}秒")
        # self.wait(random_number)

    def close(self):
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def to_dict(self):
        """将对象转换为字典"""
        return {
            "name": self.name,
            "link": self.link,
            "avatar": self.avatar,
            # "tags": self.tags,
            "location": self.location,
            "job": self.job,
            # "recent": self.recent,
            "open_to_work": self.open_to_work,
            # "may_know_job": self.may_know_job,
            # "may_know_normal": self.may_know_normal,
            "login": self.login
        }
