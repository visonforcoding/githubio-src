from webdriver import Driver
import time
import os
import logging
import re
import hashlib


logfile = './post.log'

def CalcSha1(filepath):
    with open(filepath,'rb') as f:
        sha1obj = hashlib.sha1()
        sha1obj.update(f.read())
        hash = sha1obj.hexdigest()
        print(hash)
        return hash

def logPost(filepath):
    f = open(logfile,'a')
    filehash = CalcSha1(filepath)
    f.write(filehash+'\n')
    f.close()

def deEmojify(text):
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'',text)

driver = Driver(headless=True)
driver.setAutoClose()
url = "https://www.cnblogs.com/"
smsLoginUrl = "https://account.cnblogs.com/signin?returnUrl=https:%2F%2Fwww.cnblogs.com%2F#sms"
driver.open_browser(smsLoginUrl)
# phoneEle = driver.browser.find_element_by_id("mat-input-1")
# phoneEle.send_keys("18316629973")
# driver.click_element('//*[@id="mat-tab-content-0-1"]/div/div/app-verification-code-input/mat-form-field/div/div[1]/div[4]/button/span[1]')
#手动登录
time.sleep(35)

# #点击编辑
driver.click_element('//*[@id="navbar_login_status"]/a[2]')
workDir = "./source/_posts"
for dirpath, dirnames, filenames in os.walk(workDir):
    driver.logger.info('读取目录:%s' % (dirpath))
    for filename in filenames:
        addNewEle = driver.click_element('/html/body/cnb-root/cnb-layout/div[2]/div[3]/div[1]/cnb-sidebar[1]/div/ul/li[1]/a')
        time.sleep(1)
        driver.logger.info('读取文件:%s' % (filename))
        f = open(dirpath+"/"+filename)
        lines = f.readlines()
        titleLine = lines[1]
        title = titleLine[6:]
        print(title)
        driver.input('//*[@id="post-title"]',title)
        body = "".join(lines[5:]).replace("<!--more-->","")
        body = deEmojify(body)
        driver.input('//*[@id="md-editor"]',body)
        driver.scrollToBootom()
        time.sleep(1)
        driver.click_element('/html/body/cnb-root/cnb-layout/div[2]/div[3]/div[2]/div/cnb-spinner/div/cnb-post-editing-v2/cnb-post-editor/div[3]/cnb-spinner/div/cnb-submit-buttons/button[2]')
        time.sleep(3)
        f.close()
        logPost(dirpath+"/"+filename)

driver.close_browser()
