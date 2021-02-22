---
title: spring-boot+vue+supervisor+nginx的前后端分离部署
date: 2021-02-22 14:43:54
tags: java
---

- 要保证同域部署,因为跨域会有很多问题要重新解决

顺便树下，但其实现在互联网产品一般都有多客户端，pc web 、小程序、app。保守的同域session模式保持会话已经满足不了一些需求。比如，单端登录等。

言归正传，我采取的思路是，前端请求接口时统一加上api前缀，nginx将api前缀的路由请求代理转发到spring-boot

<!--more-->

## nginx配置

```nginx

server {
    server_name admin.domain.xyz;
    index index.html;

    location  / {
                index index.html;
                root /home/wwwuser/webroot/itdoc-admin-web/dist/spa;
        }

    location /api/ {
              proxy_pass  http://127.0.0.1:8081/;
        }
    # optionally disable falling back to PHP script for the asset directories;
    # nginx will return a 404 error when files are not found instead of passing the
    # request to Symfony (improves performance but Symfony's 404 page is not displayed)
    # location /bundles {
    #     try_files $uri =404;
    # }

    error_log /var/log/nginx/admin_error.log;
    access_log /var/log/nginx/admin_access.log;
}

```

## supervisor守护java -jar

我这里采取java -jar模式部署，但是单纯的这种模式并不能保证自启动和进程监控等。因此需要借助supervisor。

```ini
[program:itdoc]
command=/usr/local/jdk-11.0.2/bin/java -jar itdoc-0.0.2-SNAPSHOT.jar
process_name=%(program_name)s
numprocs=1
directory=/home/wwwuser/webroot
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
user=wwwuser
redirect_stderr=false
stdout_logfile=/var/log/webroot/itdoc-out.log
stdout_logfile_maxbytes=1MB
stdout_logfile_backups=10
stdout_capture_maxbytes=1MB
stdout_events_enabled=false
stderr_logfile=/var/log/webroot/itdoc-err.log
stderr_logfile_maxbytes=1MB
stderr_logfile_backups=10
stderr_capture_maxbytes=1MB

```

这里的`autostart` 和 `autorestart` 能保证自启动和启动重启
