---
title: 数据|地理位置geo处理之mongodb geo 索引
date: 2017-12-01 10:34
tags: 方案
---

> 目前越来越多的业务都会基于LBS，附近的人，外卖位置，附近商家等等，现就讨论离我最近这一业务场景的解决方案。

目前已知解决方案有:

- mysql 自定义函数计算
- mysql geo索引
- mongodb geo索引
- postgresql PostGis索引
- redis geo
- ElasticSearch

本文测试下mongodb geo索引 函数运算的性能

<!-- more -->

## 准备工作

### 创建数据表

```sql
db.driver.createIndex({loc: "2dsphere"})
```

## 创建数据python脚本

```python
# coding=utf-8
from pymongo import MongoClient
import logging
import random
import threading

""" 中国的经纬度范围 纬度3.86~53.55，经度73.66~135.05。大概0.00001度差距1米 """

# 创建 日志 对象
logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

# Connect to the mongodb database

mongoconn = MongoClient('127.0.0.1', 27017)
mdb = mongoconn.geo_analysis
driver_collection = mdb.driver


def ins_driver(thread_name, nums):
    logger.info('开启线程%s' % thread_name)
    for i in range(nums):
        lng = '%.5f' % random.uniform(73.66, 135.05)
        lat = '%.5f' % random.uniform(3.86, 53.55)
        logging.debug('插入记录:%s' % i)
        driver_collection.insert_one({
            "loc":[
                float(lng),
                float(lat)
            ]
        })


thread_nums = 10
for i in range(thread_nums):
    t = threading.Thread(target=ins_driver, args=(i, 40000))
    t.start()

```

![image.png](http://upload-images.jianshu.io/upload_images/4033700-dda526bdfcc5c759.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

以上脚本创建10个线程，10个线程插入4万条数据。耗费52.43s执行完,总共插入40万条数据

## 测试

- 测试环境

系统：mac os

内存：16G

cpu: intel core i5

硬盘: 500g 固态硬盘

测试下查找距离(134.38753,18.56734)附近20公里的司机

```js
db.runCommand({geoNear:'driver', near:[134.38753,18.56734], spherical:true, maxDistance:20000/6378000, distanceMultiplier:6378000});
```

- 耗时：0.001s
- explain:使用索引
