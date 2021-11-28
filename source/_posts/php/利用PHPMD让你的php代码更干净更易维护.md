---
title: 利用PHPMD让你的php代码更干净更易维护
date: 2021-07-27 14:01:44
tags: PHP
---

PHPMD - PHP Mess Detector

等价于java工具PMD，能够对php 源代码进行如下问题检测：

- 可能的bug
- 欠佳的代码
- 过于复杂的表达式
- 未使用的方法、变量、参数、属性

最新版本发布于 2021/05/11

<!--more-->

[https://phpmd.org/about.html](https://phpmd.org/about.html)

## 基本使用

```shell
phpmd /path/to/source text codesize
```

- 第一个参数 要检测的代码地址
-  第二个参数指定输出检测结果的格式
-  第三个参数是指定的规则集

## 规则集合

- `Clean Code`: 一些包含clean code的规则集合，包括面向对象设计的 SOLID（单一功能、开闭原则、里氏替换、接口隔离以及依赖反转）原则。
- `Code Size` : 有关代码大小的相关问题，例如行数等
- `Controversial` : 具有争议的规则，可以不参考此规则
- `Design` ： 设计规则，包含类依赖数量等等
- `Naming`: 命名规则
- `Unused Code`: 未使用代码规则

关于`clean code` 有一本书名就叫 << Clean Code >>,个人读下来感受颇深。 

这里主要介绍一些我认为非常有必要注意的规则

## Clean Code

### BooleanArgumentFlag

布尔标志参数违反单一责任原则（SRP）,可以将此类方法一拆为二。

```PHP
class Foo {
    public function drink($thirsty = true) {
        if($thirsty){
            // 喝2杯
        }else{
            // 喝一杯
        }
    }
}
```


```php
class Foo {
    public function drinkThirsty() {
        
            // 喝2杯
        
    }
    
      public function drinkUnThirsty() {
       
            // 喝2杯
        
    }
}
```

### ElseExpression

```php
class Foo
{
    public function bar($flag)
    {
        if ($flag) {
            // one branch
        } else {
            // another branch
        }
    }
}
```

像这样的if else的表达式其实是没必要的，可通过三元表达式、拆分方法或者可能的情况下先return来规避这类问题，以将代码简单或增加可读性。

```php
class Foo
{
    public function bar($flag)
    {
        if ($flag) {
            // one branch
            return
        } 
        // another branch
        
    }
}
```

## Code Size

### CyclomaticComplexity

圈复杂度，用来衡量代码复杂度的一个计算规则。复杂度越高代表代码可读性、可维护性越差，易错性更高、集成测试更难。


![](https://vison-blog.oss-cn-beijing.aliyuncs.com/20210727111045.png)



#### 点边计算法

![](https://vison-blog.oss-cn-beijing.aliyuncs.com/20210727110713.png)

上述表达式的圈复杂度为 e = 10 n = 8 Cyclomatic Complexity = 10 - 8 + 2 = 4

![](https://vison-blog.oss-cn-beijing.aliyuncs.com/20210727111603.png)

计算公式为：

V(G) = E - N + 2

其中，e表示控制流图中边的数量，n表示控制流图中节点的数量。


更多可参考 [http://kaelzhang81.github.io/2017/06/18/详解圈复杂度/](http://kaelzhang81.github.io/2017/06/18/%E8%AF%A6%E8%A7%A3%E5%9C%88%E5%A4%8D%E6%9D%82%E5%BA%A6/)


### ExcessiveMethodLength

方法长度，该规则有2个属性

minimum 最小限定值 默认 100

ignore-whitespace 是否忽略空白行 默认 false

### ExcessiveClassLength

类长度

minimum 最小限定值 默认 1000

ignore-whitespace 是否忽略空白行 默认 false


### ExcessiveParameterList

参数个数限定

minimum 10，根据《clean code》一书的说法，这个值应该限定为3

### ExcessivePublicCount

公共方法、公共属性

minimum	45

### TooManyFields

maxfields	15

### TooManyMethods

maxmethods	25	
ignorepattern	(^(set|get))i

### TooManyPublicMethods

maxmethods	10	The method count reporting threshold
ignorepattern	(^(set|get))i


## 自定义规则

有的默认规则也许并不能满足自身需求需做舍弃或修改。例如函数参数数，在《clean code》一书中定义的是最多为3，而phpmd默认指定的是10. 10个确实已经非常难看了，想象你去调用一个有10个参数的函数，你一定会吐槽懵逼的。

好在phpmd这些都可以修改，如下：

- 引入unusedcode规则集
- 引入codesize,并暂时排除`NPathComplexity`和`CyclomaticComplexity`这两个理解起来有一定困难的规则。诚然`CyclomaticComplexity`在度量复杂度十分有效，但若你的所有函数已经满足`ExcessiveMethodLength`已经进步很大了，所以一步步来。
- 修改ExcessiveParameterList,让限定值为3.
- 修改ExcessiveMethodLength和ExcessiveClassLength,忽略空白行
- 排除StaticAccess规则

```xml
<?xml version="1.0"?>
<ruleset name="My first PHPMD rule set"
         xmlns="http://pmd.sf.net/ruleset/1.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://pmd.sf.net/ruleset/1.0.0
                     http://pmd.sf.net/ruleset_xml_schema.xsd"
         xsi:noNamespaceSchemaLocation="
                     http://pmd.sf.net/ruleset_xml_schema.xsd">
    <description>
        My custom rule set that checks my code...
    </description>

    <rule ref="rulesets/unusedcode.xml" />
    <rule ref="rulesets/codesize.xml">
        <exclude name="ExcessiveParameterList" />
        <exclude name="NPathComplexity"/>
        <exclude name="CyclomaticComplexity"/>
    </rule>
    <rule ref="rulesets/codesize.xml/ExcessiveParameterList">
        <properties>
            <property name="minimum">
                <value>
                    3
                </value>
            </property>
        </properties>
    </rule>
    <rule ref="rulesets/codesize.xml/ExcessiveClassLength">
        <properties>
            <property name="ignore-whitespace">
                <value>
                    true
                </value>
            </property>
        </properties>
    </rule>
    <rule ref="rulesets/codesize.xml/ExcessiveMethodLength">
        <properties>
            <property name="ignore-whitespace">
                <value>
                    true
                </value>
            </property>
        </properties>
    </rule>
    <rule ref="rulesets/cleancode.xml">
        <exclude name="StaticAccess" />
    </rule>
</ruleset>
```


