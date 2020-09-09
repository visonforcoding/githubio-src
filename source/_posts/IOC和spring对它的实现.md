---
title: IOC和spring对它的实现
date: 2020-09-09 21:10:50
tags:  java
---


![](http://img.rc5j.cn/blog20200909211506.png)

<!--more-->

## IOS概述

https://www.cnblogs.com/DebugLZQ/archive/2013/06/05/3107957.html 这篇文章已经讲的很好。

我做下总结。

- 面向对象编程的世界，程序之间的耦合不可避免，而且会使得系统变得难以维护
- IOC就是为了降低这种耦合
- IOS也不是完美的，所有事情都有优缺点

![](http://img.rc5j.cn/blog20200909212010.png)

IOC就是为了把原本互相之间有耦合在一起，会造成牵一发而动全身的现象。通过容器解耦开,各自能独立运作。

![](http://img.rc5j.cn/blog20200909212051.png)


## spring的实现

org.springframework.beans 和org.springframework.context 包是Spring Framework 的IoC 容器的基础。



