---
title: mysql字符集问题
date: 2020-09-01 19:01:33
tags: mysql
---

现代产品和国际化产品建议都使用utf8mb4字符集，表情已无处不在🤖🦖。人生苦短建议mb4.

<!--more-->

mysql 可以设置数据库级别，表级别，列级别 字符集编码；控制粒度依次细化，也就是如果都设置了，列级别优先级最高。

定义数据表结构时建议不要定义列的字符集，以免将来修改变得麻烦。

## 修改表的字符集

### 修改表的字符集 并刷新之前已存在的数据

```
ALTER table table_name CONVERT to CHARACTER set  新的字符集; 
```

### 修改表的字符集，但不对之前已存在的数据刷新

```
ALTER table table_name DEFAULT to CHARACTER set  新的字符集; 
```

## 批量修改

```sql
SELECT
	CONCAT(
		'ALTER TABLE ',
		TABLE_NAME,
		' CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;'
	)
FROM
	information_schema.`TABLES`
WHERE
	TABLE_SCHEMA = 'DATABASE_NAME';
```
得到修改语句，复制出执行语句，进行执行。如果数据库数据较多，将会比较耗时。

如果只是修改默认字符集不修改数据。

```sql
SELECT
	CONCAT(
		'ALTER TABLE ',
		TABLE_NAME,
		' DEFAULT  CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;'
	)
FROM
	information_schema.`TABLES`
WHERE
	TABLE_SCHEMA = 'DATABASE_NAME';
```
这样执行应该较为安全，也满足一般需求。

