from linkedin_scraper import Person, actions
from selenium import webdriver
driver = webdriver.Chrome()

email = "some-email@email.address"
password = "password123"
cookie = "AQEDAVNefkgFTRomAAABkn5FZ6oAAAGSolHrqlYAoZXdC8PjeSfFJQPhQMj74Yivzowknyn9VXqFr3oaocZN8enPTQfHHNCcSMw0wCqLzHxydPV_7KEcf6gdU0223f6swHCzp5CfimGV8zzeXHkCB0Kl"

actions._login_with_cookie(driver, cookie) # if email and password isnt given, it'll prompt in terminal
person = Person("https://www.linkedin.com/in/klaudia-szkopiak-477151308/", driver=driver)
print(person)