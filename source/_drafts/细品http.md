---
title: 细品http
date: 2020-07-21 18:32:08
tags: 计算机基础
---

![](https://vison-blog.oss-cn-beijing.aliyuncs.com/20210430142400.png)

<!--more-->

## HTTP标头headers

### Content-Type

`Content-Type`实体头用于指示所述媒体类型的资源的。

作为Response，Content-Type标头告诉客户端返回的内容的内容类型实际上是什么。在某些情况下，浏览器将执行MIME嗅探，并且不一定遵循此标头的值；为防止出现这种情况，X-Content-Type-Options可以将标头设置为nosniff。

在Request（例如POST或PUT）中，客户端告诉服务器实际发送的数据类型。

## 304与缓存




### Http协议中的cache机制

- 直接本地缓存
- 304校验缓存

### 直接使用本地缓存

![](http://img.rc5j.cn/blog20200914114534.png)


#### http 1.1的 Cache-Control 


Response中的 Cache-Control 头指示浏览器按何种规则缓存该资源，例：


Cache-Control: public, max-age=31536000
该header是复合类型，常见参数的含义：

- public : 用户浏览器和中间proxy都会cache
- private : 只有用户端会cache
- max-age=xxx : 设置cache的最大存活时间，单位s
- no-store : 不要缓存
- no-cache : 同上，但是浏览器的支持可能不一致，最好两个一起用

### 304校验缓存

![](http://img.rc5j.cn/blog20200914114231.png)


