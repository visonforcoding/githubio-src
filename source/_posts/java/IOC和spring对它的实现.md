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


BeanFactory 接口提供高级的配置机制，可以管理任意类型的对象。

- ApplicationContext 是BeanFactory 的子接口。
- 它添加了和Spring 的AOP 特性很简便的整合；
- 消息资源处理（用于国际化i18n），事件发布；
- 应用层特定的上下文， 比如用于Web 应用程序的WebApplicationContext。

总之，BeanFactory 提供了配置框架和基本功能，而ApplicationContext 添加了更多企业级开发特定的功能。

