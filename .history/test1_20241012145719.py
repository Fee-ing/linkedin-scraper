from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# 指定 chromedriver 的路径
service = Service(executable_path="/path/to/chromedriver")

# 初始化 Chrome WebDriver
driver = webdriver.Chrome(service=service)

# 导航到一个网页
driver.get("http://baidu.com")

# 完成后关闭浏览器
driver.quit()