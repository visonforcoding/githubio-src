---
title: [原创]Selenium自动化测试在页面web性能测试应有的尝试
date: 2020-05-07 23:26:14
tags: python
---

对于web测试，我们通常在做的测试都是人工的功能测试。那么少见的自动化测试到底适用哪些场景呢？

<!-- more -->

# 用python进行web自动化测试

> 前段时间，在客服信息系统进入用户体验阶段时发现内存存在泄露问题。我们花了很多时间去排查原因。经过各种可能的优化方案，结果发现没有实质性的效果，于是我们决定重构。但是如何保证重构方案的可行呢？于是我们用到了python+Selenium

## 为什么会用到web自动化测试

### web自动化测试适用场景


对于web测试，我们通常在做的测试都是人工的功能测试。那么少见的自动化测试到底适用哪些场景呢？

- 回归测试。每一次应用发布，都伴随着一次回归测试。对于重复性的工作，机器显然更适合。
- 兼容性测试。不管是Web测试，还是App测试，兼容性测试都是必不可少的一环。以Web测试为例，同样的测试用例，需要在不同的浏览器上分别运行一遍，这对测试人员而言不可谓不是一种折磨。
- 大规模测试。如果一次测试涉及的测试用例过多（比如100+），功能测试难免会有遗漏或者重复，而自动化测试可以轻松确保一个不少，一个也不多。
- 性能测试

### 弊端

万事皆有利弊，机器的自动化测试没有广泛应用肯定是有原因的。

- 不低的技术门槛。不论是使用哪种自动化测试框架，对于测试人员而言，都存在一定的技术门槛，一般至少需要学习并掌握一门编程语言。
可观的开发成本和维护成本。跟任何程序一样，无论是编写自动化测试脚本，还是在需求变化时修改脚本，都需要花费大量的时间。
- 需求要稳定。自动化测试的前提是测试用例要稳定，而测试用例稳定的前提是需求要稳定。对于临时的或者说一次性的需求，自动化测试往往是得不偿失的。
- 应用周期长。应用的生命周期越长，自动化测试节省的时间越多，带来的价值也越大。


### 性能测试

随着web前端技术发展更新越来越迅猛的态势，前端技术和框架层出不穷。但往往我们会在短期内高估技术带来的影响。

![](http://img.rc5j.cn/blog20190524140107.png)


所以对于任何一个新的事物，我们采取保守的态度对待可能会少跌入一些**幻灭的低谷期**。对于新技术做充分的评估测试，可能会让我们少踩一些坑。当然往往这话，都是在事后才会提出来。

为什么可以用自动化测试做性能测试？
网上似乎都没有这种先例。我总结以下几个原因：

1. 脚本能强有规律地重复执行操作，而开发或测试自己做这个工作会很繁琐而且出了一步差错就得重来
2. 脚本能将执行操作和数据记录结合起来。而人类执行一次数据记录和动作执行也许没问题，但重复500次或更多而无差错那就困难了。


## web自动化测试方法

- python+Selenium 跨浏览器支持
- puppeteer 专注于chrome
- airtest 跨平台，安卓、ios、web，web还是用的Selenium

## 测试结果

![](http://img.rc5j.cn/blog20190514101858.png)

执行脚本

![](http://img.rc5j.cn/blog20190524162047.gif)

脚本运行情况，浏览器在自动进行操作

![](http://img.rc5j.cn/blog20190524162725.png)

得出统计结果。我们模拟用户的某个最频繁的操作，发现采用新的方案后内存会在短时间内有效回收。整体上，页面内存会趋于稳定的态势。



## 遇到的问题

### 动态的ggcode

```python
 ggcode = prompt("输入谷歌码: ")
```

由于登录用的谷歌码是动态的，所以这里只能每次输入进行填充。这里我们引入prompt_toolkit进行终端的交互


### 获取元素

如今的前端项目，由于使用的是数据驱动dom，不是传统的jquery操作，现在基本看不到id class等进行元素定位。现在最方便的做法只能是通过xpath寻找元素。

![](http://img.rc5j.cn/blog20190524180042.png)

```

xpath = '//*[@id="app"]/div/div[2]/div[1]'
element = self.browser.find_element_by_xpath(
                    xpath)
```

**由于不是固定id，页面一旦改变xpath很有可能改变，会导致元素找不到。**



### webdriver进程不退出

在使用过程当中发现提供的`quit()` 方法并不能让进程退出，所以只能自己将进程kill掉。

```python
def close_browser(self):
```

### 点击

在进行按钮点击的时候，经常会因为页面未加载完等原因导致无法点击。结果就是可能会抛出异常。对于这种情况webdriver本身有提供wait等待。

```python
wait = WebDriverWait(self.browser, 30)
            element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
```

`WebDriverWait` 需要设置一个等待时长，不可能无限等待


还有些情况下，是由于需要下拉滚动条才能进行点击。这种情况可以考虑执行js进行点击。

```python
js_click_next_page = 'document.querySelector("body > div.worker-order-search-list > div.content-wrapper > section > ul > li.ivu-page-next").click()'
                browser.execute_script(js_click_next_page)
```
**使用webdriver.click还是用js点击？**
>When Should You Use JavaScript for Clicking?
If you are using Selenium for testing an application, my answer to this question is "almost never". By and large, your Selenium test should reproduce what a user would do with the browser. Taking the example of the drop down menu: a test should click on the button that brings up the drop down first, and then click on the menu item. If there is a problem with the GUI because the button is invisible, or the button fails to show the menu items, or something similar, then your test will fail and you'll have detected the bug. If you use JavaScript to click around, you won't be able to detect these bugs through automated testing.

**总之还是看你的使用目的，如果自动化测试的目的倾向于测试页面功能。那么建议使用webdriver.click。如果是为了测试性能，那可以进行js点击了。**

## 获取页面内存

浏览器的任务管理器可以很容易的看到页面的内存、cpu、网络情况，但是如何获取到记录并统计呢？

答案是，很可惜现在还没找到。如果有官方办法，请告诉我。

我走了一个其他途径获取，从操作系统层面获取进程。获取一个进程得内存占用是一个简单的事，但是如何知道某个页面的进程id呢。很遗憾的是，webdriver同样没有接口方法提供。于是我只能从webdriver子进程入手，看有没有信息能与page关联上。很遗憾的事，单单从子进程名看与页面毫无关联。所以。。最后，我只能做一个假设，假设浏览器启动类似linux启动。启动的程序是有先后关系的。

```python
def get_page_pid(self, page_num=1):
        """[获取启动页面的进程id,非官方方法,不一定正确。
            原理:假设chrome主进程启动子进程是有顺序的,那么打开的页面进程在第4个开始启动]

        Returns:
            [type] -- [description]
        """
        webdriver_pid = self.browser.service.process.pid
        ps = psutil.Process(webdriver_pid)
        ps_children = ps.children(True)
        return ps_children[3+page_num-1].pid
```

这是一种对项目无侵入的做法，你不需要改动项目代码，就可以对浏览器页面内存进行统计。还有其他做法，可以对项目进行增加内存上报进行统计。但这样的做法同样有弊端：

1. 需要动被测项目，对项目干扰
2. 增加工作量，不光是上报还包括接收上报接口
3. 如果是多iframe页签方式，统计聚合上报将非常繁琐

需要注意的是，统计页面进程方法。**得到的数据是整个页面进程所占用的内存，并非页面js占用内存。**

## 统计

在统计上，我使用了chartify+pandas,只要传入数据就能快捷地生成图表

```python
def chartArea(self, data, x_column, y_column):
        """[绘制区域图]

        Arguments:
            data {[dict]} -- [数据矩阵,拿去构建pandas dataFrame]
            x_column {[type]} -- [x轴字段]
            y_column {[type]} -- [y轴字段]
        """
        data_frame = pd.DataFrame(data)
        print(data_frame)
        self.ch.plot.area(data_frame=data_frame,
                          x_column=x_column, y_column=y_column, stacked=True)

    def show(self, show_type='html'):
        self.ch.save('./output/%s-%s.png' %
                     (self.subtitle, time.strftime("%Y%m%d%H%M%S")), 'png')

```


## 总结

正如前面所说，web自动化测试没有广泛应用肯定是有原因的。但是做为前端问题的论证还是有很大意义。

比如，页面占用内存限制是多少？我找了很多资料没有找到(官方的才可信)。

通过测试，我得到的结果是，chrome 对单页面js 内存有限制2G,对页面进程内存无限制。你一个页面进程甚至可以跑到20G。

python+Selenium 使用起来很简单，感兴趣又有需要的话，不妨一试。


## 附加
