---
title: 利用信号控制php常驻进程平滑中断思考
date: 2020-05-30 10:30:49
tags: php linux
---

很多场景下我们都需要进程程序在后台一直处理任务，比如队列消费。可采用while true的方式让进程常驻按一定的频次执行任务。但是但我们要重启进程或中止进程时，如何保证进程内正在执行的任务执行完毕再中止呢？

<!--more-->

思考一下，可不可以我们通过一种指令告诉进程，"诶，我现在要重启一下，你能把正在做的事情做完了先退出歇会么？"


`kill`命令可以解决这个问题。

## 再看kill

许人肯定会觉得 kill 不就是杀掉进程么？ 我经常用`kill -9`杀进程。 这么说也没错，不过我们现在可以系统地来看看`kill`命令.

我们先看下官方的定义,让那个男人来跟我们讲讲。

```shell
man shell
```

```
KILL(1)                                                                         User Commands                                                                         KILL(1)

NAME
       kill - terminate a process

SYNOPSIS
       kill [-s signal|-p] [-q sigval] [-a] [--] pid...
       kill -l [signal]

DESCRIPTION
       The command kill sends the specified signal to the specified process or process group.  If no signal is specified, the TERM signal is sent.  The TERM signal will kill
       processes which do not catch this signal.  For other processes, it may be necessary to use the KILL (9) signal, since this signal cannot be caught.

       Most modern shells have a builtin kill function, with a usage rather similar to that of the command described here.  The '-a' and '-p' options, and the possibility to
       specify processes by command name are a local extension.

       If sig is 0, then no signal is sent, but error checking is still performed.
```

- 官方解释`kill`是用来终止进程的。
- `kill` 发送指定的信号给到进程或进程组。
- 如果没有指定信号，默认发送`TERM`信号。
- `TERM`信号将会杀掉进程，当`TERM`未被捕获的时候。
- `9`信号不能被捕获

**谈谈我的理解**

1. kill命令就是用来杀掉进程的
2. 它可以给进程发送一些指令，让程序去捕获做特殊处理。比如上面说到的场景，让程序执行完正在执行的任务，再退出。

## 验证

接下来我们用PHP脚本来验证下上面的理解。我们用`pcntl_signal`来对信号进行捕获。

```php
class SignalShell extends Shell
{

    private $taskFinish = false;

    public function __construct()
    {
//        pcntl_signal(SIGTERM, [$this, 'sig_handler']);
//        pcntl_signal(SIGHUP, [$this, 'sig_handler']);
        pcntl_signal(SIGINT, [$this, 'sig_handler']);
//        pcntl_signal(SIGQUIT, [$this, 'sig_handler']);
        pcntl_signal(SIGILL, [$this, 'sig_handler']);
        pcntl_signal(SIGPIPE, [$this, 'sig_handler']);
        pcntl_signal(SIGALRM, [$this, 'sig_handler']);
        pcntl_signal(SIGUSR1, [$this, 'sig_handler']);
        $this->info("注册信号");
    }

    public function task()
    {
        while (true && !$this->taskFinish) {
            sleep(10);
            $this->info(uniqid());
        }
    }

    public function sig_handler($signo)
    {
        $time = date('Y-m-d H:i:s');
        if ($signo == 14) {
            //忽略alarm信号
            echo $time . " ignore alarm signo[{$signo}]\r\n";
        } else {
            echo $time . " exit  signo[{$signo}]\r\n";
            if ($signo == SIGUSR1) {
                $this->info("捕获自定义");
                $this->taskFinish = true;
            }
        }
    }
}
```

代码很简单，就是让脚本每隔10秒输出一个字符串，任务之前对一些信号进行捕获。

![](http://img.rc5j.cn/blog20200530114817.png)

分别对进程执行了，kill、kill QUIT、kill HUP 发现进程都会被直接终止。

下面我们开始,对`TERM`进行捕获。

```php
pcntl_signal(SIGTERM, [$this, 'sig_handler']);
```
打开注释。

![](http://img.rc5j.cn/blog20200530115128.png)

15信号(TERM)被捕获到了，但是进程并没有退出,还再继续执行。

我们再试下USR1信号。

![](http://img.rc5j.cn/blog20200530115632.png)

USR1被捕获到了，并且程序立即执行完一次输出退出了。注意我是程序自己控制了,捕获到USR1之后不继续执行循环。

细心的朋友们可能会发现，程序中的sleep被跳过了。

**这是什么原因呢?**

## sleep

事实上sleep是一个特殊的函数。其实官方文档有解释:

![](http://img.rc5j.cn/blog20200530120859.png)

`sleep`在被信号中止时，会返回非0值,非windows下会返回剩余秒数。

让我们来验证下。

```php
 while (true && !$this->taskFinish) {
            $res = sleep(10);
            $this->info("sleep返回:".$res);
            $this->info(uniqid());
 }
```
我们记录了sleep执行完的返回值。

![](http://img.rc5j.cn/blog20200530121207.png)

发现信号给到时，sleep确实会返回剩余秒数。这就解释了为什么上面看到的sleep被跳过了。

## 总结

> A process can define how to handle incoming POSIX signals. If a process does not define a behaviour for a signal, then the default handler for that signal is being used. The table below lists some default actions for POSIX-compliant UNIX systems, such as FreeBSD, OpenBSD and Linux.

1. kill能给进程发送信号量，告诉进程按什么方式结束。
2. kill定义的不同信号量，用法不同，但是需要程序自己去处理。它只是定义了目的，但未定义过程和实际结果。



## 参考

![](https://en.wikipedia.org/wiki/Signal_(IPC))


