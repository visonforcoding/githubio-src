---
title: log4j使用指南
tags: java
---

对于刚开始接触java的人来说，用什么来打日志似乎快被java的这么多概念搞懵了。log4j、log4j2、slf4j、logback?!!

![](https://vison-blog.oss-cn-beijing.aliyuncs.com/20201221143621.png)

<!--more-->


## log4j

Apache Log4j 是一个非常古老的日志框架，并且是多年来最受欢迎的日志框架。 它引入了现代日志框架仍在使用的基本概念，如分层日志级别和记录器。

2015 年 8 月 5 日，该项目管理委员会宣布 Log4j 1.x 已达到使用寿命。 建议用户使用 Log4j 1 升级到 Apache 
Log4j 2。
## log4j2

Apache Log4j 2是对 Log4j 的升级，它比其前身 Log4j 1.x 提供了重大改进，并提供了 Logback 中可用的许多改进，同时修复了 Logback 架构中的一些固有问题。

与 Logback 一样，Log4j2 提供对 SLF4J 的支持，自动重新加载日志配置，并支持高级过滤选项。 除了这些功能外，它还允许基于 lambda 表达式对日志语句进行延迟评估，为低延迟系统提供异步记录器，并提供无垃圾模式以避免由垃圾收集器操作引起的任何延迟。

所有这些功能使 Log4j2 成为这三个日志框架中最先进和最快的。

## Logback
logback 是由 log4j 创始人设计的又一个开源日志组件，作为流行的 log4j 项目的后续版本，从而替代 log4j。

Logback 的体系结构足够通用，以便在不同情况下应用。 目前，logback 分为三个模块：logback-core，logback-classic和logback-access。

logback-core：模块为其他两个模块的基础。
logback-classic：模块可以被看做是log4j的改进版本。此外，logback-classic 本身实现了 SLF4J API，因此可以在 logback 和其他日志框架（如 log4j 或 java.util.logging（JUL））之间来回切换。
logback-access：模块与 Servlet 容器（如 Tomcat 和 Jetty）集成，以提供 HTTP 访问日志功能。

![](https://vison-blog.oss-cn-beijing.aliyuncs.com/20201221143239.png)

