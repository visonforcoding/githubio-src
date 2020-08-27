---
title: glances+influxdb+granfana打造服务器监控系统
date: 2020-08-25 17:56:32
tags: devops
---

![](http://img.rc5j.cn/blog20200825175740.png)

服务监控就是你的眼睛，当你对服务器运行状况一无所知时，你应该感到坐立不安。

<!--more-->

## glances安装

glances是由python编写的，因此可以使用pip直接安装

```
pip3 install glances
```