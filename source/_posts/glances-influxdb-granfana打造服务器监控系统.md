---
title: glances+influxdb+granfana打造服务器监控系统
date: 2020-08-25 17:56:32
tags: devops
---

![](https://vison-blog.oss-cn-beijing.aliyuncs.com/20210430141234.png)

服务监控就是你的眼睛，当你对服务器运行状况一无所知时，你应该感到坐立不安。

<!--more-->

## glances安装

glances是由python编写的，因此可以使用pip直接安装

```
pip3 install glances
```

## influxdb安装

```
wget https://dl.influxdata.com/influxdb/releases/influxdb-1.8.2.x86_64.rpm
sudo yum localinstall influxdb-1.8.2.x86_64.rpm
```

## 收集数据到influxdb

配置 glances

`vim /etc/glances/glances.conf`

```ini
[influxdb]
# Configuration for the --export influxdb option
# https://influxdb.com/
host=localhost
port=8086
user=root
password=root
db=glances
prefix=localhost
#tags=foo:bar,spam:eggs
```

```
pip3 install influxdb
glances --export influxdb
```
执行 `glances --export influxdb` 测试下，报错

`InfluxDB database 'glances' did not exist. Please create it`需要新建数据库。

执行shell `influx`

```
CREATE DATABASE glances  #创建数据
SHOW DATABASES   # 查看数据库
```
再次执行`glances --export influxdb` ,可显示如下代表目前一切正常

![](https://vison-blog.oss-cn-beijing.aliyuncs.com/20210430141339.png)

## granfana安装

```
wget https://dl.grafana.com/oss/release/grafana-7.1.5-1.x86_64.rpm
sudo yum install grafana-7.1.5-1.x86_64.rpm
```
### 启动

```shell
systemctl daemon-reload
systemctl start grafana-server
systemctl status grafana-server

systemctl enable grafana-server.service
```

### 配置数据源

![](https://vison-blog.oss-cn-beijing.aliyuncs.com/20210430141408.png)

grafana 还支持zipkin

![](https://vison-blog.oss-cn-beijing.aliyuncs.com/20210430141436.png)


