---
title: mysql的waitimeout
date: 2021-06-02 20:33:18
tags: mysql
---


首先，我们来看下
```shell
show GLOBAL VARIABLES like '%timeout%';
```
默认值为28800s即8小时,我们改为100s

```ini
# Default Homebrew MySQL server config
[mysqld]
# Only allow connections from localhost
bind-address = 0.0.0.0
wait_timeout=100
interactive_timeout=100
```
重新查看结果

![](https://vison-blog.oss-cn-beijing.aliyuncs.com/20210603144255.png)

<!--more-->

查看对守护进程连接的影响

```php
 public function longT()
    {
        $TicketModel = new TicketModel();
        $this->success('开始建立连接...');
        while (true) {
            sleep(120);
            dump($TicketModel->select('t_id')->fetch());
        }
    }
```

发现在100s后的连接已被主动断开

![](https://vison-blog.oss-cn-beijing.aliyuncs.com/20210603144315.png)

代码中的场景是，**在wait_timeout之内无任何操作会自动关闭**




## 官方解释

interactive_timeout 28800

>The number of seconds the server waits for activity on an interactive connection before closing it. An interactive client is defined as a client that uses the **CLIENT_INTERACTIVE** option to mysql_real_connect(). See also wait_timeout.


waitimeout 28800

The number of seconds the server waits for activity on a noninteractive connection before closing it.



On thread startup, the session wait_timeout value is initialized from the global wait_timeout value or from the global interactive_timeout value, depending on the type of client (as defined by the CLIENT_INTERACTIVE connect option to mysql_real_connect()). See also interactive_timeout.



通过MySQL客户端连接db的是交互会话，通过jdbc等程序连接db的是非交互会话。 


总结：

如果应用程序长时间的使用一个连接，而有机会长时间不进行任何操作。则会导致连接被关闭。


参考文献:

1.[https://dev.mysql.com/doc/refman/5.7/en/server-system-variables.html](https://dev.mysql.com/doc/refman/5.7/en/server-system-variables.html)
2.[https://cloud.tencent.com/developer/article/1181515](https://cloud.tencent.com/developer/article/1181515)


