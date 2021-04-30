---
title: 利用Locust进行性能测试
date: 2021-01-23 10:17:02
tags: 软件工程
---

- 要看一个项目的最大可用能力是多少，性能测试工作少不了.
- 每一个项目都应该做压测
- 多线程并发模型一定要做压测

<!--more-->


## 安装

```
$ pip3 install locust
```

## 编写脚本

```python
import time
from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
    wait_time = between(1, 2.5)

    @task
    def hello_world(self):
        self.client.get("/hello")
        self.client.get("/world")

    @task(3)
    def view_items(self):
        for item_id in range(10):
            self.client.get(f"/item?id={item_id}", name="/item")
            time.sleep(1)

    def on_start(self):
        self.client.post("/login", json={"username":"foo", "password":"bar"})

```

`wait_time = between(1, 2.5)`

Our class defines a wait_time that will make the simulated users wait between 1 and 2.5 seconds after each task (see below) is executed. For more info see wait_time attribute.

`def hello_world(self):`


```python
@task
def hello_world(self):
    self.client.get("/hello")
    self.client.get("/world")

@task(3)
def view_items(self):
...
```
`task(3)` 内的参数表示任务执行的权重，`view_items`的次数将是`hello_world`次数的3倍。

## 执行

```
$ locust -f locust_files/my_locust_file.py
```

![](https://vison-blog.oss-cn-beijing.aliyuncs.com/20210330151409.png)

任务执行界面和结果

![](https://vison-blog.oss-cn-beijing.aliyuncs.com/20210330151426.png)
