from webdriver import Driver
import time
import os
import logging

driver = Driver()
driver.setAutoClose()
url = "https://www.cnblogs.com/"
driver.open_browser(url)

driver.scrollToBootom()