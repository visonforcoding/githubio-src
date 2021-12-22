---
title: spring-boot全局处理异常[兜底、防重]
date: 2021-12-22 19:26:38
tags: spring
---

网上有非常多的文章介绍了如何进行全局异常捕获处理，但是我发现并不满足我遇到的一个问题。

<!--more-->

## 案例

```java
    @GetMapping(name = "商品详情", path = "/goods/{id}")
    public Response detail(@PathVariable Long id) {
        Optional<Goods> goods = goodsRepository.findById(id);
        if (goods.isPresent()) {
            return new Response(ResponseCode.success, "获取成功", goods);
        }
        return new Response(ResponseCode.noDataFound, "获取失败");
    }
```

一个非常普通的api,查询并返回。

```java
  //Goods entity
   public String getPurchasingPrice() {
        return String.format("%d", this.purchasingPriceFen / 100);
    }
```

会出异常的点在于我的`Goods`的属性`purchasingPriceFen`有可能会出现`NullPointerException`.

此时的异常发生于jackson.databind.而控制器仍然会正常返回成功的json.

在常规的的`RestControllerAdvice`处理方法中

```java
@RestControllerAdvice
@Slf4j
public class ControllerAdvice {

    private Response handleConstraintViolationException(MethodArgumentNotValidException ex) {
        Map<String, String> errors = new HashMap<>();
        ex.getBindingResult().getAllErrors().forEach((error) -> {
            String fieldName = ((FieldError) error).getField();
            String errorMessage = error.getDefaultMessage();
            errors.put(fieldName, errorMessage);
        });
        return new Response(ResponseCode.parametrErrror, "参数错误", errors);
    }

    @ExceptionHandler(Exception.class)
    public Response handBaseException(Exception ex, HttpServletResponse response) {
        if (ex instanceof MethodArgumentNotValidException) {
            return handleConstraintViolationException((MethodArgumentNotValidException) ex);
        }
        log.error(ex.getMessage());
        Map<String, StackTraceElement[]> errors = new HashMap<>();
        errors.put("errors", ex.getStackTrace());
        return new Response(ResponseCode.systemError, ex.getMessage(), errors);
    }
}
```

会导致先输出正常的json，后面又会输出捕获的异常的错误json，最终2个json串叠加输出。

## 解决办法

我找了许多文章都没有解决这个问题,后面想到了正常的情况下前面的json是不应该输出的，那么把它清除不就行了？

于是最终的兜底方式是

```java
    @ExceptionHandler(Exception.class)
    public Response handBaseException(Exception ex, HttpServletResponse response) throws Exception {
        if (ex instanceof MethodArgumentNotValidException) {
            return handleConstraintViolationException((MethodArgumentNotValidException) ex);
        }
        log.error(ex.getMessage());
        response.reset();  //关键方法
        response.setStatus(500);
        Map<String, StackTraceElement[]> errors = new HashMap<>();
        errors.put("errors", ex.getStackTrace());
        return new Response(ResponseCode.systemError, ex.getMessage(), errors);
    }
```

通过`response.reset()`重置掉response。

关于完整的异常处理可参考:[https://spring.io/blog/2013/11/01/exception-handling-in-spring-mvc](https://spring.io/blog/2013/11/01/exception-handling-in-spring-mvc)
