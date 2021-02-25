---
title: 地理位置geo处理之mysql函数
date: 2017-12-01 17:39:29
tags: mysql
---

> 目前越来越多的业务都会基于LBS，附近的人，外卖位置，附近商家等等，现就讨论离我最近这一业务场景的解决方案。

目前已知解决方案有:

- mysql 自定义函数计算
- mysql geo索引
- mongodb geo索引
- postgresql PostGis索引
- redis geo
- ElasticSearch

本文测试下mysql 函数运算的性能

<!-- more -->

## 准备工作

### 创建数据表

```sql
CREATE TABLE `driver` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `lng` float DEFAULT NULL,
  `lat` float DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```

### 创建测试数据

在创建数据之前先了解下基本的地理知识:

- **全球经纬度的取值范围为:** 纬度-90~90，经度-180~180

- **中国的经纬度范围大约为：** 纬度3.86~53.55，经度73.66~135.05

- 北京行政中心的纬度为39.92，经度为116.46

- 越北面的地方纬度数值越大，越东面的地方经度数值越大

- 度分转换： 将度分单位数据转换为度单位数据，公式：度=度+分/60

- 分秒转换： 将度分秒单位数据转换为度单位数据，公式：度 = 度 + 分 / 60 + 秒 / 60 / 60

在纬度相等的情况下：
- 经度每隔0.00001度，距离相差约1米

在经度相等的情况下：
- 纬度每隔0.00001度，距离相差约1.1米


## mysql函数计算

```sql
DELIMITER //
CREATE DEFINER=`root`@`localhost` FUNCTION `getDistance`(
	`lng1` float(10,7) 
    ,
	`lat1` float(10,7)
    ,
	`lng2` float(10,7) 
    ,
	`lat2` float(10,7)

) RETURNS double
    COMMENT '计算2坐标点距离'
BEGIN
	declare d double;
    declare radius int;
    set radius = 6371000; #假设地球为正球形，直径为6371000米
    set d = (2*ATAN2(SQRT(SIN((lat1-lat2)*PI()/180/2)   
        *SIN((lat1-lat2)*PI()/180/2)+   
        COS(lat2*PI()/180)*COS(lat1*PI()/180)   
        *SIN((lng1-lng2)*PI()/180/2)   
        *SIN((lng1-lng2)*PI()/180/2)),   
        SQRT(1-SIN((lat1-lat2)*PI()/180/2)   
        *SIN((lat1-lat2)*PI()/180/2)   
        +COS(lat2*PI()/180)*COS(lat1*PI()/180)   
        *SIN((lng1-lng2)*PI()/180/2)   
        *SIN((lng1-lng2)*PI()/180/2))))*radius;
    return d;
END//
DELIMITER ;
```

## 创建数据python脚本

```python
# coding=utf-8
from orator import DatabaseManager, Model
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

# Connect to the database

config = {
    'mysql': {
        'driver': 'mysql',
        'host': 'localhost',
        'database': 'dbtest',
        'user': 'root',
        'password': '',
        'prefix': ''
    }
}

db = DatabaseManager(config)
Model.set_connection_resolver(db)


class Driver(Model):
    __table__ = 'driver'
    __timestamps__ = False
    pass


def ins_driver(thread_name,nums):
    logger.info('开启线程%s' % thread_name)
    for _ in range(nums):
        lng = '%.5f' % random.uniform(73.66, 135.05)
        lat = '%.5f' % random.uniform(3.86, 53.55)

        driver = Driver()
        driver.lng = lng
        driver.lat = lat
        driver.save()

thread_nums = 10
for i in range(thread_nums):
    t = threading.Thread(target=ins_driver, args=(i, 400000))
    t.start()
```
![image.png](http://upload-images.jianshu.io/upload_images/4033700-dda526bdfcc5c759.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



以上脚本创建10个线程，10个线程插入4万条数据。耗费150.18s执行完,总共插入40万条数据

## 测试

- 测试环境

系统：mac os

内存：16G

cpu: intel core i5

硬盘: 500g 固态硬盘

测试下查找距离(134.38753,18.56734)这个坐标点最近的10个司机

```sql
select *,`getDistance`(134.38753,18.56734,`lng`,`lat`) as dis from driver ORDER BY dis limit 10
```
- 耗时：18.0s
- explain:全表扫描

我测试了从1万到10万间隔1万和从10万到90万每间隔10万测试的结果变化

![image.png](http://upload-images.jianshu.io/upload_images/4033700-c40f60c1ef7b3f18.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


## 结论

- 此方案在数据量达到3万条查询耗时就会超过1秒
- 大约每增加1万条就会增加0.4秒的耗时
