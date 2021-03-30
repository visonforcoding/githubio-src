---
title: '[spring源码]SpringApplication'
date: 2021-03-16 21:40:49
tags: java
---


## 概览

可用于从Java main引导和启动Spring应用程序的类。
默认情况下，类将执行以下步骤来引导您的应用：

  - 创建适当的`ApplicationContext`实例（取决于您的
  classpath）
  - 注册一个`CommandLinePropertySource`以将命令行参数为spring属性。
  - 刷新应用程序上下文，加载所有单例bean
  - 触发任何`CommandLineRunner`bean
  - 在大多数情况下，可以调用静态`run（Class，String [])`方法直接从您的{@literal main}方法引导您的应用程序.

```java
 @Configuration
 @EnableAutoConfiguration
 public MyApplication {
 
  // ... Bean定义
  public static void main（String [] args）{
  SpringApplication.run(MyApplication.class，args);
   }
 }
 ```

 对于更高级的配置，可以创建一个在运行前已自定义的`SpringApplication`实例：

```java
 public static void main(String[] args) {
    SpringApplication application = new SpringApplication(MyApplication.class);
    // ... customize application settings here
    application.run(args)
  }
```

  `SpringApplication`可以从各种不同的来源读取bean。
 通常建议使用单个`@Configuration`类进行引导
 您的应用程序，但是，您还可以从以下位置设置`getSources()`来源：
  
  - 要加载的完全限定的类名
`AnnotatedBeanDefinitionReader`
 - 由`XmlBeanDefinitionReader`加载的XML资源的位置，
 - `GroovyBeanDefinitionReader`加载的groovy脚本
 - `ClassPathBeanDefinitionScanner`要扫描的软件包的名称

 配置属性也绑定到`SpringApplication`这使它
 可以动态设置`SpringApplication`属性，例如其他
 *源（“ spring.main.sources”-CSV列表）用于指示Web环境的标志
 `spring.main.web-application-type = none`或关闭横幅广告的标志
 `spring.main.banner-mode = off`
