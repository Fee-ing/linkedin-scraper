from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# 指定 chromedriver 的路径
service = Service(executable_path="/path/to/chromedriver")

# 初始化 Chrome WebDriver
capabilities = DesiredCapabilities.CHROME.copy()
driver = webdriver.Chrome(service=service, desired_capabilities=capabilities)

# 尝试打开一个网页
driver.get("http://www.baidu.com")

# 输出页面标题以确认是否正确打开
print(driver.title)

# 完成后关闭浏览器
driver.quit()