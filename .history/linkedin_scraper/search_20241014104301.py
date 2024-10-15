from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from .objects import Scraper
import os
import random

class Search(Scraper):

  def __init__(
        self,
        keyword=None,
        driver=None,
        get=True,
        scrape=True,
    ):
        self.keyword = keyword
        