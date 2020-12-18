---
title: NoSQL and Big Data Processing
tags:
---

![](https://vison-blog.oss-cn-beijing.aliyuncs.com/20201202183405.png)

## 历史

- 关系型数据库在业务当中占据主导地位
- 基于web的应用程序流量变得越来越大，特别是电商型站点
- 开发人员开始使用memcache或其他缓存机制


### Scaling Up 问题

 > Scale Out是指Application可以在水平方向上扩展。一般对数据中心的应用而言，Scale out指的是当添加更多的机器时，应用仍然可以很好的利用这些机器的资源来提升自己的效率从而达到很好的扩展性。 Scale Up是指Application可以在垂直方向上扩展。一般对单台机器而言，Scale Up值得是当某个计算节点（机器）添加更多的CPU Cores，存储设备，使用更大的内存时，应用可以很充分的利用这些资源来提升自己的效率从而达到很好的扩展性。

 - 随着数据集的增大,光靠scale up的方式暴露越来越多的问题
 - RDBMS 并不是设计来进行分布式的。
 - 开始探索多节点数据库方案
 - "水平拓展"概念被提出来
 - 出现了不同的表现形式，主从Master-slave,分片Sharding

### Master/Slave

- 所有的写操作到主库，读操作在复制的从库。
- 某些关键的读操作可能会发生错误，当写操作没有完全复制到从库。
- 大数据量的读操作依然有问题

### Sharding

- 读写拓展都支持的比较好
- 对业务不透明,业务层侵入做划分
- 丢失关联关系，join操作不友好

### 其他的RDBMS拓展方式

- 多主复制
- 只插入，不更新
- 不做join,减少查询时间
- 内存型数据库

## NoSQL

- 指代 Not Only SQL
- 一类非关系型存储系统
- 没有固定的数据结构，不做join操作
- 对ACID不严格遵守，我们称为CAP理论


### ACID

在写入或更新资料的过程中，为保证事务（transaction）是正确可靠的，所必须具备的四个特

Atomicity（原子性）：一个事务（transaction）中的所有操作，或者全部完成，或者全部不完成，不会结束在中间某个环节

Consistency（一致性）：在事务开始之前和事务结束以后，数据库的完整性没有被破坏。这表示写入的资料必须完全符合所有的预设

Isolation（隔离性）：数据库允许多个并发事务同时对其数据进行读写和修改的能力，隔离性可以防止多个事务并发执行时由于交叉执行而导致数据的不一致。

Durability（持久性）：事务处理结束后，对数据的修改就是永久的，即便系统故障也不会丢失


### CAP理论

![](https://vison-blog.oss-cn-beijing.aliyuncs.com/20201203201903.png)

> 2000年7月，加州大学伯克利分校的Eric Brewer教授在ACM PODC会议上提出CAP猜想。2年后，麻省理工学院的Seth Gilbert和Nancy Lynch从理论上证明了CAP。之后，CAP理论正式成为分布式计算领域的公认定理。

### CAP理论概述

CAP理论：一个分布式系统最多只能同时满足一致性（Consistency）、可用性（Availability）和分区容错性（Partition tolerance）这三项中的两项。

### Consistency 一致性
一致性指“all nodes see the same data at the same time”，即更新操作成功并返回客户端完成后，所有节点在同一时间的数据完全一致，所以，一致性，说的就是数据一致性。

**Once a writer has written,all readers will see that write**

两种类型的一致性:

– strong consistency – ACID(Atomicity Consistency
Isolation Durability)

– weak consistency – BASE(Basically Available Softstate
Eventual consistency )

Availability 可用性
可用性指“Reads and writes always succeed”，即服务一直可用，而且是正常响应时间。


![](https://vison-blog.oss-cn-beijing.aliyuncs.com/20201203213555.png)


通常我们说的可用性，是服务或进程的5个9，即99.999%。

Traditionally, thought of as the server/process
available five 9’s (99.999 %).

Partition Tolerance分区容错性
分区容错性指“the system continues to operate despite arbitrary message loss or failure of part of the system”，即分布式系统在遇到某节点或网络分区故障的时候，仍然能够对外提供满足一致性和可用性的服务。




