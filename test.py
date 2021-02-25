from webdriver import Driver
import time
import os
import logging

driver = Driver()
driver.setAutoClose()
url = "https://www.cnblogs.com/"
smsLoginUrl = "https://account.cnblogs.com/signin?returnUrl=https:%2F%2Fwww.cnblogs.com%2F#sms"
driver.open_browser(smsLoginUrl)
phoneEle = driver.browser.find_element_by_id("mat-input-1")
phoneEle.send_keys("18316629973")
driver.click_element('//*[@id="mat-tab-content-0-1"]/div/div/app-verification-code-input/mat-form-field/div/div[1]/div[4]/button/span[1]')
#手动登录
time.sleep(60)

# #点击编辑
driver.click_element('//*[@id="navbar_login_status"]/a[2]')
workDir = "./source/_posts"
for dirpath, dirnames, filenames in os.walk(workDir):
    driver.logger.info('读取目录:%s' % (dirpath))
    for filename in filenames:
        addNewEle = driver.click_element('/html/body/cnb-root/cnb-layout/div[2]/div[3]/div[1]/cnb-sidebar[1]/div/ul/li[1]/a')
        driver.logger.info('读取文件:%s' % (filename))
        f = open(dirpath+"/"+filename)
        titleEle = driver.search_element_by_xpath('//*[@id="post-title"]')
        lines = f.readlines()
        titleLine = lines[1]
        title = titleLine[6:]
        titleEle.send_keys(title)
        body = "".join(lines[5:]).replace("<!--more-->","")
        bodyEle = driver.search_element_by_xpath('//*[@id="md-editor"]')
        bodyEle.send_keys(body)
        driver.click_element('/html/body/cnb-root/cnb-layout/div[2]/div[3]/div[2]/div/cnb-spinner/div/cnb-post-editing-v2/cnb-post-editor/div[3]/cnb-spinner/div/cnb-submit-buttons/button[1]')
        f.close()

driver.close_browser()
