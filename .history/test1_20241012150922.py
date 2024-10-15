from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# 创建 ChromeOptions 实例
options = Options()

# 设置需要的能力
capabilities = DesiredCapabilities.CHROME.copy()
capabilities['acceptInsecureCerts'] = True  # 示例能力，根据需要添加

# 指定 chromedriver 的路径
service = Service(executable_path="/usr/local/bin/chromedriver")

# 初始化 Chrome WebDriver
driver = webdriver.Chrome(service=service, options=options, desired_capabilities=capabilities)

# 尝试打开一个网页
driver.get("http://www.baidu.com")

# 输出页面标题以确认是否正确打开
print(driver.title)

# 完成后关闭浏览器
driver.quit()