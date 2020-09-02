---
title: supervisor使用
date: 2020-09-02 10:50:48
tags: 运维
---

作为一款进程管理工具，supervisor普遍用来管理应用的守护进程

<!--more-->

## 安装

常规安装的方式有两种,pip安装或发行版安装

以centos 8为pip安装方式为例。

### pip安装

```shell
pip install supervisor
```

## 运行

### 配置文件

```
echo_supervisord_conf > /etc/supervisord.conf
```
生成配置文件

### 配置systemd服务

如果是发行版安装，默认会配置好开机启动服务。如果非发行版安装，可以手动配置。

There are user-contributed scripts for various operating systems at: https://github.com/Supervisor/initscripts

注意，事实上github上的脚本有点问题，与实际安装的目录位置不匹配。稍作修改

```ini
# supervisord service for systemd (CentOS 7.0+)
# by ET-CS (https://github.com/ET-CS)
[Unit]
Description=Supervisor daemon

[Service]
Type=forking
ExecStart=/usr/local/bin/supervisord
ExecStop=/usr/local/bin/supervisorctl $OPTIONS shutdown
ExecReload=/usr/local/bin/supervisorctl $OPTIONS reload
KillMode=process
Restart=on-failure
RestartSec=42s

[Install]
WantedBy=multi-user.target
```
将此文件为 ``
### 启动服务

重新读取所有服务项

```
systemctl daemon-reload
```
启动服务

```
systemctl start supervisord.service
```
开机启动

```
systemctl enable supervisord.service
```

### 使用

### 启用子配置目录

`vim /etc/supervisord.conf`
最后2行打开注释并编辑为
```
[include]
files = ./supervisord.d/*.ini
```

重启

```
systemctl reload supervisord.service
# 或者
supervisorctl reload
```

### 添加项目

`vim /etc/supervisord.d/glances.ini`

```ini
[program:glances]
command=glances --export influxdb -q
process_name=%(program_name)s
numprocs=1
directory=/tmp
umask=022
priority=999
autostart=true
autorestart=unexpected
startsecs=10
startretries=3
exitcodes=0
stopsignal=TERM
stopwaitsecs=10
stopasgroup=false
killasgroup=false
user=root
redirect_stderr=false
stdout_logfile=/var/log/glances/glances-out.log
stdout_logfile_maxbytes=1MB
stdout_logfile_backups=10
stdout_capture_maxbytes=1MB
stdout_events_enabled=false
stderr_logfile=/var/log/glances/glances-err.log
stderr_logfile_maxbytes=1MB
stderr_logfile_backups=10
stderr_capture_maxbytes=1MB
```
注意先建好目录 `/var/log/glances`

### 重新读取配置并启用

```
supervisorctl reload
supervisorctl start glances
```

### 可查看运行状态

```
supervisorctl status
```

结果

```
glances                          RUNNING   pid 46026, uptime 0:05:05
```