---
title: gunicorn+flask_rest构建部署轻量级api服务
date: 2020-08-20 15:51:30
tags: python
---

![](http://img.rc5j.cn/blog20200820155306.png)

<!--more-->

## flask 结构

首先简单看看 flask_rest的目录结构。

![](http://img.rc5j.cn/blog20200820155423.png)

### 入口文件

```python
#app.py
from flask import Flask
from flask_restful import Resource, Api
from resources.bd import Index,Format
from flask_cors import CORS

# from common import config
app = Flask(__name__)
CORS(app)
api = Api(app)



api.add_resource(Format, '/bd/format')

# if __name__ == '__main__':
#     app.run(debug=True)
```

如果使用gunicorn启动，则注释掉app.run

## gunicorn启动配置

```python
# config.py
import os
import gevent.monkey
gevent.monkey.patch_all()

import multiprocessing

debug = True
loglevel = 'debug'
bind = "0.0.0.0:5000"
pidfile = "logs/gunicorn.pid"
accesslog = "logs/access.log"
errorlog = "logs/debug.log"
daemon = True

# 启动的进程数
workers = multiprocessing.cpu_count()
worker_class = 'gevent'
x_forwarded_for_header = 'X-FORWARDED-FOR'
```

## 启动

```shell
python3 -m venv webpj
source webpj/bin/activate
pip install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
pip install xlrd -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
pip install openpyxl -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
gunicorn -c config.py app:app
```

## 平滑重启

```shell
cat logs/gunicorn.log | xargs kill -HUP
```


