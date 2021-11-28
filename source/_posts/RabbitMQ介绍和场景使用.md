---
title: RabbitMQ介绍和场景使用
date: 2021-06-25 09:28:32
tags: 架构
---

## 安装

```yaml
version: '3.1'
services:
    rabbitmq-manger:
        image: rabbitmq:3-management
        restart: always
        ports:
          - 5672:5672
          - 8091:15672
```
使用docker进行快速安装

## 历史

- 2007年8月，Rabbit公司发行了 RabbitMQ 1.1.0.
- 2009年8月，VMware出资4.2亿美元收购了SpringSource[9]，并在一段时间内作为VMware的一个独立的部门；公司原有的商业产品以vFabric应用套件名义发售。之后SpringSource又接连收购了RabbitMQ[10]、Redis[11]和Gemstone[12]。除Redis外，它们的产品也成为了vFabric应用套件的一部分。

你会发现一个有趣而诧异的事实，VMware 和 Spring 、RabbitMQ、Redis这些大名鼎鼎的技术是同属一家公司。而 著名的 Spring背后的SpringSource公司主要以培训和咨询盈利。

<!--more-->

## 概念

![](https://vison-blog.oss-cn-beijing.aliyuncs.com/20210616101427.png)


> RabbitMQ is a message broker: it accepts and forwards messages. You can think about it as a post office: when you put the mail that you want posting in a post box, you can be sure that Mr. or Ms. Mailperson will eventually deliver the mail to your recipient. In this analogy, RabbitMQ is a post box, a post office and a postman.

这是官网最开头的一段介绍,这里将RabbitMQ类比为邮局派信场景，RabbitMQ扮演邮箱、邮局、邮差的角色。这里也看到了 `broker` 这个单词，Kafka也有broker这个概念，这里我们暂且将它理解为`代理`的意思。


## 生产者 producer

简单理解就是发送消息的程序

![](https://vison-blog.oss-cn-beijing.aliyuncs.com/20210618112249.png)


## 消费者 consumer

![](https://vison-blog.oss-cn-beijing.aliyuncs.com/20210618112407.png)

## 队列 queue

![](https://vison-blog.oss-cn-beijing.aliyuncs.com/20210618112446.png)

消息存储于queue当中，多个producer 可往一个 queue发送消息

## 交换机 Exchange

![](https://vison-blog.oss-cn-beijing.aliyuncs.com/20210618112856.png)

交换机是用来发送消息的AMQP实体。交换机拿到一个消息之后将它路由给一个或零个队列。它使用哪种路由算法是由交换机类型和被称作绑定（bindings）的规则所决定的(这个后面会讲到)。

**Exchange Type**

- direct  直连 
- fanout  扇出
- topic   主题
- headers  头

除交换机类型外，在声明交换机时还可以附带许多其他的属性，其中最重要的几个分别是：
- Name
- Durability （消息代理重启后，交换机是否还存在）
- Auto-delete （当所有与之绑定的消息队列都完成了对此交换机的使用后，删掉它）
- Arguments（依赖代理本身）

```php
 public function exchange_declare(
        $exchange,
        $type,
        $passive = false,
        $durable = false,
        $auto_delete = true,
        $internal = false,
        $nowait = false,
        $arguments = array(),
        $ticket = null
    )
```
持久（durable）、暂存（transient）。持久化的交换机会在消息代理（broker）重启后依旧存在，而暂存的交换机则不会（它们需要在代理再次上线后重新被声明）。然而并不是所有的应用场景都需要持久化的交换机。

**默认交换机**

那就是每个新建队列（queue）都会自动绑定到默认交换机上，绑定的路由键（routing key）名称与队列名称相同。


**直连交换机 Direct**

![](https://vison-blog.oss-cn-beijing.aliyuncs.com/20210618113517.png)

```php
 $channel->queue_bind('hello_queue', 'hello_exchange', 'hello_key');
```

它是如何工作的：
- 将一个队列绑定到某个交换机上，同时赋予该绑定一个路由键（routing key）
- 当一个携带着路由键为hello_key的消息被发送给直连交换机hello_exchange时，交换机会把它路由给hello_queue的队列。

```php
 $channel->basic_publish($msg, 'hello_exchange', 'hello_key');
```

![](https://vison-blog.oss-cn-beijing.aliyuncs.com/20210618113859.png)

**扇形交换机  fanout**

扇型交换机（funout exchange）将消息路由给绑定到它身上的所有队列，而不理会绑定的路由键。

如果N个队列绑定到某个扇型交换机上，当有消息发送给此扇型交换机时，交换机会将消息的拷贝分别发送给这所有的N个队列。

![](https://vison-blog.oss-cn-beijing.aliyuncs.com/20210618114009.png)

```php
// RabbitFanoutProduce.php
$faker = Factory::create('zh_CN');
$connection = new AMQPStreamConnection('192.168.106.179', 5672, 'guest', 'guest');
// 创建通道
$channel = $connection->channel();

$channel->exchange_declare('test.fanout', AMQPExchangeType::FANOUT, false, false, false);

$body = $faker->text(20);
$msg = new AMQPMessage($body, ['delivery_mode' => AMQPMessage::DELIVERY_MODE_PERSISTENT]);
$channel->basic_publish($msg, 'test.fanout');
```
`RabbitFanoutProduce` 生产者定义了一个`test.fanout` 交换机类型是`AMQPExchangeType::FANOUT`

```php
// lmsConsoumer.php
$connection = new AMQPStreamConnection('192.168.106.179', 5672, 'guest', 'guest');
// 创建通道
$channel = $connection->channel();

$channel->queue_declare('test.lms', false, false, false);
$channel->queue_bind('test.lms', 'test.fanout');
$callback = function ($msg) {
    echo ' [x] ', $msg->body, "\n";
};
$channel->basic_consume('test.lms', '', false, true, false, false, $callback);

while ($channel->is_open()) {
    $channel->wait();
}
```

`lmsConsoumer` 订阅了一个`test.lms`的队列并绑定到`test.fanout`交换机

```php
// omsConsoumer.php
$connection = new AMQPStreamConnection('192.168.106.179', 5672, 'guest', 'guest');
// 创建通道
$channel = $connection->channel();

$channel->queue_declare('test.oms', false, false, false,false);
$channel->queue_bind('test.oms', 'test.fanout');
$callback = function ($msg) {
    echo ' [x] ', $msg->body, "\n";
};
$channel->basic_consume('test.oms', '', false, true, false, false, $callback);

while ($channel->is_open()) {
    $channel->wait();
}
```

`omsConsoumer` 订阅了一个`test.oms`的队列并绑定到`test.fanout`交换机

示例中演示了，一个生产者生产消息给2个系统订阅消费。

Fanout 典型的一个应用场景是多个应用系统订阅一个消息事件。

eg： 客服系统、运营系统、财务系统同时订阅订单系统的订单状态变更事件。

![](https://vison-blog.oss-cn-beijing.aliyuncs.com/20210618114806.png)

这样不同系统都能各自使用各自的队列处理订单的变更业务逻辑。

细化下场景举个例子：

当订单完结 order close:
- 客服系统需要给客户发送一个客户满意度调查
- 运营系统需要发送一张按订单消费金额配比的优惠券
- 财务系统需要计算这笔订单的入账


**主题交换机 topic**

主题交换机（topic exchanges）通过对消息的路由键和队列到交换机的绑定模式之间的匹配，将消息路由给一个或多个队列。

![](https://vison-blog.oss-cn-beijing.aliyuncs.com/20210618114944.png)

topic有点类似 direct和fanout的结合体，即可以广播又可以按一定规则指定 route.

上面示例图案例：

- 这是一个关于动物的消息消费程序
- 有关orange的动物将进入Q1 ，例如 fast.orange.pig 快速的橙色猪
- 有关 rabbit 和 lazy 的动物将进入 Q2 ，例如 lazy.green.rabbit 或 lazy.yellow.monkey
- 如果匹配多个模式则进入多个相应的队列，例如 lazy.orange.monkey 则会进入Q1和Q2

```php
$faker = Factory::create('zh_CN');
$connection = new AMQPStreamConnection('192.168.106.179', 5672, 'guest', 'guest');
// 创建通道
$channel = $connection->channel();
$channel->exchange_declare('test.topic', AMQPExchangeType::TOPIC, false, false, false);

$channel->queue_declare('Q1');
$channel->queue_declare('Q2');
$channel->queue_bind('Q1', 'test.topic', '*.orange.*');
$channel->queue_bind('Q2', 'test.topic', '*.*.rabbit');
$channel->queue_bind('Q2', 'test.topic', 'lazy.#');


$body = $faker->name();
$msg = new AMQPMessage($body, ['delivery_mode' => AMQPMessage::DELIVERY_MODE_PERSISTENT]);
$channel->basic_publish($msg, 'test.topic', 'fast.orange.pig');
$channel->basic_publish($msg, 'test.topic', 'lazy.green.rabbit');
$channel->basic_publish($msg, 'test.topic', 'lazy.orange.monkey');
```

![](https://vison-blog.oss-cn-beijing.aliyuncs.com/20210618115131.png)


可以看到3个消息，发送到了2个队列。Q1和Q2各有2个，因为lazy.orange.monkey进入了2个队列。


**头交换机 header**

有时消息的路由操作会涉及到多个属性，此时使用消息头就比用路由键更容易表达，头交换机（headers exchange）就是为此而生的。头交换机使用多个消息属性来代替路由键建立路由规则。通过判断消息头的值能否与指定的绑定相匹配来确立路由规则。

它提供更多的匹配，可设置x-match 为any 或all 来控制是任意匹配还是全部匹配。


### 队列 queue

AMQP中的队列（queue）跟其他消息队列或任务队列中的队列是很相似的：它们存储着即将被应用消费掉的消息。队列跟交换机共享某些属性，但是队列也有一些另外的属性。

- Name
- Durable（消息代理重启后，队列依旧存在）
- Exclusive（只被一个连接（connection）使用，而且当连接关闭后队列即被删除）
- Auto-delete（当最后一个消费者退订后即被删除）
- Arguments（一些消息代理用他来完成类似与TTL的某些额外功能）

### 消息确认

消费者应用（Consumer applications） - 用来接受和处理消息的应用 - 在处理消息的时候偶尔会失败或者有时会直接崩溃掉。而且网络原因也有可能引起各种问题。这就给我们出了个难题，AMQP代理在什么时候删除消息才是正确的？AMQP 0-9-1 规范给我们两种建议：
- 当消息代理（broker）将消息发送给应用后立即删除。（使用AMQP方法：basic.deliver或basic.get-ok）
- 待应用（application）发送一个确认回执（acknowledgement）后再删除消息。（使用AMQP方法：basic.ack）

前者被称作自动确认模式（automatic acknowledgement model），后者被称作显式确认模式（explicit acknowledgement model)。

```php
$callback = function ($msg) {
  echo ' [x] Received ', $msg->body, "\n";
  sleep(substr_count($msg->body, '.'));
  echo " [x] Done\n";
  $msg->ack();
};

$channel->basic_consume('task_queue', '', false, false, false, false, $callback);
```

以上代码示例展示ack使用，basic_consume的第4个参数要 设置为true。

### 拒绝消息

当一个消费者接收到某条消息后，处理过程有可能成功，有可能失败。应用可以向消息代理表明，本条消息由于“拒绝消息（Rejecting Messages）”的原因处理失败了（或者未能在此时完成）。当拒绝某条消息时，应用可以告诉消息代理如何处理这条消息——销毁它或者重新放入队列。当此队列只有一个消费者时，请确认不要由于拒绝消息并且选择了重新放入队列的行为而引起消息在同一个消费者身上无限循环的情况发生。


### 连接

AMQP连接通常是长连接。AMQP是一个使用TCP提供可靠投递的应用层协议。AMQP使用认证机制并且提供TLS（SSL）保护。当一个应用不再需要连接到AMQP代理的时候，需要优雅的释放掉AMQP连接，而不是直接将TCP连接关闭。


### 虚拟主机 vhost

为了在一个单独的代理上实现多个隔离的环境（用户、用户组、交换机、队列 等），AMQP提供了一个虚拟主机（virtual hosts - vhosts）的概念。这跟Web servers虚拟主机概念非常相似，这为AMQP实体提供了完全隔离的环境。

```php
$connection = new AMQPStreamConnection('192.168.106.179', 5672, 'guest', 'guest','test-vhost');

```

## 动态匹配模型

生产者

```php
 protected function execute(InputInterface $input, OutputInterface $output): int
    {
        $connection = new AMQPStreamConnection('192.168.106.179', 5672, 'guest', 'guest');
        // 创建通道
        $channel = $connection->channel();
        $channel->exchange_declare('order.lifecycle', AMQPExchangeType::TOPIC, false, false, false);
        //定义一个默认 全状态队列
        $channel->queue_declare('order.all');
        //匹配 全状态 订单消息
        $channel->queue_bind('order.all', 'order.lifecycle', 'order.*');
        $faker = Factory::create('zh_CN');
        $orderStatus = [
            self::ORDER_CREATE, self::ORDER_SENDED, self::ORDER_WAIT_PAY
        ];
        $status = $orderStatus[array_rand($orderStatus)];
        $body = [
            'status' => $status,
            'name' => $faker->name,
            'order_no' => $faker->uuid
        ];
        dump($body);
        $msg = new AMQPMessage(json_encode($body), ['delivery_mode' => AMQPMessage::DELIVERY_MODE_PERSISTENT]);
        //消息 动态 绑定 路由键
        $channel->basic_publish($msg, 'order.lifecycle','order.'.$status);
        return Command::SUCCESS;
    }
```
```php
消费者
 public function handPay()
    {
        $connection = new AMQPStreamConnection('192.168.106.179', 5672, 'guest', 'guest');
        // 创建通道
        $channel = $connection->channel();
        //定义 h66 消费 pay 队列
        $channel->queue_declare('h66.pay');
        //将 WAIY_PAY 类型消息 绑定到该队列
        $channel->queue_bind('h66.pay', 'order.lifecycle', 'order.WAIT_PAY');
        $callback = function($msg) {
            $body = json_decode($msg->body, true);
            $this->info("处理数据...{$body['status']} {$body['order_no']}");
        };
        // 消费 队列
        $channel->basic_consume('h66.pay', '', false, true, false, false, $callback);
        // 阻塞队列监听事件
        while ($channel->is_open()) {
            $channel->wait();
        }
    }
```
 
代码示例中 生成者根据订单状态动态生产相应路由键消息到交换机，消费者订阅自己所需的状态到自己的队列当中进行消费。

例如 `handPay` 消费者只订阅待支付类型。
 

## 参考

1. https://rabbitmq.mr-ping.com/
2. https://www.rabbitmq.com/getstarted.html
