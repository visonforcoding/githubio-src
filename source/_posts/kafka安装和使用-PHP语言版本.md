---
title: kafka搭建和使用(PHP语言版本)
date: 2020-07-08 16:13:45
tags: kafka
---

首先,安装确实是一个费时费力的事情。这里我们使用docker安装。

<!--more-->

## docker搭建kafka

```yml
## docker-compose.yml
version: '3.1'
services:
    zookeeper:
        image: wurstmeister/zookeeper
        ports:
          - "2181:2181"
    kafka:
        image: wurstmeister/kafka
        ports:
          - "9092:9092"
        environment:
           KAFKA_ADVERTISED_HOST_NAME: 172.17.0.1
           KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
           KAFKA_ADVERTISED_PORT: 9092
```
更多细节建议访问官方文档查阅。

## PHP实现

### 生产者

```PHP
 public function kafka(Request $request)
    {
        $faker = Factory::create('zh_CN');
        $message = $faker->name();
        Log::debug('消息', ['message' => $message]);

        $conf = new Conf();
        $conf->set('log_level', (string) LOG_DEBUG);
        $conf->set('debug', 'all');
        $conf->set('metadata.broker.list', '127.0.0.1:9092');
        $conf->setDrMsgCb(function ($kafka, $message) {
            Log::debug("kafka信息", ['message' => var_export($message, true)]);
        });
        $conf->setErrorCb(function ($kafka, $err, $reason) {
            Log::debug("kafka错误", ['err' => $err, 'reason' => $reason]);
        });

        $conf->setLogCb(function ($kafka, $level, $facility, $message) {
            Log::debug(vsprintf("Kafka %s: %s (level: %d)\n", [$facility, $message, $level]));
        });

        //If you need to produce exactly once and want to keep the original produce order, uncomment the line below
        //$conf->set('enable.idempotence', 'true');

        $producer = new Producer($conf);

        $topic = $producer->newTopic("test");
        $topic->produce(RD_KAFKA_PARTITION_UA, 0, $faker->name());
        $producer->poll(0);

        $result = $producer->flush(10000);
        if (RD_KAFKA_RESP_ERR_NO_ERROR !== $result) {
            throw new \RuntimeException('Was unable to flush, messages might be lost!');
        }

        return new ActionResponse($result);
    }
```

### 消费者

```PHP
public function consume()
    {
        $conf = new Conf();

// Configure the group.id. All consumer with the same group.id will consume
// different partitions.
        $conf->set('group.id', 'myConsumerGroup');

// Initial list of Kafka brokers
        $conf->set('metadata.broker.list', '127.0.0.1');

// Set where to start consuming messages when there is no initial offset in
// offset store or the desired offset is out of range.
// 'smallest': start from the beginning
        $conf->set('auto.offset.reset', 'smallest');

        $consumer = new KafkaConsumer($conf);

// Subscribe to topic 'test'
        $consumer->subscribe(['test']);

        echo "Waiting for partition assignment... (make take some time when\n";
        echo "quickly re-joining the group after leaving it.)\n";

        while (true) {
            $message = $consumer->consume(120 * 1000);
            switch ($message->err) {
                case RD_KAFKA_RESP_ERR_NO_ERROR:
                    $this->info($message->payload);
                    break;
                case RD_KAFKA_RESP_ERR__PARTITION_EOF:
                    echo "No more messages; will wait for more\n";
                    break;
                case RD_KAFKA_RESP_ERR__TIMED_OUT:
                    $this->info("Timed out");
                    break;
                default:
                    throw new Exception($message->errstr(), $message->err);
                    break;
            }
        }
    }
```

## 测试

生产者是一个restful的api，直接调用会往kafka里写入1个中文姓名的消息。

消费者是一个PHP脚本进程，启动会开始消费kafka消息

```shell
php bin/cli.php kafka consume
```

![](http://img.rc5j.cn/blog20200709115956.png)

## 问题

虽然已经搭建了kafka`消息中间件`,和编写了`生产者`和`消费者`.但是关于其中的许多细节还要搞清除。包括:

- 什么是broken
- 什么是partition
- 消息flush是做什么
- poll又是做什么
- 等等更多细节