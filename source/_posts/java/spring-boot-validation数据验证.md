---
title: spring-boot validation数据验证
date: 2020-09-14 22:40:18
tags: spring-boot
---

![](http://img.rc5j.cn/blog20200914225941.png)

做业务处理，不可避免的要对参数进行校验，一套完整规范的校验体系可以提高不少的效率。

在写了PHP、java、python 等编程语言之后，我发现java的优势就是它的规范、它的严谨。在`jsr`之下建立各种场景的标准，所有人都在这套规范下拓展、迭代、升级。最终这套体系变得越来越完美、符合体系的生态产品也越来越多。 这大概就是java最强之处吧。

本节介绍下spring-boot的验证，它也是基于`jsr`的validation之下。

<!--more-->

## 依赖

```xml
    <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
      <dependency> 
            <groupId>org.springframework.boot</groupId> 
            <artifactId>spring-boot-starter-validation</artifactId> 
        </dependency>
        <dependency>
            <groupId>javax.validation</groupId>
            <artifactId>validation-api</artifactId>
            <version>2.0.1.Final</version>
            <type>jar</type>
        </dependency>
```
javax.validation 正是 jsr的规范。

## 定义验证规则

```java
    @NotBlank(message = "用户名不可为空")
    @NotNull(message = "不可为空")
    private String username;

    @NotBlank(message = "密码不可为空")
    @NotNull(message = "密码不可为空")
    private String pwd;
```

## controller使用

```java
 public Response login(@Valid @RequestBody LoginInfo loginInfo, HttpServletRequest request, HttpSession session) {

 }


```
这里要对`@Valid` 进行使用

## 全局处理

```java
 
@RestControllerAdvice
public class ControllerAdvice {

    /**
     * ConstraintViolationException
     */
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public Response handleConstraintViolationException(MethodArgumentNotValidException ex) {
        Map<String, String> errors = new HashMap<>();
        ex.getBindingResult().getAllErrors().forEach((error) -> {
            String fieldName = ((FieldError) error).getField();
            System.out.println(fieldName);
            String errorMessage = error.getDefaultMessage();
            errors.put(fieldName, errorMessage);
            System.out.println(errorMessage);
        });
        return new Response(ResponseCode.parametrErrror, "参数错误", errors);
    }

}
```
由于使用`@Valid`对参数进行校验之后，如果有校验不通过会抛出一个`MethodArgumentNotValidException`异常。全局进行捕获之后可以全局处理参数不正确的情况。


## 参考

https://www.cnblogs.com/fqybzhangji/p/10384347.html


