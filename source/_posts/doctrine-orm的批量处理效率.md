---
title: doctrine orm的批量处理效率
date: 2021-12-21 14:44:16
tags: php
---

doctrine无疑是一款优秀的ORM工具，本文会根据doctrine官网的批处理这章节来讲讲doctrine的批量处理。

官网链接 [doctrine批量处理](https://www.doctrine-project.org/projects/doctrine-orm/en/current/reference/batch-processing.html#batch-processing)

此章开头，doctrine讲到会介绍doctrine的有效率的批处理方式。
<!--more-->

> This chapter shows you how to accomplish bulk inserts, updates and deletes with Doctrine in an efficient way.

**本文将以批量插入为例讲doctrine是如何执行批量操作和它的原理是什么。**

在文章的开头，有一段有意思的话，我觉得耐人寻味。
![](https://vison-blog.oss-cn-beijing.aliyuncs.com/20211210154538.png)

简单翻译就是，**ORM工具并不适合去处理批量操作**，每个关系型数据库都有它最高效的方式来应对。如果以下的方式你认为并不是最高效的，那么建议您根据特定的关系型数据库特有的方式来处理。

下面来看看doctrine是如何处理的。

```php
<?php
$batchSize = 20;
for ($i = 1; $i <= 10000; ++$i) {
    $user = new CmsUser;
    $user->setStatus('user');
    $user->setUsername('user' . $i);
    $user->setName('Mr.Smith-' . $i);
    $em->persist($user);
    if (($i % $batchSize) === 0) {
        $em->flush();
        $em->clear(); // Detaches all objects from Doctrine!
    }
}
$em->flush(); // Persist objects that did not make up an entire batch
$em->clear();
```

通过日志，我们发现`doctrine`所谓的`有效率`的方式是按`$batchSize`数量切分，进行事务提交。比直接的逐条` $em->flush();`操作省去了大量的`commit`网络通信。

通过`wireshark`抓包我们也验证了这一推断。

![](https://vison-blog.oss-cn-beijing.aliyuncs.com/20211210160127.png)

假设数据总数是 n, batchSize 是m:

- 逐条flush,需要执行n次insert和commit,即2n次通信。
- doctrine bulk操作是n+n/m次，通信次数会少很多。

并不意味着将batchSize设置最大就是最有效的方式，batchSize越大也意味着flush的工作将会更耗时。

但与mysql 本身的批量处理还是会多非常多次的通信。

```sql
INSERT INTO tbl_name (a,b,c) VALUES(1,2,3),(4,5,6),(7,8,9);
```
使用mysql本身的方法可能只要执行2次通信。

因此，其实doctrine官网那段话说的非常忠恳了，要想获得最佳性能可能需要根据特定RDBMS来相应的处理。
