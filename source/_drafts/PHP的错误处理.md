---
title: PHP的错误处理
date: 2020-08-11 14:44:53
tags: php
---

`set_error_handler` 覆盖前一个注册

```php
set_error_handler(function(){
    echo "error hander function 2\n";
});
```