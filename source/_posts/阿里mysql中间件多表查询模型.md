---
title: 阿里mysql中间件多表查询模型
date: 2022-02-23 15:36:45
tags:
---

之前读了一本书《企业IT架构转型之道:阿里巴巴中台战略思想与架构实战》，期中有关于数据库中间件的部分实现令我映像深刻。

![图片来源:https://shardingsphere.apache.org/document/current/en/concepts/pluggable/](https://vison-blog.oss-cn-beijing.aliyuncs.com/20220223170048.png)

中间件解决了几个问题：

- 数据库使用治理,通过mysql proxy的形式,能在开发时期的建表不规范ddl、生产的查询潜在危害sql进行预警、拦截、监控等操作
- sharding处理,通过中间件的处理使得业务开发不用太关心sharding处理专心处理业务逻辑。
- 负载均衡处理,可以使得sql分散到不同实例，并对业务层无侵入。

对于sharding这一块还解决了在分库分表之后跨库夸表的查询，采用多线程查询内存聚合的方式来提高查询效率。

```java
package com.vison.jpal.queryprocess;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.Statement;
import java.util.*;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

public class ThreadQuery extends Thread {

    public static final String URL = "jdbc:mysql://localhost:3306/demo";
    public static final String USER = "root";
    public static final String PASSWORD = "";
    public static List<Map<String, Object>> totalListUser;
    public static Logger logger = LogManager.getLogger(ThreadQuery.class.getName());

    protected String table;

    public void setTable(String table) {
        this.table = table;
    }

    public static void main(String[] args) throws Exception {
        totalListUser = new ArrayList<>();
        List<String> tables = new ArrayList<>();
        for (int i = 0; i <= 246; i++) {
            tables.add(String.format("user_%02d", i));
        }
        List<Map<String, Object>> listUser = new ArrayList<>();
        List<ThreadQuery> threads = new ArrayList<>();
        for (String table : tables) {
            ThreadQuery threadQuery = new ThreadQuery();
            threadQuery.setTable(table);
            threadQuery.start();
            threads.add(threadQuery);
        }
        for (Thread thread : threads) {
            thread.join();
        }
        logger.info("完成");
        System.out.print(totalListUser);

    }


    public void run() {
        try {
            List<Map<String, Object>> rs = this.singleQueryUser();
            ThreadQuery.totalListUser.addAll(rs);
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
    }

    public List<Map<String, Object>> singleQueryUser() throws Exception {
        //2. 获得数据库连接
        logger.info(String.format("线程%s启动",table));
        Connection conn = DriverManager.getConnection(URL, USER, PASSWORD);
        //3.操作数据库，实现增删改查
        Statement stmt = conn.createStatement();
        ResultSet rs = stmt.executeQuery(String.format("SELECT * FROM %s WHERE `age` = 25 LIMIT 2 ",table));
        //如果有数据，rs.next()返回true
        List<Map<String, Object>> listUser = new ArrayList<>();
        while (rs.next()) {
            Map<String, Object> user = new HashMap<>();
            user.put("name", rs.getString("name"));
            user.put("age", rs.getInt("age"));
            listUser.add(user);
        }
        return listUser;
    }
}

```

此代码只是一个非常基础的实现demo,真正上生产还需要解决很多其他问题：

1. 线程池链接池解决链接和线程建立开销
2. 并发数的最佳数量设置
3. limit和order by的处理,设想`select * from user where age = 25  order by create_time desc limit 10`该如何从sharding表进行处理
