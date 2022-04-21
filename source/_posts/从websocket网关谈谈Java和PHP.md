---
title: 从websocket网关谈谈Java和PHP
date: 2022-04-21 17:34:46
tags:
---

> 前面的文章我们讲到了如何实现WebSocket协议，从基础的socket API进行了协议的实现。也了解了如何用更便利的eventIO编写websocket应用。我们分别用Java和php实现了基础班本和事件驱动版本的websocket协议。

戳[基础|websocket协议](https://visonforcoding.xyz/2022/04/06/%E5%9F%BA%E7%A1%80-websocket%E5%8D%8F%E8%AE%AE/)查看。

- 我们通过java socket原生实现了websocket协议
- 我们通过`Ratchet`构建了php版本的事件驱动型websocket server。
- 通过`TooTallNate / Java-WebSocket`也可以构建事件驱动的websocket

本文将会进行一次升级，构建通用型的websocket网关来解决公司内多场景对websocket的需求。

## 场景

### 扫码支付通知

用户扫描网页二维码,当服务端接受到微信或支付宝的支付回调之后，通过websocket通知用户网页显示支付成功页面。

### 上传文件后台处理

后端运营人员,要导入百万的数据进行后台处理,上传成功后页面列表显示的是后台处理中，服务端在异步进行任务处理.为了提升用户体验，每处理1个任务可以websocket通知页面进度条变更。

## 需求

公司业务规模扩大，会有越来越多的类似场景出现。抽象出需求就是**耗时任务后台处理的websock通知**

## 设计

![](https://vison-blog.oss-cn-beijing.aliyuncs.com/20220421180158.png)

cswg: 通用websocket服务网关,包含一套http服务，一套websocket服务

http服务: 接收业务调用,告知业务处理状态。并通过MQ通知到WebSocket服务下发业务消息

websocket服务:不处理具体业务逻辑，只做与客户端的消息交互

业务服务:处理具体业务,业务客户端与websocket消息交互获取任务处理过程状态

期中websocket服务应该包含2个子任务：

- websocket 消息交互
- 消费MQ消息做消息下发动作

## 问题

websocket服务的2个子任务，都需要阻塞进程。一个是阻塞获取MQ数据，一个是阻塞提供websocket服务。并且2个子任务需要对象共享。消费MQ的任务需要获取websocket的服务对象进行广播消息。因此我们需要2个进程或线程,并且需要共享内存。

PHP语言当前的并发模型是多进程处理,而进程间无法共享内存。我想到通过redis做为中间件的形式进行对象共享，但实际上一是引入了依赖。第二个是对象序列号,如果对象方法中包含匿名方法做参的情况，当前我还没找到能序列化的办法。

`opis/closure`能很好的支持匿名函数的序列号，对于上述包含匿名函数做参的对象无法序列化。

线程之间的内存共享是天生的非常简单的。PHP的线程支持方面有`pthreads`和`parallel`2个拓展支持。

### pthreads

![](https://vison-blog.oss-cn-beijing.aliyuncs.com/20220421190454.png)

本来似乎`pthreads`可以支持需求。但是不幸的是，该扩展已经是不维护状态。官方建议的是使用`parallel`拓展。

### parallel

我看了`parallel`的设计理念,还是为了避免传统线程模型当中的需要花大精力处理共享内存的状态一致问题。

`parallel`在官方网页当中讲到了它的理念来自于`Go`.
并且对GO的评价是
> one of the most widely admired if not used platforms for writing parallel code at the moment

Go的主要理念

`Do not communicate by sharing memory; instead, share memory by communicating.(a variable is passed over a Channel for example).`

解释下就是摒弃传统模型当中的通过共享内存来进行对象交流，而是利用一种通道的传输来交流对象。

坦白说，话有点饶。我的理解就是首先它是为了规避传统线程模型的问题。让程序员能够更方便地些并行程序的编写。
程序员不用再考虑多线程的数据并发操作问题。

上述说的理念就是CSP模型,CSP (message passing over channels).

当探讨CSP模型的时候，传统程序员可能会在寻找并发数据结构,但是这在CSP模型当中是不需要的。CSP的另一个核心思想是`Data should have a definitive single owner`.数据应该有明确的单一所有者。数据的改变需要通过`channels`进行通信同步。

`parallel`目前在PHP生态中应用很少,网上也很少有代码介绍。测试了几次，结果都不是很理想。也许过些日子，等自己能力变得更强或者`parallel`被更多人尝试的时候，它会变得更简单。

更多并发模型可参考[Concurrency Models](https://tianpan.co/notes/181-concurrency-models),我认识的一个网友的总结。不一定都对，但是很全面。

## java实现

上面也说到，传统的线程模型虽然存在共享数据的并发操作问题。但是在不考虑这个问题的前提下，实现我们上述的需求却是非常简单的事情。

启动2个线程,一个线程用户监听MQ,一个线程启动websocket服务。以下是示例demo:

```java
//main.java
        String host = "localhost";
        int port = 8088;
        WebSocketServer server = new WsServer(new InetSocketAddress(host, port));
        Thread wsServerThread = new Thread(server,"wsServerThread");
        wsServerThread.start();
        MqWatcher mqWatcher = new MqWatcher();
        mqWatcher.setWebSocketServer(server);
        Thread mqWatcherThread = new Thread (mqWatcher, "mqWatcherThread");
        mqWatcherThread.start();
```

启动2个线程,`wsServerThread`用户监听websocket连接。
`mqWatcherThread`用户监听mq消息。

```java
public class MqWatcher implements Runnable {

    private final static String QUEUE_NAME = "ws.notice";

    private WebSocketServer webSocketServer;

    public void setWebSocketServer(WebSocketServer webSocketServer) {
        this.webSocketServer = webSocketServer;
    }

    @Override
    public void run() {
        ConnectionFactory factory = new ConnectionFactory();
        factory.setHost("localhost");
        factory.setPort(5672);
        Connection connection = null;
        try {
            connection = factory.newConnection();
            Channel channel = connection.createChannel();

            channel.queueDeclare(QUEUE_NAME, false, false, false, null);
            System.out.println(" [*] Waiting for messages. To exit press CTRL+C");

            DeliverCallback deliverCallback = (consumerTag, delivery) -> {
                String message = new String(delivery.getBody(), StandardCharsets.UTF_8);
                System.out.println(" [x] Received '" + message + "'");
                webSocketServer.broadcast(message);
            };
            channel.basicConsume(QUEUE_NAME, true, deliverCallback, consumerTag -> { });
        } catch (Exception e) {
            e.printStackTrace();
        }

    }
}
```

`MqWatcher`一旦收到mq的消息就广播给所有客户端。

基于这个简单的demo模型，再进行拓展应该就能满足需求了。

## 总结

- 我花了很长时间在思考如何基于现有PHP生态(除开swoole),进行需求的实现，发现挺难的。
- 使用Java却轻而易举地实现了需求。
- PHP在应对一般性的数据处理：存储、查询、修改、删除、格式化等工作上效率很高、很容易，但是在应对编写并发网络服务程序时会显得特别困难。
- 语言只是工具，应对不同的需求场景选择适合的工具是一般的码农的最佳选择。(如果你是顶级大神,能轻易的造出强大的轮子除外)
- 多掌握几个工具是有必要的，至少没有对比就会变成井底之蛙。
