---
title: PHP-FPM响应用户请求过程
date: 2021-12-03 17:54:37
tags: PHP
---

> 我们发布了非常多的项目，让它在机器上运行。但是你知道PHP-FPM究竟是如何让你的源代码运行并处理大量的用户请求么。

## 响应过程

![](https://vison-blog.oss-cn-beijing.aliyuncs.com/20211203094817.png)

<!--more-->

Nginx和PHP-FPM通过 [Fastcgi 协议](http://www.mit.edu/~yandros/doc/specs/fcgi-spec.html) 进行交流

```
Web browser www.example.com
|
        |
   Transport over HTTP protocol  
|
        |
    http server
 (server nginx / APACHE)            
|
        |
     Configuration analysis    
Route to www.example.com/index.php
|
        |
Fast CGI module loaded with nginx
|
        |
Fast CGI monitors 127.0.0.1:9000 addresses
Through the fast CGI protocol, the request is forwarded to PHP FPM for processing
|
        |
Request reached 127.0.0.1:9000
|
        |
PHP FPM monitoring 127.0.0.1:9000
This can be done through PHP- fpm.conf  Make changes
```

## 并行模式

PHP其实有2种模式来处理并发请求：

- 基于进程
- 基于线程

### 进程模式流程

![](https://vison-blog.oss-cn-beijing.aliyuncs.com/20211203101157.png)

1. 模块初始化: MINIT()

这个环节会初始化一些对象和一些每个请求会用到的信息，这个时候并没有开始接收请求。这段时间可以访问全局变量。

2. 请求初始化: RINIT()

PHP在这个阶段开始处理request，PHP是一种无共享架构，提供了灵活的内存管理方式。`share-nothing architecture`意味着不用担心并发引发的错乱问题。

在此中，如果需要分配动态内存，将使用`Zend内存管理器`。Zend 内存管理器会跟踪你通过它分配的内存，当请求关闭时，如果您忘记这样做，它将尝试释放受请求约束的内存。

3. 请求终止：PRSHUTDOWN()

PHP处理请求结束，此阶段清理请求内存。未来的请求当中不会有当前请求的数据。

此阶段，RSHUTDOWN()的调用时机：

- 来自`register_shutdown_function`注册的方法，用户态的shutdown调用执行完
- 所有的对象析构函数执行完
- PHP输出缓冲flush完毕
- `max_execution_time`触达

4. 请求终止后: PRSHUTDOWN()

此阶段很少被使用。

5. 全局初始化: GINIT()

此钩子在线程模型下会为每个请求都触发一次，但在多进程模型下只触发一次。

全局变量不会被清除在每个请求之后，需要每次进行`RINIT`操作。

6. 全局终止：GSHUTDOWN()

与GINIT一样，多线程模式下每次请求之后都会触发，多进程模式只会执行一次。

所以总体上的执行流程如下：

![](https://vison-blog.oss-cn-beijing.aliyuncs.com/20211203175045.png)

## 参考

1. [https://www.phpinternalsbook.com/php7/extensions_design/php_lifecycle.html](https://www.phpinternalsbook.com/php7/extensions_design/php_lifecycle.html)
