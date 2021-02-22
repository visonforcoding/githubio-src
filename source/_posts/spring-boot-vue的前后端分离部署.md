---
title: spring-boot+vue+supervisor+nginx的前后端分离部署
date: 2021-02-22 14:43:54
tags: java
---

- 要保证同域部署

> 我采取的思路是，前端请求接口时统一加上api前缀，nginx将api前缀的路由请求代理转发到spring-boot

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
