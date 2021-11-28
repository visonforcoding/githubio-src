---
title: java开发环境准备
date: 2020-08-27 11:41:07
tags: java
---

## JDK

最近似乎java 8以上的版本都不能从oracle官网下载了，于是就尝试使用open jdk11

![](http://img.rc5j.cn/blog20200827114344.png)

<!--more-->


### 下载

可以从 https://mirrors.huaweicloud.com/openjdk/ 下载得到

### mac安装

```
sudo mv /Downloads/jdk11 /Library/Java/JavaVirtualMachines/jdk-11.jdk
```

### linux

配置bash_profile

`vim ~/.bash_profile`

```
JAVA_HOME="/usr/local/jdk-11.0.2"
PATH=$PATH:$HOME/bin:$JAVA_HOME/bin
export PATH
```

## maven

### 源码安装

Maven 下载地址：http://maven.apache.org/download.cgi

### mac brew 安装

```shell
brew install maven
```

