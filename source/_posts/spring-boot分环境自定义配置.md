---
title: spring boot分环境自定义配置
date: 2020-05-26 13:03:36
tags: java spring-boot
---

在一般规模企业，应当都有测试环境和正式环境区别，或者至少也有开发环境和正式环境。那不同环境必然就会有一些环境依赖的不同，不管是出于安全性考虑还是其他原因导致的。比如数据库配置、OSS账号信息等。那程序当中就需要配置多份配置信息和根据不同环境使用不同配置。


<!--more-->

## 分环境配置


![](http://img.rc5j.cn/blog20200526133442.png)


```
# 激活日志环境
spring.profiles.active=prd
```

公共配置还是写在application。
相应配置写在-{env} 文件里。

## 自定义配置获取

上面是spring框架所需的默认配置方法，我们通常还需要非常多的自定义配置。比如密码的加盐salt等等，这是项目的自定义配置。

那如果对这些自定义内容进行配置和获取呢。


## 配置

我们依然可以在application.properties进行配置。

例如：

```properties
app.security.salt=zM2Y&*21.rkJr=11
app.oss.host=http://oss-cn-beijing.aliyuncs.com
app.oss.bucket=bucketNanme
app.oss.accessKey=accessKey
app.oss.accessSecret=accessSecret
```

## 获取配置

```java
@Service
public class OssService {

    @Value("${app.oss.host}")
    private String host;

    @Value("${app.oss.accessKey}")
    private String accessKeyId;

    @Value("${app.oss.accessSecret}")
    private String accessKeySecret;

    @Value("${app.oss.bucket}")
    private String bucketName;
}
```

**一定要是在spring bean里进行获取，否则无法获取到。**

## 参考


1. https://docs.spring.io/spring-boot/docs/1.5.22.RELEASE/reference/html/boot-features-external-config.html


