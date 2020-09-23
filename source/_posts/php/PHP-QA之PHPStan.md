---
title: PHP QA
date: 2020-09-17 20:44:41
tags: PHP
---

![](http://img.rc5j.cn/blog20200917210020.png)

写在前面，工作7年，PHP也写了7年了。期间也写一些java和python，也对各语言的特点有一些自己的体会。
这次咱们聊聊QA之余也来聊聊PHP语言本身。

<!--more-->

来到`PHPStan`的官网，我看到了一段话。

> I really like how much productivity a web developer gains by switching from compiled languages like Java or C# to an interpreted one like PHP. Aside from the dead simple execution model (start, handle one request, and die) and a much shorter feedback loop (no need to wait for the compiler), there’s a healthy ecosystem of open-source frameworks and libraries to help developers with their everyday tasks. Because of these reasons, PHP is the most popular language for web development by far.

大意是作者很乐意看到web开发者们从C#或Java这些编译性语言里切换到解释语言。除了简单的执行模型（启动，处理一个请求和终止）和较短的反馈周期（无需等待编译）之外，还有一个健康的开源框架和库生态系统可帮助开发人员完成日常工作任务。由于这些原因，PHP是迄今为止最流行的Web开发语言。

这篇文章是作者2016年12月4日写的，说实话对于`PHP是迄今为止最流行的Web开发语言`这句话我已经开始怀疑了。至少在最近这些年，在国内PHP的市场已经不那么好了。并且我也在趋向从解释性语言向编译语言切换了。但是其中对于解释性语言的优势描述我是非常赞同的，这也是它宝贵的优势。

- 简单的执行模型
- 较短的反馈周期

## QA之PHPStan

言归正传，继续PHPStan

### 安装

```
composer require --dev phpstan/phpstan
```

### 运行

```
vendor/bin/phpstan analyse src tests
```

## PHPmd

```
~/vendor/bin/phpmd src/Service/OrderService.php text codesize,unusedcode,naming
```


