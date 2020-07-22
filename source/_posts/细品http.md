---
title: 细品http
date: 2020-07-21 18:32:08
tags: 计算机基础
---

![](http://img.rc5j.cn/blog20200721183924.png)

<!--more-->

## HTTP标头headers

### Content-Type

`Content-Type`实体头用于指示所述媒体类型的资源的。

作为Response，Content-Type标头告诉客户端返回的内容的内容类型实际上是什么。在某些情况下，浏览器将执行MIME嗅探，并且不一定遵循此标头的值；为防止出现这种情况，X-Content-Type-Options可以将标头设置为nosniff。

在Request（例如POST或PUT）中，客户端告诉服务器实际发送的数据类型。