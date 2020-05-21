---
title: [原创]mysql单个表的权限控制
date: 2020-05-08 09:43:39
tags: mysql

---

> 在系统开发当中有这样的需求，A系统需要读写B系统的数据库数据,但是某些特殊的表数据只允许读操作。这时候就需要做到表级的权限控制。

<!-- more -->

## revoke

Mysql本身是支持用revoke进行权限回收操作的。

[https://dev.mysql.com/doc/refman/5.6/en/revoke.html](https://dev.mysql.com/doc/refman/5.6/en/revoke.html)

```
REVOKE
    priv_type [(column_list)]
      [, priv_type [(column_list)]] ...
    ON [object_type] priv_level
    FROM user [, user] ...

REVOKE ALL [PRIVILEGES], GRANT OPTION
    FROM user [, user] ...

REVOKE PROXY ON user
    FROM user [, user] ...
```
从语法当中可以看到还可以做到列级别的控制。


## 问题

```
mysql> revoke insert,delete,update on db_oms.t_order from 'oms_order_ro'@'localhost';
ERROR 1147 (42000): There is no such grant defined for user 'oms_order_ro' on host 'localhost' on table 't_order'
```

但是事实上，执行的时候会遇到问题。

**什么原因呢？**

```
mysql> show grants for oms_order_ro@localhost
    -> ;
+----------------------------------------------------------------------------------+
| Grants for oms_order_ro@localhost                                                |
+----------------------------------------------------------------------------------+
| GRANT USAGE ON *.* TO 'oms_order_ro'@'localhost'                                 |
| GRANT SELECT, INSERT, UPDATE, DELETE ON `db_oms`.* TO 'oms_order_ro'@'localhost' |
+----------------------------------------------------------------------------------+
```
仔细看下，我们是使用的通配符去进行赋权限。看起来这里mysql还是表现的比较本。认为没有该权限进行回收。

那么正确的做法应该是怎样的呢？


> Managing access in mysql can be quite dificult !!

Once you gave him database.* you cannot revoke access for an object that is in that class. MySQL doesn't expand the Hotels.* wildcard to the individual tables The permissions tables store the granted permissions. Therefore, since you didn't actually grant anything on Hotels.AllHotels , there's nothing for MySQL to revoke. In this case you need to do it granular form the start !

Remove all privileges on database, table, column levels, etccc.

Grant privileges to EACH table, except 'you choose'.
Grant privilege to specified fields in table 'you choose'.

**我们必须要逐个逐个表进行赋权限，然后进行回收。**

实际上这么操作虽然能解决问题，但是会带来跟多问题，如果表增加了。你必须再对这个表进行赋权限和回收权限。


