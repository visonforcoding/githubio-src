---
title: 数据库中间件shardingsphere-proxy
date: 2022-02-25 17:04:26
tags: mysql
---


## 前言

坦白说80%的程序员的80%工作都是在与数据库打交道，显然数据库工作无比的重要。当数据量不大的时候似乎一切都不是问题,一旦数据量变大，程序员的挑战就变得越来越大。

当单表数据超过8千万，普通的加索引可能效果已经不会太好了。这个时候通常的解决办法是分库分表，也就是老生常谈的`sharding`.

今天我们来看看`shardingsphere`的解决方案。

<!--more-->

官方文档：[https://shardingsphere.apache.org/document/5.1.0/en/overview/](https://shardingsphere.apache.org/document/5.1.0/en/overview/)

当前`shardingsphere`有3个产品

- ShardingSphere-JDBC
- ShardingSphere-Proxy
- ShardingSphere-Sidecar(TODO)

![](https://vison-blog.oss-cn-beijing.aliyuncs.com/20220225175604.png)

`ShardingSphere-Sidecar`还在todo，我们暂且不讨论。当前ShardingSphere在github有15k的star，可见应该还是广受大家认可的。

![](https://vison-blog.oss-cn-beijing.aliyuncs.com/20220225175742.png)

`ShardingSphere-JDBC`是java的类库与应用程序和语言绑定，`ShardingSphere-Proxy`是中间代理与语言无关。

![](https://vison-blog.oss-cn-beijing.aliyuncs.com/20220225173123.png)

从官网的蓝图来看，这是一个较新的项目，同时开发团队有着长远的规划。

## 产品架构

![](https://vison-blog.oss-cn-beijing.aliyuncs.com/20220225174114.png)

从这张产品架构图我们可以看到大致的一些产品功能：

- sql审计
- sql防火墙
- 分片
- 读写分离
- DB负载均衡
- 伸缩拓展
- 影子库

## 分片

我们来体验下`ShardingSphere-Proxy`的sharding。

### 安装

从官网的下载页面可以下到二进制的程序，如果你是使用mysql则还需要下载jdbc驱动，这些安装都很简单。

### 配置

主要工作是在配置上面。为了方便测试，我们假设的场景是只分表不分库。

我们将订单表t_order按user_id%2分2张表,t_order_0和t_order_1。

我们要对2个配置文件进行配置。

1. server.yaml

`server.yaml`主要是对ShardingSphere-Proxy本身的服务配置。

```yaml
rules:
 - !AUTHORITY
   users:
     - root@%:123456
     - sharding@:sharding
   provider:
     type: ALL_PRIVILEGES_PERMITTED
 - !TRANSACTION
   defaultType: XA
   providerType: Atomikos
 - !SQL_PARSER
   sqlCommentParseEnabled: true
   sqlStatementCache:
     initialCapacity: 2000
     maximumSize: 65535
     concurrencyLevel: 4
   parseTreeCache:
     initialCapacity: 128
     maximumSize: 1024
     concurrencyLevel: 4

props:
 max-connections-size-per-query: 1
 kernel-executor-size: 16  # Infinite by default.
 proxy-frontend-flush-threshold: 128  # The default value is 128.
 proxy-opentracing-enabled: false
 proxy-hint-enabled: false
 sql-show: false
 check-table-metadata-enabled: false
 show-process-list-enabled: false
   # Proxy backend query fetch size. A larger value may increase the memory usage of ShardingSphere Proxy.
   # The default value is -1, which means set the minimum value for different JDBC drivers.
 proxy-backend-query-fetch-size: -1
 check-duplicate-table-enabled: false
 proxy-frontend-executor-size: 0 # Proxy frontend executor size. The default value is 0, which means let Netty decide.
   # Available options of proxy backend executor suitable: OLAP(default), OLTP. The OLTP option may reduce time cost of writing packets to client, but it may increase the latency of SQL execution
   # and block other clients if client connections are more than `proxy-frontend-executor-size`, especially executing slow SQL.
 proxy-backend-executor-suitable: OLAP
 proxy-frontend-max-connections: 0 # Less than or equal to 0 means no limitation.
 sql-federation-enabled: false
   # Available proxy backend driver type: JDBC (default), ExperimentalVertx
 proxy-backend-driver-type: JDBC
```

`users:` 定义了代理的连接信息。`root@%:123456`代表用户名root密码123456和在0.0.0.0上监听。

2. config-sharding.yaml

`config-sharding.yaml`定义了分库分表的算法信息。

```yaml
schemaName: db_test

dataSources:
 ds_0:
   url: jdbc:mysql://127.0.0.1:3306/db_test?serverTimezone=UTC&useSSL=false
   username: test_rw
   password: ko*0^fwZtQ2nZv
   connectionTimeoutMilliseconds: 30000
   idleTimeoutMilliseconds: 60000
   maxLifetimeMilliseconds: 1800000
   maxPoolSize: 50
   minPoolSize: 1

rules:
- !SHARDING
 tables:
   t_order:
     actualDataNodes: ds_0.t_order_${0..1}
     tableStrategy:
       standard:
         shardingColumn: user_id
         shardingAlgorithmName: t_order_inline
 bindingTables:
   - t_order
 defaultDatabaseStrategy:
   none:
 defaultTableStrategy:
   none:
 
 shardingAlgorithms:
   t_order_inline:
     type: INLINE
     props:
       algorithm-expression: t_order_${user_id % 2}

 scalingName: default_scaling
 scaling:
   default_scaling:
     input:
       workerThread: 40
       batchSize: 1000
       rateLimiter:
         type: QPS
         props:
           qps: 50
     output:
       workerThread: 40
       batchSize: 1000
       rateLimiter:
         type: TPS
         props:
           tps: 2000
     streamChannel:
       type: MEMORY
       props:
         block-queue-size: 10000
     completionDetector:
       type: IDLE
       props:
         incremental-task-idle-minute-threshold: 30
     dataConsistencyChecker:
       type: DATA_MATCH
       props:
         chunk-size: 1000
```

`schemaName`非常重要，代表逻辑库名。

![](https://vison-blog.oss-cn-beijing.aliyuncs.com/20220225182212.png)

我们通过mysql cli连接上去可以看到db名称即为`schemaName`定义的值。

我们定义了一个数据源ds_0映射到物理库db_test。

`t_order`逻辑表映射到真实表t_order_0和t_order_1, `shardingColumn`为user_id,`shardingAlgorithmName`为t_order_inline

### 测试

接下来我们来写一段脚本测试下，主要测试2个场景。

- 跨表查询数据聚合
- 带分片字段的分片查询

对应的sql分别是

```sql
select count(*) from t_order;
select * from t_order where user_id = 12;
```

对应的java代码是

```java
package com.vison.jpal.queryprocess;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.util.Properties;

public class TestSharding {
    public static Logger logger = LogManager.getLogger(ThreadQuery.class.getName());

    public static void main(String[] args) throws Exception {
        //2. 获得数据库连接
        logger.info("开始....");
        Connection conn = DriverManager.getConnection("jdbc:mysql://www-dev.h66.cn:3307/db_test", "root", "123456");
        //3.操作数据库，实现增删改查
        Statement stmt = conn.createStatement();
        //count
        Integer user_id = 12;
        ResultSet countQuery = stmt.executeQuery("SELECT count(*) FROM t_order");
//        System.out.print(rs.getC);
        //如果有数据，rs.next()返回true
        if(countQuery.next()){
            System.out.printf("数据总数: %d%n",countQuery.getInt(1));
        }
        List<Map<String, Object>> listUser = new ArrayList<>();
        ResultSet shardingQuery = stmt.executeQuery(String.format("SELECT * FROM t_order where user_id = %s", user_id));
        while (shardingQuery.next()) {
            Map<String, Object> user = new HashMap<>();
            user.put("order_no", shardingQuery.getString("order_no"));
            user.put("user_id", shardingQuery.getInt("user_id"));
            listUser.add(user);
        }
        System.out.print(listUser);
    }
}

```

得出结果

![](https://vison-blog.oss-cn-beijing.aliyuncs.com/20220225183624.png)

## 收益

总结下我们使用`ShardingSphere-Proxy`能给我们带来哪些好处

- 使用代理的方式，对项目代码无入侵，与语言无关。任何编程语言都能接入。
- 中间件代理帮忙处理了分库分表查询的问题并且能保障性能,这无疑解放了程序员对分库分表需求的担忧。当有分库分表的需求时，几乎还可以像操作单表那样操作。
- 负载均衡、读写分离、影子库表功能让程序性能、可靠性大大提升

## 风险

- 跨表查询数据聚合到底性能如何，最佳能支持多少表多少数据量的跨表查询，如何达到最佳性能这些问题都需要考虑
