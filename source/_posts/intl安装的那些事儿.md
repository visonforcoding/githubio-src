---
title: intl安装的那些事儿
date: 2020-06-19 10:41:25
tags: php
---

被intl折磨的还不够么

<!--more-->

To build the extension you need to install the » ICU library, version 4.0.0 or newer is required. As of PHP 7.4.0 ICU 50.1 or newer is required.

This extension is bundled with PHP as of PHP version 5.3.0. Alternatively, the PECL version of this extension may be used with all PHP versions greater than 5.2.0 (5.2.4+ recommended).

## ICU安装

现在icu已被放到github，下载建议直接从github下载源码到本地。

https://github.com/unicode-org/icu/releases/tag/release-60-3

下载后编译安装

## 拓展安装

```shell
pecl install intl
```

总会遇到问题,建议用phpize 源码安装。

```
./configure  --enable-intl   --with-php-config=/usr/local/php7/bin/php-config
make
make install
```

重启php-fpm
