---
title: 学习编写php拓展
date: 2021-07-07 15:10:27
tags: php
---

## 目的

**为什么要学习编写php拓展？**

1.目前市面上有数据库或中间件无php驱动
2.有自己的公共组件或函数,虽然可以使用composer，为了提升性能替代composer包
3.为了学习php内核原理或其他拓展的内部实现原理


## hello,world


**1.源码下载**

```shell
wget https://www.php.net/distributions/php-7.2.19.tar.bz2
tar -xvf php-7.2.19.tar.bz2
```


**2.增加函数声明**


```shell
vim php_vison.h
# 在其中增加 PHP_FUNCTION(vison_print);
vim vison.c

# 将如下代码中的PHP_FE和PHP_FE_END中加入下面代码（这的代码是将函数指针注册到Zend引擎）
PHP_FE(vison_print,  NULL)

```


**3.函数定义**

```shell
vim vison.c
在最后加上创建执行方法vison_print
```

```c
PHP_FUNCTION(vison_print)
{
  php_printf("Hello vison!\n");
  RETURN_TRUE;

}
```


**4.编译**

```
phpize

./configure && make && make install

# 然后将生成的vison.so放入配置

vim /etc/php.ini

extension=vison.so

#然后输入php -m查看配置

```


**4.验证**

```shell
php -r "vison_print();"
```


