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

## 作为服务运行

此时我们需要编写.service脚本作为服务后台运行

```service
[Unit]
Description=glances  daemon
After=network.target influxdb.service

[Service]
User=root
Group=root
ExecStart=/usr/local/bin/glances --quiet --export influxdb
Type=simple
KillMode=process

[Install]
WantedBy=multi-user.target
```

命名该文件为`glances.service`并放到`/usr/lib/systemd/system`目录下

`systemctl start glances` 启动

更多的 `service`脚本编写可参考，http://www.jinbuguo.com/systemd/systemd.service.html

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

### docker-granfana安装

```yml
# docker-compose.yml
version: "3.1"

services:
  grafana:
    image: grafana/grafana:5.1.0
    ports:
      - 3001:3000
    environment:
        - GF_SECURITY_ADMIN_PASSWORD__FILE=/run/secrets/granfa_admin_pwd # 5.2.0之后才可用
```

###  nginx配置

```conf
 server {
        listen       80;
        server_name  grafana-dev.domain.cn;

        #charset koi8-r;
        location / {
           proxy_pass  http://127.0.0.1:3001;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
        }

}
```
就可以在web上进行访问,初始的账号密码都是`admin`


### 配置数据源

![](https://vison-blog.oss-cn-beijing.aliyuncs.com/20210430141408.png)

docker安装情况应注意docker容器ip 和宿主机ip

```shell
docker network ls # 查看docker网络
docker network inspect $networkid # 查看具体网络信息
```

![](https://vison-blog.oss-cn-beijing.aliyuncs.com/20210811145603.png)

在配置`influxdb` 数据源时，如果你是用`docker`安装，需要保持`granfana`和`influxdb`是在同一个网段

![](https://vison-blog.oss-cn-beijing.aliyuncs.com/20210811145551.png)

grafana 还支持zipkin

![](https://vison-blog.oss-cn-beijing.aliyuncs.com/20210430141436.png)


