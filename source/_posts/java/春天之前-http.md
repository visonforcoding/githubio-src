---
title: 春天之前-http
tags: java
---


> 试图跳过spring,而学习spring boot是不可能的。学习java web开发，从基础开始学习。就应当了解http、servlet、tomcat

- 起源
- 它解决什么问题
- 实现原理
  
# 起源

1980年6月至12月间，伯纳斯-李在的CERN（欧洲核子研究组织）担任工作。实验室的研究人员需要大量的信息查阅或沟通。在那段时间里，他提出了个构想：创建一个以超文本系统为基础的项目，方便研究人员分享及更新讯息。

1989年3月，他写下了他的初步构想，并在1990年重新配置。然后被他的经理麦克·森德尔（Mike Sendall）所接受。他使用与ENQUIRE系统相似的概念来创建万维网，为此他设计并构建了第一个网页浏览器。

世界上第一个网站在CERN搭建，而CERN则位于法国边境。网站在1991年8月6日上线。

上线 的第一个网址，http://info.cern.ch/hypertext/WWW/TheProject.html 告诉人们万维网是什么，用户如何使用浏览器，如何创建网页服务器。

# 目的

设计HTTP最初的目的是为了提供一种发布和接收HTML页面的方法。

![](https://vison-blog.oss-cn-beijing.aliyuncs.com/20201218163846.png)

# 实现

一个连接是由传输层来控制的，这从根本上不属于HTTP的范围。HTTP并不需要其底层的传输层协议是面向连接的，只需要它是可靠的，或不丢失消息的（至少返回错误）。在互联网中，有两个最常用的传输层协议：TCP是可靠的，而UDP不是。因此，HTTP依赖于面向连接的TCP进行消息传递，但连接并不是必须的。因此通过socket编程就能实现http协议。

```java
public class Server {

    private static int port = 8081;

    public static void main(String[] args) throws IOException {
        ServerSocket ss = new ServerSocket(port); // 监听指定端口
        System.out.println("server is running...");
        for (;;) {
            Socket sock = ss.accept();
            System.out.println("connected from " + sock.getRemoteSocketAddress());
            Thread t = new Handler(sock);
            t.start();
        }
    }

}

public class Handler extends Thread {

    Socket sock;

    public Handler(Socket sock) {
        this.sock = sock;
    }

    public void run() {
        try ( InputStream input = this.sock.getInputStream()) {
            try ( OutputStream output = this.sock.getOutputStream()) {
                handle(input, output);
            }
        } catch (Exception e) {
            try {
                this.sock.close();
            } catch (IOException ioe) {
            }
            System.out.println("client disconnected.");
        }
    }

    private void handle(InputStream input, OutputStream output) throws IOException {
        System.out.println("Process new http request...");
        var reader = new BufferedReader(new InputStreamReader(input, StandardCharsets.UTF_8));
        var writer = new BufferedWriter(new OutputStreamWriter(output, StandardCharsets.UTF_8));
        // 读取HTTP请求:
        boolean requestOk = false;
        String first = reader.readLine();
        if (first.startsWith("GET / HTTP/1.")) {
            requestOk = true;
        }
        for (;;) {
            String header = reader.readLine();
            if (header.isEmpty()) { // 读取到空行时, HTTP Header读取完毕
                break;
            }
            System.out.println(header);
        }
        System.out.println(requestOk ? "Response OK" : "Response Error");
        if (!requestOk) {
            // 发送错误响应:
            writer.write("HTTP/1.0 404 Not Found\r\n");
            writer.write("Content-Length: 0\r\n");
            writer.write("\r\n");
            writer.flush();
        } else {
            // 发送成功响应:
            String data = "<html><body><h1>Hello, world!</h1></body></html>";
            int length = data.getBytes(StandardCharsets.UTF_8).length;
            writer.write("HTTP/1.0 200 OK\r\n");
            writer.write("Connection: close\r\n");
            writer.write("Content-Type: text/html\r\n");
            writer.write("Content-Length: " + length + "\r\n");
            writer.write("\r\n"); // 空行标识Header和Body的分隔
            writer.write(data);
            writer.flush();
        }
        // TODO: 处理HTTP请求
    }

}
```

# 参考

- https://developer.mozilla.org/zh-CN/docs/Web/HTTP



