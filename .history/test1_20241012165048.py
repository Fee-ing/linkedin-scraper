from selenium import webdriver

driver = webdriver.Chrome()  #启动Chrome驱动，这里为Linux系统，Windows 和 Mac OS 根据实际路径填写

# 尝试打开一个网页
driver.get("http://www.baidu.com")
