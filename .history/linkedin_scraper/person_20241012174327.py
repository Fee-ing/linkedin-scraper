from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from .objects import Experience, Education, Scraper, Interest, Accomplishment, Contact
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

        about=None,
        experiences=None,
        educations=None,
        interests=None,
        accomplishments=None,
        company=None,
        job_title=None,
        contacts=None,
        driver=None,
        get=True,
        scrape=True,
        close_on_complete=True,
        time_to_wait_after_login=0,
    ):
        self.linkedin_url = linkedin_url
        self.name = name
        self.avatar = avatar
        self.tags = tags
        self.location = location
        self.job = job
        self.open_to_work = open_to_work
        self.may_know = may_know or []

        self.about = about or []
        self.experiences = experiences or []
        self.educations = educations or []
        self.interests = interests or []
        self.accomplishments = accomplishments or []
        self.also_viewed_urls = []
        self.contacts = contacts or []

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

    def add_about(self, about):
        self.about.append(about)

    def add_experience(self, experience):
        self.experiences.append(experience)

    def add_education(self, education):
        self.educations.append(education)

    def add_interest(self, interest):
        self.interests.append(interest)

    def add_accomplishment(self, accomplishment):
        self.accomplishments.append(accomplishment)

    def add_location(self, location):
        self.location = location

    def add_contact(self, contact):
        self.contacts.append(contact)

    def scrape(self, close_on_complete=True):
        if self.is_signed_in():
            self.scrape_logged_in(close_on_complete=close_on_complete)
        else:
            print("you are not logged in!")

    def _click_see_more_by_class_name(self, class_name):
        try:
            _ = WebDriverWait(self.driver, self.__WAIT_FOR_ELEMENT_TIMEOUT).until(
                EC.presence_of_element_located((By.CLASS_NAME, class_name))
            )
            div = self.driver.find_element(By.CLASS_NAME, class_name)
            div.find_element(By.TAG_NAME, "button").click()
        except Exception as e:
            pass

    def is_open_to_work(self):
        try:
            return "#OPEN_TO_WORK" in self.driver.find_element(By.CLASS_NAME,"pv-top-card-profile-picture").find_element(By.TAG_NAME,"img").get_attribute("title")
        except:
            return False

    def get_experiences(self):
        url = os.path.join(self.linkedin_url, "details/experience")
        self.driver.get(url)
        self.focus()
        main = self.wait_for_element_to_load(by=By.TAG_NAME, name="main")
        self.scroll_to_half()
        self.scroll_to_bottom()
        main_list = self.wait_for_element_to_load(name="pvs-list__container", base=main)
        for position in main_list.find_elements(By.CLASS_NAME, "pvs-list__paged-list-item"):
            position = position.find_element(By.CSS_SELECTOR, "div[data-view-name='profile-component-entity']")
            company_logo_elem, position_details = position.find_elements(By.XPATH, "*")

            # company elem
            company_linkedin_url = company_logo_elem.find_element(By.XPATH,"*").get_attribute("href")
            if not company_linkedin_url:
                continue

            # position details
            position_details_list = position_details.find_elements(By.XPATH,"*")
            position_summary_details = position_details_list[0] if len(position_details_list) > 0 else None
            position_summary_text = position_details_list[1] if len(position_details_list) > 1 else None
            outer_positions = position_summary_details.find_element(By.XPATH,"*").find_elements(By.XPATH,"*")

            if len(outer_positions) == 4:
                position_title = outer_positions[0].find_element(By.TAG_NAME,"span").text
                company = outer_positions[1].find_element(By.TAG_NAME,"span").text
                work_times = outer_positions[2].find_element(By.TAG_NAME,"span").text
                location = outer_positions[3].find_element(By.TAG_NAME,"span").text
            elif len(outer_positions) == 3:
                if "·" in outer_positions[2].text:
                    position_title = outer_positions[0].find_element(By.TAG_NAME,"span").text
                    company = outer_positions[1].find_element(By.TAG_NAME,"span").text
                    work_times = outer_positions[2].find_element(By.TAG_NAME,"span").text
                    location = ""
                else:
                    position_title = ""
                    company = outer_positions[0].find_element(By.TAG_NAME,"span").text
                    work_times = outer_positions[1].find_element(By.TAG_NAME,"span").text
                    location = outer_positions[2].find_element(By.TAG_NAME,"span").text
            else:
                position_title = ""
                company = outer_positions[0].find_element(By.TAG_NAME,"span").text
                work_times = ""
                location = ""


            times = work_times.split("·")[0].strip() if work_times else ""
            duration = work_times.split("·")[1].strip() if len(work_times.split("·")) > 1 else None

            from_date = " ".join(times.split(" ")[:2]) if times else ""
            to_date = " ".join(times.split(" ")[3:]) if times else ""
            if position_summary_text and any(element.get_attribute("pvs-list__container") for element in position_summary_text.find_elements(By.TAG_NAME, "*")):
                inner_positions = (position_summary_text.find_element(By.CLASS_NAME,"pvs-list__container")
                    .find_element(By.XPATH,"*").find_element(By.XPATH,"*").find_element(By.XPATH,"*")
                    .find_elements(By.CLASS_NAME,"pvs-list__paged-list-item"))
            else:
                inner_positions = []
            if len(inner_positions) > 1:
                descriptions = inner_positions
                for description in descriptions:
                    res = description.find_element(By.TAG_NAME,"a").find_elements(By.XPATH,"*")
                    position_title_elem = res[0] if len(res) > 0 else None
                    work_times_elem = res[1] if len(res) > 1 else None
                    location_elem = res[2] if len(res) > 2 else None


                    location = location_elem.find_element(By.XPATH,"*").text if location_elem else None
                    position_title = position_title_elem.find_element(By.XPATH,"*").find_element(By.TAG_NAME,"*").text if position_title_elem else ""
                    work_times = work_times_elem.find_element(By.XPATH,"*").text if work_times_elem else ""
                    times = work_times.split("·")[0].strip() if work_times else ""
                    duration = work_times.split("·")[1].strip() if len(work_times.split("·")) > 1 else None
                    from_date = " ".join(times.split(" ")[:2]) if times else ""
                    to_date = " ".join(times.split(" ")[3:]) if times else ""

                    experience = Experience(
                        position_title=position_title,
                        from_date=from_date,
                        to_date=to_date,
                        duration=duration,
                        location=location,
                        description=description,
                        institution_name=company,
                        linkedin_url=company_linkedin_url
                    )
                    self.add_experience(experience)
            else:
                description = position_summary_text.text if position_summary_text else ""

                experience = Experience(
                    position_title=position_title,
                    from_date=from_date,
                    to_date=to_date,
                    duration=duration,
                    location=location,
                    description=description,
                    institution_name=company,
                    linkedin_url=company_linkedin_url
                )
                self.add_experience(experience)

    def get_educations(self):
        url = os.path.join(self.linkedin_url, "details/education")
        self.driver.get(url)
        self.focus()
        main = self.wait_for_element_to_load(by=By.TAG_NAME, name="main")
        self.scroll_to_half()
        self.scroll_to_bottom()
        main_list = self.wait_for_element_to_load(name="pvs-list__container", base=main)
        for position in main_list.find_elements(By.CLASS_NAME,"pvs-list__paged-list-item"):
            position = position.find_element(By.XPATH,"//div[@data-view-name='profile-component-entity']")
            institution_logo_elem, position_details = position.find_elements(By.XPATH,"*")

            # company elem
            institution_linkedin_url = institution_logo_elem.find_element(By.XPATH,"*").get_attribute("href")

            # position details
            position_details_list = position_details.find_elements(By.XPATH,"*")
            position_summary_details = position_details_list[0] if len(position_details_list) > 0 else None
            position_summary_text = position_details_list[1] if len(position_details_list) > 1 else None
            outer_positions = position_summary_details.find_element(By.XPATH,"*").find_elements(By.XPATH,"*")

            institution_name = outer_positions[0].find_element(By.TAG_NAME,"span").text
            if len(outer_positions) > 1:
                degree = outer_positions[1].find_element(By.TAG_NAME,"span").text
            else:
                degree = None

            if len(outer_positions) > 2:
                times = outer_positions[2].find_element(By.TAG_NAME,"span").text

                if times != "":
                    from_date = times.split(" ")[times.split(" ").index("-")-1] if len(times.split(" "))>3 else times.split(" ")[0]
                    to_date = times.split(" ")[-1]
            else:
                from_date = None
                to_date = None



            description = position_summary_text.text if position_summary_text else ""

            education = Education(
                from_date=from_date,
                to_date=to_date,
                description=description,
                degree=degree,
                institution_name=institution_name,
                linkedin_url=institution_linkedin_url
            )
            self.add_education(education)

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
                    print(f"Found an image in <li>: {img_element.get_attribute('src')}")
                except Exception as e:
                    print("No image found in this <li>.")
            # link_sources = []
            # for li in list_li:
            #     print(333333)
            #     img_src = li.find_element(By.CLASS_NAME, "evi-image lazy-image ember-view").get_attribute("src")
            #     # if li.find_element(By.CLASS_NAME, "evi-image lazy-image ember-view"):
            #     #     img_src = li.find_element(By.CLASS_NAME, "evi-image lazy-image ember-view").get_attribute("src")
            #     #     print(img_src)
            #     #     user_link = li.find_element(By.CLASS_NAME, "optional-action-target-wrapper").get_attribute("href")
            #     #     if "framedphoto" in img_src:
            #     #         link_sources.append(user_link)
            
            # self.may_know = link_sources
            # print(link_sources)
        except Exception as e:
            print(f"An error occurred: {e}")
        
        self.wait(5)
        self.driver.get(self.linkedin_url)
        self.focus()

    def scrape_logged_in(self, close_on_complete=True):
        driver = self.driver
        duration = None

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

    @property
    def company(self):
        if self.experiences:
            return (
                self.experiences[0].institution_name
                if self.experiences[0].institution_name
                else None
            )
        else:
            return None

    @property
    def job_title(self):
        if self.experiences:
            return (
                self.experiences[0].position_title
                if self.experiences[0].position_title
                else None
            )
        else:
            return None

    def __repr__(self):
        return ""
