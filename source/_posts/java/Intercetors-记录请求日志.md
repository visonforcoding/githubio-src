---
title: 'Servlet Filiter 和 Spring Intercetors,记录请求日志'
date: 2021-12-02 10:46:17
tags: java
---
> 在前面的文章我们有看到Servlet Filiter的作用。与之类似的Spring中我们知道有拦截器Intercetors。

现在有1个需求，记录request的所有请求信息，URL、请求方法、请求体。我们自然而然会想到使用`Filiter`或`Intercetors`

![](https://vison-blog.oss-cn-beijing.aliyuncs.com/20211201133516.png)

`Filiter`和`Intercetors`的区别在于所执行的时间点不同，但都在到达controller之前。看起来二者都可以完成这个需求。

<!--more-->

我们先来看下Filiter。Spring当中本身支持servlet的几个注解。

>When using an embedded container, automatic registration of classes annotated with @WebServlet, @WebFilter, and @WebListener can be enabled by using @ServletComponentScan.

但是他也说了，如果要保证顺序，需要通过定义`FilterRegistrationBean`的方式。

> you must define a FilterRegistrationBean for the Filter and set the registration bean’s order using the setOrder(int) method.


**不管是Filiter还是Intercetors都是需要拿到request,从request获取要记录的信息。当要记录请求体的时候，在Java IO当中有个最大的问题是如果一旦`request.getInputStream()` 后面就会读取不到请求体**，并抛出`HttpMessageNotReadableException: Required request body is missing` 异常。

Spring本身提供记录请求体的Filiter `AbstractRequestLoggingFilter`,我们可以继承并自定义。

```java
public class CustomizedRequestLoggingFilter extends AbstractRequestLoggingFilter {
    @Override
    protected void beforeRequest(HttpServletRequest request, String message) {

    }

    @Override
    protected void afterRequest(HttpServletRequest request, String message) {
        log.info(message);
    }
}
```

启用该`bean`

```java
@Configuration
@Slf4j
public class FilterConfigure {

    @Bean
    public FilterRegistrationBean<LogFilter> logFilter() {
        // 利用 slf4j.MDC 记录 唯一请求码
        FilterRegistrationBean<LogFilter> bean = new FilterRegistrationBean<LogFilter>();
        bean.setFilter(new LogFilter());
        bean.addUrlPatterns("/*");//过滤所有路径
        bean.setOrder(1);
        return bean;
    }



    @Bean
    public CustomizedRequestLoggingFilter logInitFilter() {
        //原生bean记录请求信息 请求体
        log.info("logInitFilter...");
        CustomizedRequestLoggingFilter filter
                = new CustomizedRequestLoggingFilter();
        filter.setIncludeClientInfo(true);
        filter.setIncludeQueryString(true);
        filter.setIncludePayload(true);
        filter.setMaxPayloadLength(2048);
        filter.setIncludeHeaders(false);
        filter.setAfterMessagePrefix("REQUEST DATA : ");
        return filter;
    }

}
```

但是原生的`AbstractRequestLoggingFilter`提供的Message格式已经固定，并不能根据自己的喜好来。

![](https://vison-blog.oss-cn-beijing.aliyuncs.com/20211202103252.png)

而且换行符没被转义，虽然便于调试观察但并不利于ELK这样的日志体系记录日志。

要解决这个问题就需要自己读取request并记录，就必须解决上文提到的`request.getInputStream()` stream读取问题。

解决办法网上也有，就是通过拷贝一份stream，将拷贝的stream继续扔回`FilterChain`。示例代码如下

```java
    @Bean
    public FilterRegistrationBean<LogClientFilter> logClientFilter() {
        //自定义的 request log filter
        FilterRegistrationBean<LogClientFilter> bean = new FilterRegistrationBean<LogClientFilter>();
        bean.setFilter(new LogClientFilter());
        bean.addUrlPatterns("/*");
        bean.setOrder(3);
        return bean;
    }
```

关键的MultiRead对象

```java
public class MultiReadHttpServletRequest extends HttpServletRequestWrapper {
    private ByteArrayOutputStream cachedBytes;

    /**
     * Construct a new multi-read wrapper.
     *
     * @param request to wrap around
     */
    public MultiReadHttpServletRequest(HttpServletRequest request) {
        super(request);
    }

    @Override
    public ServletInputStream getInputStream() throws IOException {
        if (cachedBytes == null) cacheInputStream();

        return new CachedServletInputStream(cachedBytes.toByteArray());
    }

    @Override
    public BufferedReader getReader() throws IOException {
        return new BufferedReader(new InputStreamReader(getInputStream()));
    }

    private void cacheInputStream() throws IOException {
        /* Cache the inputstream in order to read it multiple times. For
         * convenience, I use apache.commons IOUtils
         */
        cachedBytes = new ByteArrayOutputStream();
        IOUtils.copy(super.getInputStream(), cachedBytes);
    }

    /* An inputstream which reads the cached request body */
    private static class CachedServletInputStream extends ServletInputStream {
        private final ByteArrayInputStream buffer;

        public CachedServletInputStream(byte[] contents) {
            this.buffer = new ByteArrayInputStream(contents);
        }

        @Override
        public int read() throws IOException {
            return buffer.read();
        }

        @Override
        public boolean isFinished() {
            return buffer.available() == 0;
        }

        @Override
        public boolean isReady() {
            return true;
        }

        @Override
        public void setReadListener(ReadListener listener) {
            throw new RuntimeException("Not implemented");
        }
    }
}

```

日志记录Filiter


```java
public class LogClientFilter implements Filter {
    public void init(FilterConfig config) throws ServletException {
        log.info("log client...");
    }

    public void destroy() {
    }

    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain) throws ServletException, IOException {
        ObjectMapper mapper = new ObjectMapper();
        ObjectNode rootNode = mapper.createObjectNode();
        HttpServletRequest httpServletRequest = (HttpServletRequest) request;
        MultiReadHttpServletRequest wrappedRequest =
                new MultiReadHttpServletRequest(httpServletRequest);
        request.getInputStream();
        rootNode.put("uri", httpServletRequest.getRequestURI());
        rootNode.put("clientIp", httpServletRequest.getRemoteAddr());
        String method = httpServletRequest.getMethod();
        rootNode.put("method", method);
        String content = IOUtils.toString(wrappedRequest.getInputStream());
        if (method.equals("GET") || method.equals("DELETE")) {
            rootNode.put("request", httpServletRequest.getQueryString());
        } else {
            rootNode.put("request",content);
        }
        log.info(rootNode.toString());
        chain.doFilter(request, response);
    }

}
```



## 参考

1. [https://www.jvt.me/posts/2020/05/25/read-servlet-request-body-multiple/ 多次读取servlet请求体](https://www.jvt.me/posts/2020/05/25/read-servlet-request-body-multiple/)
2. [https://www.javadevjournal.com/spring/log-incoming-requests-spring/ 记录spring的请求](https://www.javadevjournal.com/spring/log-incoming-requests-spring/)
3. [https://levelup.gitconnected.com/how-to-log-the-request-body-in-a-spring-boot-application-10083b70c66](https://levelup.gitconnected.com/how-to-log-the-request-body-in-a-spring-boot-application-10083b70c66)
4.   [https://stackoverflow.com/questions/54035778/commonsrequestloggingfilter-not-working-in-spring-boot-application/54545890#](https://stackoverflow.com/questions/54035778/commonsrequestloggingfilter-not-working-in-spring-boot-application/54545890#)