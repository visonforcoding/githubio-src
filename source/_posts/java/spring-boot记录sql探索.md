---
title: spring-boot记录sql探索
date: 2021-02-23 19:28:29
tags: java
---

> 目标记录每次请求内的http、es、mysql耗时，本篇讨论mysql部分

为什么说要探索，这不是很简单的事么？但是能满足以下几点么？

- 能记录limit等参数
- 能将参数和sql写一起，能直接使用
- 能记录耗时
- 能计数累加,统计一次请求中sql执行的总数和总耗时

<!--more-->

## spring原生能力

```ini
logging.level.org.hibernate.SQL=debug
logging.level.org.hibernate.type.descriptor.sql.BasicBinder=trace
```
通过上面两条配置。

- ✔️可以显示sql.
- ❌不能和参数一行显示
- ❌不能显示limit参数
- ❌不能计数和记录耗时

```
2021-02-23 19:35:42.932 DEBUG 97586 --- [  restartedMain] org.hibernate.SQL                        : select admin0_.id as id1_0_, admin0_.create_time as create_t2_0_, admin0_.modify_time as modify_t3_0_, admin0_.email as email4_0_, admin0_.password as password5_0_, admin0_.status as status6_0_, admin0_.username as username7_0_ from admin admin0_ where admin0_.username=?
2021-02-23 19:35:42.949 TRACE 97586 --- [  restartedMain] o.h.type.descriptor.sql.BasicBinder      : binding parameter [1] as [VARCHAR] - [root]
```

## 原生log+org.hibernate.EmptyInterceptor

`org.hibernate.EmptyInterceptor`提供钩子，hibernate本身提供entity的curd钩子。重写`EmptyInterceptor`方法，可以实现计数。但是`onPrepareStatement`方法只是装配sql前的事件，而且不是完整的sql。

- ✔️ 可以显示sql
- ❌ 不能和参数一行显示
- ❌ 不能显示limit参数
- ✔️ 能计数
- ❌ 不能记录耗时

```ini
spring.jpa.properties.hibernate.ejb.interceptor=com.vison.itdoc.config.HibernateInterceptor
```

```java
public class HibernateInterceptor extends EmptyInterceptor {
    
    @Override
    public boolean onLoad(Object entity, Serializable id, Object[] state, String[] propertyNames, Type[] types) {
//        Log.info("onload...", entity)
        return true;
    }
    
    @Override
    public String onPrepareStatement(String string) {
        // count++
        return INSTANCE.onPrepareStatement(string);
    }
    
    @Override
    public void afterTransactionCompletion(Transaction t) {
        INSTANCE.afterTransactionCompletion(t);
        Log.info("after trans complete", t);
    }
    
}
```

## log4jdbc

log4jdbc能很好的解决sql完整显示和记录耗时的问题

```
2021-02-23 19:59:13.709  INFO 97586 --- [nio-8081-exec-1] jdbc.sqltiming                           : select posts0_.id as id1_2_, posts0_.create_time as create_t2_2_, posts0_.modify_time as modify_t3_2_, 
posts0_.content as content4_2_, posts0_.title as title5_2_ from posts posts0_ where 1=1 order 
by posts0_.id asc limit 10 ;
 {executed in 1 msec}
```

还能够定义超过1定时间的执行sql记录为error类型。

```xml
        <dependency>
            <groupId>com.googlecode.log4jdbc</groupId>
            <artifactId>log4jdbc</artifactId>
            <version>1.2</version>
            <scope>runtime</scope>
        </dependency>

```

```ini
spring.datasource.driver-class-name: net.sf.log4jdbc.DriverSpy
#使用log4jdbc后mysql的url
spring.datasource.url=jdbc:log4jdbc:mysql://localhost:3306/xxxx?useUnicode=true&characterEncoding=UTF-8
#使用log4jdbc后oracle的url
#spring.datasource.url: jdbc:log4jdbc:oracle:thin:@127.0.0.1:1521:orcl

```
注意需要添加`spring.datasource.driver-class-name` 和更改 `spring.datasource.url` 将jdbc改为 jdbc:log4jdbc

*log4jdbc.properties*可以定义更多配置

```ini
#配置为需要记录的包或类匹配路径
#log4jdbc.debug.stack.prefix=com.drp
#log4jdbc加载的drivers (驱动名)
#log4jdbc.drivers=oracle.jdbc.OracleDriver
log4jdbc.auto.load.popular.drivers=true
#在日志中显示warn警告
log4jdbc.statement.warn=true
#毫秒值.执行时间超过该值的SQL语句将被记录为warn级别.
log4jdbc.sqltiming.warn.threshold=2000
#毫秒值.执行时间超过该值的SQL语句将被记录为error级别.
log4jdbc.sqltiming.error.threshold=3000
#是把boolean记录为 'true'/'false' 还是 1/0. 默认设置为false,不启用,为了移植性.
#log4jdbc.dump.booleanastruefalse=true
#输出的sql,一行最大的字符数，默认90. 以后新版可能为0
#log4jdbc.dump.sql.maxlinelength=90
#如果在调试模式下转储，则转储整个堆栈跟踪  默认false
log4jdbc.dump.fulldebugstacktrace=false

#是否记录某些类型的语句，默认true
log4jdbc.dump.sql.select=true
log4jdbc.dump.sql.insert=true
log4jdbc.dump.sql.delete=true
log4jdbc.dump.sql.update=true
log4jdbc.dump.sql.create=true

#输出sql末尾处加入分号，默认false
log4jdbc.dump.sql.addsemicolon=true

#将此设置为false以不修剪已记录的SQL
log4jdbc.trim.sql=true
#将此设置为false不删除额外的空行
log4jdbc.trim.sql.extrablanklines=true

#log4jdbc.suppress.generated.keys.exception=false


```

- ✔️ 可以显示sql
- ✔️ 不能和参数一起显示
- ✔️ 不能显示limit参数
- ❌ 能计数
- ✔️  能记录单个sql耗时
- ❌ 不能统计总耗时
  
不足的是，单纯log4jdbc并不能满足所有。理论上log4jdbc+org.hibernate.EmptyInterceptor可以满足需求了

## P6Spy

测试完毕，发现P6Spy目前最能满足需求：

- ✔️ 可以显示sql
- ✔️ 不能和参数一起显示
- ✔️ 不能显示limit参数
- ✔️ 能计数
- ✔️ 不能记录耗时
- ✔️ 支持curd事件前后钩子，钩子参数返回sql和执行耗时及异常信息🚀

```xml
        <dependency>
            <groupId>p6spy</groupId>
            <artifactId>p6spy</artifactId>
            <version>3.9.1</version>
        </dependency>

```
同`log4jdbc`需要改driver和url

```ini
spring.datasource.driver-class-name=com.p6spy.engine.spy.P6SpyDriver
spring.datasource.url=jdbc:p6spy:mysql://localhost:3306/test?useLegacyDatetimeCode=false&serverTimezone=UTC
```

*psy.properties*可以定义更多配置

```ini
#modulelist=com.p6spy.engine.spy.P6SpyFactory,com.p6spy.engine.logging.P6LogFactory,com.p6spy.engine.outage.P6OutageFactory
modulelist=com.vison.itdoc.config.CustomeP6Factory,com.p6spy.engine.logging.P6LogFactory,com.p6spy.engine.outage.P6OutageFactory
#moduelist很关键，我这里使用了自定义的Factory，因为我需要自定义event
appender=com.p6spy.engine.spy.appender.Slf4JLogger
logMessageFormat=com.p6spy.engine.spy.appender.CustomLineFormat
customLogMessageFormat=%(executionTime) ms|%(category)|%(sql)
excludecategories=result,resultset,info,debug
```

正常使用默认配置就可以显示出sql和耗时信息

```
 4 ms|statement|select admin0_.id as id1_0_, admin0_.create_time as create_t2_0_, admin0_.modify_time as modify_t3_0_, admin0_.email as email4_0_, admin0_.password as password5_0_, admin0_.status as status6_0_, admin0_.username as username7_0_ from admin admin0_ where admin0_.username='root'
```

可以看到，耗时信息和实际参数

### 自定义事件


`modulelist=com.p6spy.engine.spy.P6SpyFactory`改成`自定义Factory`

自定义Factory

```java
public class CustomeP6Factory implements com.p6spy.engine.spy.P6Factory {

    @Override
    public P6LoadableOptions getOptions(P6OptionsRepository optionsRepository) {
        return new P6SpyOptions(optionsRepository);
    }

    @Override
    public JdbcEventListener getJdbcEventListener() {
        return new P6spyListener(); //使用自定义Listener
    }

}

```

自定义事件

```java
public class P6spyListener extends JdbcEventListener {

    @Override
    public void onAfterExecuteQuery(PreparedStatementInformation statementInformation, long timeElapsedNanos, SQLException e) {
        App.sqlCount.incrementAndGet();
        Log.info("execute query...", statementInformation.getSqlWithValues());
    }

    @Override
    public void onAfterExecuteUpdate(PreparedStatementInformation statementInformation, long timeElapsedNanos, int rowCount, SQLException e) {
        App.sqlCount.incrementAndGet();
        Log.info("execute update..", statementInformation.getSqlWithValues());
    }

    @Override
    public void onAfterExecute(StatementInformation statementInformation, long timeElapsedNanos, String sql, SQLException e) {
        Log.info("execute..", statementInformation.getSqlWithValues());
    }

}
```

可以看到，我在自定义事件中进行了sql计数.于是我可以在请求结束时打印每次请求的总sql执行次数。

```java
public class RequestInitInterceptor implements HandlerInterceptor {

    public RequestInitInterceptor() {
    }

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler)
            throws Exception {
        App._uniq_req_no = UUID.randomUUID().toString();
        App.sqlCount = new AtomicInteger(0);
        Log.setMsgTraceNo(App._uniq_req_no);
        Log.info("request start...", handler);
        return true;
    }

    @Override
    public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex)
            throws Exception {
        Log.info(String.format("finish request sql执行次数:%s", App.sqlCount));
    }

}
```

由于事件参数还给出了`timeElapsedNanos`,最终我们还能统计出所有sql执行的耗时。这样一来我们就能看出一次请求内，最耗时的操作具体是什么。达到类似以下效果：

![](https://vison-blog.oss-cn-beijing.aliyuncs.com/20210224141855.png)



