---
title: 用phpunit进行单元测试
date: 2021-07-23 09:48:24
tags: php
---

最近读了一本书《clean code》。深有感悟，感觉非常接底气，讲到了日常编码中真正遇到的困扰。大致我总结下就是要做几件事：

- 重构，定期重构，保持重构
- clean code,编写整洁、易维护的代码
- 单元测试

本篇我们讲下如何利用phpunit进行单元测试

<!--more-->


## 安装

这里主要说明下安装的版本问题，最新版phpunit-latest目前依赖php7.4. 但是我们线上版本仍然是php7.2,因此我们需要安装旧的版本.

[https://phpunit.de/announcements/phpunit-8.html](https://phpunit.de/announcements/phpunit-8.html)  从这个链接能找到phpunit-8。

安装的方式有2种，`PHAR` 和 `composer`，两种方式都可以全局安装。

[https://phpunit.readthedocs.io/zh_CN/latest/installation.html#installation-requirements](https://phpunit.readthedocs.io/zh_CN/latest/installation.html#installation-requirements) 官方的教程文档里不推荐进行全局安装。

> 请注意，并不推荐全局安装 PHPUnit，比如说放在 /usr/bin/phpunit 或 /usr/local/bin/phpunit。
相反，PHPUnit 应该作为项目本地依赖项进行管理。

但是我还是选择全局安装，因为不想将本地太多依赖。

## 使用


### IDE提示

```php
<?php

declare(strict_types=1);

use PHPUnit\Framework\TestCase;

final class RedisCacheTest extends TestCase
{

    public function testSet(): void
    {
       $res =  \Hll\Cache\Cache::set('foo', date('Y-m-d H:i:s'),10);
       $this->assertTrue($res);
    }

}
```

这是我的一个测试用例脚本，测试脚本类需要继承`TestCase`.

由于我的安装方式并不是本地项目安装，所以在ide不会提示TestCase的相关方法。这对于来说是不能容忍的，不过好在IDE能额外的配置引入项目外的文件进行提示。

![](https://vison-blog.oss-cn-beijing.aliyuncs.com/20210723100857.png)

### 工程目录

再来看看工程目录结构

![](https://vison-blog.oss-cn-beijing.aliyuncs.com/20210723101019.png)

在我编写的一个`cache`组件库中

- `src`作为源代码目录
- `tests`作为测试用例目录
- `bootstrap.php`是phpunit的启动加载文件，用于做些全局的初始化动作，比如加载autoload.

### 执行测试

```shell
phpunit --bootstrap tests/bootstrap.php --verbose tests/case 
```
该命令是执行测试 tests/case下的所有测试用例文件，当然你也可以具体到只执行单个文件。

`--bootstrap`

加载启动文件

`--colors`

彩色输出

`--debug`

输出调试信息，例如当一个测试开始执行时输出其名称。

`--testtox`

以`testtox`格式显示测试结果

![](https://vison-blog.oss-cn-beijing.aliyuncs.com/20210723102912.png)

`--configuration`、`-c`

从 XML 文件中读取配置信息。

如果`phpunit.xml` 或 `phpunit.xml.dist`（按此顺序）存在于当前工作目录并且未使用 `--configuration`，将自动从此文件中读取配置。