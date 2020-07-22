---
title: docker+compose+nginx+php
date: 2018-07-22 16:52:09
tags:  docker
---

![](http://img.rc5j.cn/blog20200722165520.png)

<!--more-->

> Docker 可以让开发者打包他们的应用以及依赖包到一个轻量级、可移植的容器中，然后发布到任何流行的 Linux 机器上，也可以实现虚拟化。

## 我用docker做什么？

快速搭建开发所需环境，测试实验新组件(如rabbitmq,kafka).避免因安装而浪费太多时间，我的目的是快速尝试使用。

## 安装docker

```shell
brew cask install docker
```

## docker-compose

Compose 是一个用户定义和运行多个容器的 Docker 应用程序。在 Compose 中你可以使用 YAML 文件来配置你的应用服务。然后，只需要一个简单的命令，就可以创建并启动你配置的所有服务。


## 目录结构


![2018-08-07-14-17-25](http://upload-images.jianshu.io/upload_images/4033700-1a2d2c681ac9df9c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

一组服务建立一个目录

## 配置文件

```yaml
version: '2'
services:
  php7.2:
    image: php:7.2-fpm
    ports:
      - "9000:9000"
    volumes: 
      - ./php:/usr/local/etc/php
      - /Users/caowenpeng/www:/www
  nginx:
    image: nginx
    ports: 
      - "80:80"
    volumes:
      - /Users/caowenpeng/www:/www
      - ./nginx:/etc/nginx

```

## 启动

```shell
docker-compose up -d
```

## 常用命令

|命令|说明|
|---|---|
|up|创建和启动容器|
|ps|列出所有容器|
|down|停止并删除容器，镜像，挂载|
|start|启动服务|
|stop|停止服务|
|restart|重启服务|


**第一次使用up,之后使用start,如果再次使用up将会重新创建容器，一些对容器的修改将会丢失**


## 其他问题

进入容器 

```bash
 docker-compose exec php7.2 bash
```

进入容器后会发现只能用少量命令，连ps等都没有，这个时候需要安装一些程序

```bash
apt-get update  ##更新元
apt-get install procps  ## 安装 ps
```

安装php-rdkafka拓展

```bash
apt-get install wget
wget https://github.com/edenhill/librdkafka/archive/master.zip

apt-get install unzip

unzip master.zip

cd librdkafka

./configure 

make

make install 

pecl install http://pecl.php.net/get/rdkafka-3.0.4.tgz

#在php.ini 配置启用 rdkafka拓展



```