---
title: servlet | servlet学习笔记
date: 2021-11-28 12:10:18
tags: java
---
## 定义

![](https://vison-blog.oss-cn-beijing.aliyuncs.com/20211128120653.png)

简单而言，Servlet是一个API，本质上的实现是由承载的Servlet容器去处理。通过Java多线程处理并响应客户端的Http Request。

<!--more-->

## 历史

![](https://vison-blog.oss-cn-beijing.aliyuncs.com/20211128105759.png)

截止目前，最新版本规范为6.0。

## 过滤器 Filter

在HTTP请求到达Servlet之前，可以被一个或多个Filter预处理，类似打印日志、登录检查等逻辑，完全可以放到Filter中。

![](https://vison-blog.oss-cn-beijing.aliyuncs.com/20211128110826.png)

Filter不光能拦截请求，对请求进行预处理，还能够修改返回。

![](https://vison-blog.oss-cn-beijing.aliyuncs.com/20211128111038.png)

## 事件监听器 Listener

Servlet 侦听器用于侦听 Web 容器中的事件，例如，当您创建会话时，或在会话中放置属性时，或者如果您在另一个容器中被动化并激活时，要订阅这些事件，

![](https://vison-blog.oss-cn-beijing.aliyuncs.com/20211128111619.png)

### 事件类型

1. **javax.servlet.AsyncEvent** – 在 ServletRequest 上启动的异步操作（通过调用 ServletRequest#startAsync 或ServletRequest#startAsync（ServletRequest， ServletResponse））完成、超时或产生错误时触发的事件。

2. **javax.servlet.http.HttpSessionBindingEvent** – 当会话绑定或取消绑定 HttpSessionListener 时，这种类型的事件要么发送到实现 HttpSessionBindingListener 的对象，要么发送到在 Web 中配置的 

3. **HttpSessionAttributeListener**当任何属性在会话中被绑定、取消绑定或替换时。会话通过调用 HttpSession.setAttribute 绑定对象，并通过调用 HttpSession.removeAttribute 解除绑定对象。
当对象从会话中删除时，我们可以将此事件用于清理活动。

4. **javax.servlet.http.HttpSessionEvent** – 这是一个类，表示 Web 应用程序中会话更改的事件通知。

5. **javax.servlet.ServletContextAttributeEvent** – 事件类，用于通知有关 Web 应用程序 ServletContext 属性的更改。

6. **javax.servlet.ServletContextEvent**– 这是有关 Web 应用程序 servlet 上下文更改的通知的事件类。

7. **javax.servlet.ServletRequestEvent** – 此类事件表示 ServletRequest 的生命周期事件。该事件的源是此 Web 应用程序的 ServletContext。

8. **javax.servlet.ServletRequestAttributeEvent**– 这是一个事件类，用于通知应用程序中 servlet 请求的属性的更改。


## 注解

在2005年的servlet 2.5中引入了注解能力，可以不再配置太多xml。

`@WebServlet` 

声明java类为servlet

`@WebInitParam` 

作为`WebServlet`参数注解。初始化serverl参数。

```java
@WebServlet(
  name = "BankAccountServlet", 
  description = "Represents a Bank Account and it's transactions", 
  urlPatterns = {"/account", "/bankAccount" }, 
  initParams = { @WebInitParam(name = "type", value = "savings")})
public class AccountServlet extends javax.servlet.http.HttpServlet {

    String accountType = null;

    public void init(ServletConfig config) throws ServletException {
        accountType = config.getInitParameter("type");
    }

    public void doPost(HttpServletRequest request, HttpServletResponse response) 
      throws IOException {
        // ...
    }
}
```

`@WebFilter`

声明过滤器，如果要对请求进行拦截、修改而不影响逻辑代码。

```java
@WebFilter(
  urlPatterns = "/account/*",
  filterName = "LoggingFilter",
  description = "Filter all account transaction URLs")
public class LogInFilter implements javax.servlet.Filter {
    
    public void init(FilterConfig filterConfig) throws ServletException {
    }

    public void doFilter(
        ServletRequest request, ServletResponse response, FilterChain chain) 
          throws IOException, ServletException {
        HttpServletRequest req = (HttpServletRequest) request;
        HttpServletResponse res = (HttpServletResponse) response;

        res.sendRedirect(req.getContextPath() + "/login.jsp");
        chain.doFilter(request, response);
    }

    public void destroy() {
    }

}
```

`@WebListener`

声明事件监听器。

```java
@WebListener
public class BankAppServletContextListener 
  implements ServletContextListener {

    public void contextInitialized(ServletContextEvent sce) { 
        sce.getServletContext().setAttribute("ATTR_DEFAULT_LANGUAGE", "english"); 
    } 
    
    public void contextDestroyed(ServletContextEvent sce) { 
        // ... 
    } 
}
```

`@ServletSecurity`、`@HttpConstraint`、`@HttpMethodConstraint`

类似nginx认证功能


`@MultipartConfig`

处理文件上传配置

```java
@WebServlet(urlPatterns = { "/uploadCustDocs" })
@MultipartConfig(
  fileSizeThreshold = 1024 * 1024 * 20,
  maxFileSize = 1024 * 1024 * 20,
  maxRequestSize = 1024 * 1024 * 25,
  location = "./custDocs")
public class UploadCustomerDocumentsServlet extends HttpServlet {

    protected void doPost(HttpServletRequest request, HttpServletResponse response) 
      throws ServletException, IOException {
        for (Part part : request.getParts()) {
            part.write("myFile");
        }
    }

}
```


## 参考阅读

1. [https://o7planning.org/10395/java-servlet-filter](https://o7planning.org/10395/java-servlet-filter)
2. [https://www.codejava.net/java-ee/servlet/how-to-modify-http-response-using-java-filter 如何使用filter修改response](https://www.codejava.net/java-ee/servlet/how-to-modify-http-response-using-java-filter)
3. [https://en.wikipedia.org/wiki/Jakarta_Servlet 维基servlet](https://en.wikipedia.org/wiki/Jakarta_Servlet)
4. [Java-web-注解 www.baeldung.com](https://www.baeldung.com/javaee-web-annotations)
5. [Java-servlets](https://www.simplilearn.com/tutorials/java-tutorial/java-servlets)

