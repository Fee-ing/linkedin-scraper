from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# 设置webdriver路径
url1 = "http://www.baidu.com"
url2 = "https://www.bing.com/?mkt=zh-CN"

# 创建一个新的Chrome浏览器实例
driver = webdriver.Chrome()

# 使用get方法打开网页
driver.get(url1)

time.sleep(2)

# 使用JavaScript来打开新的标签页并加载URL
driver.execute_script("window.open('');")
driver.switch_to.window(driver.window_handles[1])
driver.get(url2)

# 停留一段时间以供观察
time.sleep(2)

driver.close()

driver.switch_to.window(driver.window_handles[0])

time.sleep(2)

# 关闭浏览器
driver.quit()