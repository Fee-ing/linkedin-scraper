from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from .objects import Scraper
import os


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
        may_know=None,
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
        self.may_know = may_know or []

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
            print("you are not logged in!")

    
    def get_base_user_info(self):
        self.focus()
        self.wait(5)

        main_block = self.driver.find_element(By.CLASS_NAME, "scaffold-layout__main")
        section_top = main_block.find_element(By.TAG_NAME, "section")
        self.name = section_top.find_element(By.TAG_NAME, "h1").text
        self.avatar = section_top.find_element(By.CLASS_NAME, "pv-top-card-profile-picture__image--show").get_attribute("src")
        self.tags = section_top.find_element(By.CLASS_NAME, "ph5").find_element(By.CLASS_NAME, "mt2").find_element(By.TAG_NAME, "div").find_element(By.CLASS_NAME, "text-body-medium").text
        self.location = section_top.find_element(By.CLASS_NAME, "ph5").find_element(By.CLASS_NAME, "mt2").find_element(By.TAG_NAME, "div").find_element(By.TAG_NAME, "span").text
        self.job = section_top.find_element(By.CLASS_NAME, "pv-open-to-carousel").find_element(By.CLASS_NAME, "pv-open-to-carousel-card__content").find_element(By.TAG_NAME, "p").text
        self.open_to_work = "#OPEN_TO_WORK" in section_top.find_element(By.CLASS_NAME, "pv-top-card-profile-picture__image--show").get_attribute("title")
        print("姓名: {name}\n主页: {linkedin_url}\n头像: {avatar}\n标签: {tags}\n位置: {location}\n是否求职: {open_to_work}\n求职方向: {job}".format(
            name=self.name,
            linkedin_url=self.linkedin_url,
            avatar=self.avatar,
            tags=self.tags,
            location=self.location,
            job=self.job,
            open_to_work="是" if self.open_to_work else "否"
        ))

    def get_may_know(self):
        self.wait(5)

        more_link = self.driver.find_element(By.ID, "navigation-overlay-section-pymk-education-see-more").get_attribute("href")
        self.driver.get(more_link)
        self.focus()
        
        link_sources = []
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
                    if "framedphoto" in img_src:
                        user_link = li_element.find_element(By.CLASS_NAME, "optional-action-target-wrapper").get_attribute("href")
                        link_sources.append(user_link)
                except Exception as e:
                    pass
            
            self.may_know = link_sources
            print(link_sources)
        except Exception as e:
            pass
        
        self.wait(5)
        self.driver.get(self.linkedin_url)
        self.focus()

    def scrape_logged_in(self, close_on_complete=True):
        driver = self.driver

        root = WebDriverWait(driver, self.__WAIT_FOR_ELEMENT_TIMEOUT).until(
            EC.presence_of_element_located(
                (
                    By.CLASS_NAME,
                    self.__TOP_CARD,
                )
            )
        )

        self.get_base_user_info()
        
        self.get_may_know()

        if close_on_complete:
            driver.quit()

    def __repr__(self):
        return self
