from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import coloredlogs
import logging
import time
import psutil


class Driver:

    isClosed = False  # 浏览器是否关闭
    logger = None    
    autoClose = True  # 是否自动关闭webdriver进程

    def __init__(self, wait=False, loggerConfig=None):
        """[自动化测试浏览器驱动]

        Keyword Arguments:
            wait {bool} -- [是否启用隐式等待] (default: {False})
        """
        self.browser = webdriver.Chrome()
        # self.browser.launch_app(111331)
        self.start_time = time.time()
        self.logger = self._Driver__init_color_log(loggerConfig)
        self.performance_data = {'times': [], 'uss': [], 'cpu': []}
        if wait:
            self.logger.info('启用隐式等待..')
            self.browser.implicitly_wait(30)

    def __del__(self):
        # 测试结束 关闭掉 浏览器
        if(self.autoClose):
            self.close_browser()
        # self.close_webdriver()

    def setAutoClose(self, auto=False):
        self.autoClose = auto

    def open_browser(self, url):
        """
        Do something for browser
        :return: webdriver
        """
        # 窗口最大化
        self.browser.maximize_window()
        # 打开地址链接
        self.browser.get(url)
        return self.browser

    def close_browser(self):
        """
        quit browser
        :return:
        """
        if self.isClosed != True:
            end_time = time.time()
            speed_time = end_time - self.start_time
            self.logger.info(
                '测试进程中止,开始时间%s,总耗时%.2fs' %
                (time.strftime("%Y-%m-%d %H:%M:%S",
                               time.localtime(self.start_time)), speed_time))
            # self.browser.quit()  # 发现有bug 并不会关闭掉 webdriver 进程,而且之后代码不会执行
            self.browser.close()
            self.isClosed = True
            webdriver_pid = self.browser.service.process.pid
            ps = psutil.Process(webdriver_pid)
            self.logger.info('关闭webdriver进程%d' % webdriver_pid)
            ps.kill()

    def get_page_pid(self, page_num=1):
        """[获取启动页面的进程id,非官方方法,不一定正确。
            原理:假设chrome主进程启动子进程是有顺序的,那么打开的页面进程在第4个启动]

        Returns:
            [type] -- [description]
        """
        webdriver_pid = self.browser.service.process.pid
        ps = psutil.Process(webdriver_pid)
        ps_children = ps.children(True)
        return ps_children[3 + page_num - 1].pid

    def set_page_performance(self, times, page_num=1):
        page_pid = self.get_page_pid(page_num)
        ps = psutil.Process(page_pid)
        memory_info = ps.memory_full_info()
        ps.cpu_percent(interval=1)
        cpu = ps.cpu_percent(interval=None)
        uss = memory_info.uss
        self.performance_data['times'].append(times)
        self.performance_data['uss'].append(uss / 1024 / 1024)
        self.performance_data['cpu'].append(cpu)  # 获取有问题 暂不能用

    def __init_color_log(self, loggerConfig):
        """[启用彩色日志]

        Returns:
            [type] -- [description]
        """
        # Create a logger object.
        logger = logging.getLogger(__name__)

        # By default the install() function installs a handler on the root logger,
        # this means that log messages from your code and log messages from the
        # libraries that you use will all show up on the terminal.
        if loggerConfig:
            if 'level' in loggerConfig:
                coloredlogs.install(level=loggerConfig['level'], logger=logger)
        else:
            coloredlogs.install(level='DEBUG', logger=logger)

        # If you don't want to see log messages from libraries, you can pass a
        # specific logger object to the install() function. In this case only log
        # messages originating from that logger will show up on the terminal.
        self.logger = logger
        return logger

    def search_element_by_xpath(self, xpath):
        """[通过xpath寻找元素,直到寻找到为止。本身driver有提供wait方法，可以考虑重构替换]

        Arguments:
            xpath {[type]} -- [description]

        Returns:
            [type] -- [description]
        """
        while True:
            try:
                element = self.browser.find_element_by_xpath(xpath)
            except:
                self.logger.warning('%s未找到元素,继续寻找....' % xpath)
                continue
            else:
                return element

    def click_element(self, xpath):

        try:
            wait = WebDriverWait(self.browser, 30)
            element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        except:
            self.browser.save_screenshot(
                './screenshot/%s-%s.png' %
                (__name__, time.strftime("%Y%m%d%H%M%S")))
            self.logger.error('等待超时.....')
            time.sleep(100)
            # 路径不对居然不会报错
            raise
        # 仍然还有机会 元素被覆盖而不能被点击 只能采用 轮询重试了
        while True:
            try:
                element.click()
            except BaseException as e:
                time.sleep(2)  # 这里还是睡眠一秒进行点击 不然脚本cpu占用厉害
                self.logger.warning('%s元素无法点击,继续点击....' % xpath)
                self.logger.warning('捕获异常:', e)
                continue
            else:
                break
