---
title: 非正式对比PHP&JAVA
date: 2020-09-25 14:10:36
tags:
---

## 主机环境

- CPU 2核
- 内存 4G
- CentOS 8

## PHP 环境

- PHP 7.2.33
- nginx/1.14.1

```
ab -n3000 -c10 http://php-demo.test.cn/index.php

```

```json
{
  "ret": 0
}

```



| PHP-FPM个数 | RPS    |
| ----------- | ------ |
| 2           | 100.19 |
| 5           | 85.77  |
| 10          | 94.44  |
| 20          | 93.36  |

## java spring-boot

QPS 94.12