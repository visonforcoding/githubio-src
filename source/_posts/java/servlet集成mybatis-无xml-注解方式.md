---
title: servlet | servlet集成mybatis-无xml&注解方式
date: 2021-01-06 16:14:24
tags: java
---

> 习惯了php项目之后，恐怕非常不喜欢操作xml吧.本章将介绍servlet+mybatis无xml配置模式。
<!--more-->

## 依赖

```xml
     <dependency>
            <groupId>mysql</groupId>
            <artifactId>mysql-connector-java</artifactId>
            <version>5.1.26</version>
        </dependency>
        <!-- https://mvnrepository.com/artifact/org.mybatis/mybatis -->
        <dependency>
            <groupId>org.mybatis</groupId>
            <artifactId>mybatis</artifactId>
            <version>3.5.6</version>
        </dependency>
```

## 引入

首先定义datasource

```java
public class DatabaseConfig {

    static String driver = "com.mysql.jdbc.Driver";
    static String url = "jdbc:mysql://localhost:3306/db_itdoc?useSSL=false";
    static String username = "root";
    static String password = "12345678";

    public static DataSource getDataSource() {
        Properties properties = new Properties();
        properties.setProperty("driver", driver);
        properties.setProperty("url", url);
        properties.setProperty("username", username);
        properties.setProperty("password", password);
        UnpooledDataSourceFactory unpooledDataSourceFactory = new UnpooledDataSourceFactory();
        unpooledDataSourceFactory.setProperties(properties);
        DataSource dataSource = unpooledDataSourceFactory.getDataSource();
        return dataSource;
    }
}
```

获取sessionFactory

```java
public class MybatisLoader {

    static SqlSessionFactory sqlSessionFactory = null;

    public static SqlSessionFactory getSqlSessionFactory() {
        if (sqlSessionFactory == null) {
            DataSource dataSource = DatabaseConfig.getDataSource();
            TransactionFactory transactionFactory
                    = new JdbcTransactionFactory();
            Environment environment
                    = new Environment("development", transactionFactory, dataSource);
            Configuration configuration = new Configuration(environment);
            configuration.addMapper(UserMapper.class);
            sqlSessionFactory
                    = new SqlSessionFactoryBuilder().build(configuration);
        }
        return sqlSessionFactory;
    }

}
```

## 定义mapper

```java
public interface UserMapper {

    @Select("SELECT * FROM user WHERE id = #{id}")
    User selectUser(int id);

    @Insert("INSERT INTO user(name,email) VALUES(#{name}, #{email})")
    int insertUser(User user);

}
```

## 查询和插入

```java
public class UserController {

    public UserController() {
    }

    @GetMapping(path = "/user/profile")
    public String profile(HttpServletRequest request, HttpServletResponse response) {
        System.out.print(request.getCookies());
        return "i am user profile";
    }

    @GetMapping(path = "/user")
    public Response user(HttpServletRequest request, int id) {
        User user = null;
        SqlSession session = MybatisLoader.getSqlSessionFactory().openSession();
        UserMapper mapper = session.getMapper(UserMapper.class);
        user = mapper.selectUser(id);
        return new Response(0, "获取成功", user);
    }

    @PostMapping(path = "/user/add")
    public Response add(User user) {
        Log.info("request user", user);
        try {
            SqlSession session = MybatisLoader.getSqlSessionFactory().openSession();
            UserMapper mapper = session.getMapper(UserMapper.class);
            int id = mapper.insertUser(user);
            session.commit();
            Log.debug("返回", id);
        } catch (Exception e) {
            Log.error("保存失败", e);
        }
        return new Response(0, "保存", user);
    }
}

```