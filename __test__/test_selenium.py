import time

from selenium import webdriver

wd = webdriver.Chrome('/JAVA_BIGDATA/chromedriver_win32/chromedriver.exe')
wd.get('http://google.com')

time.sleep(5)

html = wd.page_source
print(html)

wd.quit()