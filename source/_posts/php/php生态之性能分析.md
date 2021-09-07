---
title: php生态之性能分析
date: 2020-07-23 15:00:58
tags: php
---

![](http://img.rc5j.cn/blog20200724153643.png)

一般情况下我们并不会太关注PHP的执行效率，因为一般而言他都表现正常满足需求。但当真正遇到问题的时候，我们需要有分析性能在哪丢失的能力。

<!--more-->

`xhprof`正是这样的工具。但是由于年久失修，目前已经不支持PHP7 .

![](http://img.rc5j.cn/blog20200724154122.png)

不过，好在还有非官方商业组织开源了PHP7版本,`tideways-xhprof`。

![](http://img.rc5j.cn/blog20200724154306.gif)

官网  https://tideways.com/profiler/xhprof-for-php7

## 安装

```shell
git clone "https://github.com/tideways/php-xhprof-extension.git"
cd php-xhprof-extension
phpize
./configure
make
sudo make install
```

配置好ini，重启查看下php -m

## 图形化

`tideways-xhprof` 可以将分析出方法调用、方法调用过程和性能消耗数据。

`tideways-xhprof` 本身还提供商业化服务，有着比较好的体验。不过也同时有开源的图形化工具。比较好的是`xhgui`和他配套的是`perftools/php-profiler`.看了下作者，还是`markstory`，cakephp的作者，几年前使用cakephp的时候，还有过交流。


## xgui安装

可以选择源码部署，也可以选择docker部署。方便点选择使用docker。

1. Clone or download xhgui from GitHub.

2. Startup the containers: docker-compose up -d

3. Open your browser at http://xhgui.127.0.0.1.xip.io:8142 or just http://localhost:8142

## php-profiler使用

官方github上写几种接入方式，我推荐用注册shutdown方式，正在对项目代码无入侵。保存过程在shutdown之后。

```PHP
 $profiler = new \Xhgui\Profiler\Profiler($config);

    // The profiler itself checks whether it should be enabled
    // for request (executes lambda function from config)
$profiler->enable();

    // shutdown handler collects and stores the data.
$profiler->registerShutdownHandler();
```
上面的`$config`，在使用非文件存储的时候要注意不要安装官方配置来，官方配置目前存在一点问题，新配置会不生效。我看了源码，并且提交了PR。

```PHP
//    'db.host' => 'mongodb://127.0.0.1:27018',
//    'db.db' => 'xhprof',
    'save.handler.mongodb' => array(
        'dsn' => 'mongodb://127.0.0.1:27018',
        'database' => 'xhprof',
        // Allows you to pass additional options like replicaSet to MongoClient.
        // 'username', 'password' and 'db' (where the user is added)
        'options' => array(),
    ),
```
注释部分才有效.



## 默认配置

```PHP
<?php
/**
 * Default configuration for Xhgui
 */

$mongoUri = getenv('XHGUI_MONGO_URI') ?: '127.0.0.1:27017';
$mongoUri = str_replace('mongodb://', '', $mongoUri);
$mongoDb = getenv('XHGUI_MONGO_DB') ?: 'xhprof';

return array(
    'debug' => false,
    'mode' => 'development',

    // Can be mongodb, file or upload.

    // For file
    //
    //'save.handler' => 'file',
    //'save.handler.filename' => dirname(__DIR__) . '/cache/' . 'xhgui.data.' . microtime(true) . '_' . substr(md5($url), 0, 6),

    // For upload
    //
    // Saving profile data by upload is only recommended with HTTPS
    // endpoints that have IP whitelists applied.
    //
    // The timeout option is in seconds and defaults to 3 if unspecified.
    //
    //'save.handler' => 'upload',
    //'save.handler.upload.uri' => 'https://example.com/run/import',
    //'save.handler.upload.timeout' => 3,

    // For MongoDB
    'save.handler' => 'mongodb',
    'db.host' => sprintf('mongodb://%s', $mongoUri),
    'db.db' => $mongoDb,

    'pdo' => array(
        'dsn' => 'sqlite:/tmp/xhgui.sqlite3',
        'user' => null,
        'pass' => null,
        'table' => 'results'
    ),

    // Allows you to pass additional options like replicaSet to MongoClient.
    // 'username', 'password' and 'db' (where the user is added)
    'db.options' => array(),
    'templates.path' => dirname(__DIR__) . '/src/templates',
    'date.format' => 'M jS H:i:s',
    'detail.count' => 6,
    'page.limit' => 25,

    // call fastcgi_finish_request() in shutdown handler
    'fastcgi_finish_request' => true,

    // Profile x in 100 requests. (E.g. set XHGUI_PROFLING_RATIO=50 to profile 50% of requests)
    // You can return true to profile every request.
    'profiler.enable' => function() {
        $ratio = getenv('XHGUI_PROFILING_RATIO') ?: 100;
        return (getenv('XHGUI_PROFILING') !== false) && (mt_rand(1, 100) <= $ratio);
    },

    'profiler.simple_url' => function($url) {
        return preg_replace('/\=\d+/', '', $url);
    },
    
    //'profiler.replace_url' => function($url) {
    //    return str_replace('token', '', $url);
    //},

    'profiler.options' => array(),

    'profiler.skip_built_in' => false,
);

```
以上是默认配置

## 效果

![](http://img.rc5j.cn/blog20200724134032.png)

图中可以看到,每次请求的花费时间。


![](http://img.rc5j.cn/blog20200724165205.png)

![](http://img.rc5j.cn/blog20200724165354.png)

通过观察方法调用次数，可以发现symfony ErrorHandler这个组件方法执行的特别多。

于是我取消了这个组件，发现接口请求时间从`113ms`直接就降到了`71ms`.

**这就是很直观的性能定位了**