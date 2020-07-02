---
title: PHP生态之自动化测试
date: 2020-07-01 09:58:44
tags: php
---

PHP TESTING FOR EVERYONE

<!--more-->

![](http://img.rc5j.cn/blog20200701101728.png)


在长久的工作经历中，测试大佬常会在你耳旁嘀咕开发要自测要自测。但是实际上开发往往只会关心当前负责的单元功能的正确与否。繁杂的开发任务当中，还要兼顾所有流程的功能运转可能就没那个精力了，或者说这本身就是测试的工作。在远古时代互联网领域工作还没细分到前端、后端、测试、UI的时候，所有一揽子活都只有一个人做，那就是程序员。

**但是如何尽量保证程序返回结果是预期的？** 能否做到每次发布之前自动对程序测试看是否达到预期？
这个时候我们可以引入**自动化测试**。

## 自动化测试范围

- UI测试
- 接口测试
- 单元测试
- 数据测试

其中UI测试和数据测试的自动化可能是最不容易做且效益最小的。这部分可能最好是人为的进行测试效果最好。


在体验了java 的junit之后特别觉得junit的强大,其实PHP也可以做。接下来我们来了解下PHP的测试框架`codeception`

## 安装使用

### install

```
composer require "codeception/codeception" --dev
```

### setup

```
php vendor/bin/codecept bootstrap
```
该命令会初始化配置文件和目录


## codeception单元测试

![](http://img.rc5j.cn/blog20200702143824.png)

codeception的单元测试其实也是基于phpunit之上构建的。phpunit的单元测试用例可以之前在codeception上执行。

### 创建单元测试

```
php vendor/bin/codecept generate:test unit Example
```
执行完会在tests/unit目录里创建测试用例文件 

```php

class ExampleTest extends \Codeception\Test\Unit
{
    /**
     * @var \UnitTester
     */
    protected $tester;

    protected function _before()
    {
    }

    protected function _after()
    {
    }

    // tests
    public function testMe()
    {

    }
}
```

- all public methods with test prefix are tests
- _before method is executed before each test (like setUp in PHPUnit)
- _after method is executed after each test (like tearDown in PHPUnit)



### 运行用例

```
php vendor/bin/codecept run unit ExampleTest
```
运行所有单元测试用例

```
php vendor/bin/codecept run unit
```

```php
class UserTest extends \Codeception\Test\Unit
{
    public function testValidation()
    {
        $user = new User();

        $user->setName(null);
        $this->assertFalse($user->validate(['username']));

        $user->setName('toolooooongnaaaaaaameeee');
        $this->assertFalse($user->validate(['username']));

        $user->setName('davert');
        $this->assertTrue($user->validate(['username']));
    }
}
```