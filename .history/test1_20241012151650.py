from selenium import webdriver
from selenium.webdriver.chrome.options import Options

option = webdriver.ChromeOptions()
option.add_argument('--user-data-dir=/Users/BGZB002/Library/Application Support/Google/Chrome/Default') #加载前面获取的 个人资料路径
driver = webdriver.Chrome(chrome_options=option, executable_path="/usr/local/bin/chromedriver")  #启动Chrome驱动，这里为Linux系统，Windows 和 Mac OS 根据实际路径填写

# 尝试打开一个网页
driver.get("http://www.baidu.com")

# 输出页面标题以确认是否正确打开
print(driver.title)

# 完成后关闭浏览器
driver.quit()