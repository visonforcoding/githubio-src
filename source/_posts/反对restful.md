---
title: 反对restful
date: 2022-06-30 09:54:41
tags:
---

> 是人都会犯错，人创造的东西就会有错。勇于质疑、敢于质疑。

## 反对restful

REST这个词，是[Roy Thomas Fielding](https://en.wikipedia.org/wiki/Roy_Fielding "Roy Thomas Fielding")在他2000年的[博士论文](https://www.ics.uci.edu/\~fielding/pubs/dissertation/top.htm "博士论文")中提出的。

<!--more-->

restful的几大概念：

- 每一个URI代表一种资源，所以URL必须是名词。

- 客户端通过HTTP动词`get`、`post`、`put`、`delete`，对服务器端资源进行操作，4个http 请求方式，差不多正好对应后端服务对数据的查、增、改、删。

- 状态码响应，100多种状态码，覆盖了绝大部分可能遇到的情况。发生错误时，不要返回 200 状态码

- response 的 body直接就是数据，不要做多余的包装。

http 动词

```sql
GET：   读取（Read）
POST：  新建（Create）
PUT：   更新（Update）
PATCH： 更新（Update），通常是部分更新
DELETE：删除（Delete）
```

而下面的 URL 不是名词，所以被认为都是错误的。

```sql
## 错误
/getAllCars
/createNewCar
/deleteAllRedCars

## 正确
GET    /zoos：列出所有动物园
POST   /zoos：新建一个动物园
GET    /zoos/ID：获取某个指定动物园的信息
PUT    /zoos/ID：更新某个指定动物园的信息（提供该动物园的全部信息）
PATCH  /zoos/ID：更新某个指定动物园的信息（提供该动物园的部分信息）
DELETE /zoos/ID：删除某个动物园
GET    /zoos/ID/animals：列出某个指定动物园的所有动物
DELETE /zoos/ID/animals/ID：删除某个指定动物园的指定动物

```

状态码举例

```sql
400 Bad Request：服务器不理解客户端的请求，未做任何处理。
401 Unauthorized：用户未提供身份验证凭据，或者没有通过身份验证。
403 Forbidden：用户通过了身份验证，但是不具有访问资源所需的权限。
404 Not Found：所请求的资源不存在，或不可用。
405 Method Not Allowed：用户已经通过身份验证，但是所用的 HTTP 方法不在他的权限之内。
410 Gone：所请求的资源已从这个地址转移，不再可用。
415 Unsupported Media Type：客户端要求的返回格式不支持。比如，API 只能返回 JSON 格式，但是客户端要求返回 XML 格式。
422 Unprocessable Entity ：客户端上传的附件无法处理，导致请求失败。
429 Too Many Requests：客户端的请求次数超过限额。
```

返回内容包含了多余的数据被认为是错误的

```sql
{"success":true, "data":{"id":1, "name":"周伯通"} } ## 错误
{"id":1, "name":"周伯通"}   ## 正确

```

## 问题

- 定义不同请求类型`get`、`post`、`put`、`delete` 不停切换,前后端都需要花时间去考虑定义和类型的切换。

存在模棱两可的情况下，不知道如何定义。例如 即有对资源的新增和更新。打个比方：

一个接口即增加了商品又更新了商品品类 *。*

这个时候你的URL资源如何定义？ `goods` ? `goodsAndgoodsCategory`?

是使用`post` 还是使用`put`？

- 在一些基于URL的请求监控统计或限流应用中，restful的模式反而会造成额外的问题

```sql
GET    /zoos：列出所有动物园
POST   /zoos：新建一个动物园
```

被认为是2个接口，在监控应用中可能会被统计到1个url去。

并且 带资源id的URL eg:`/foo/1`会被监控认为是多个不同的url

- 发生错误时，不要返回 200 状态码.就算是资源不存在会被认为`404`

打个比方，某个商品不存在或已下架，这个时候按restful的规范，你需要将http状态码设置为 404.

而我们通常认为页面不存在或URL本身不存在才是404.

另一个问题是，就算http状态码有100多个，但是也可能不满足多变的业务需求。

## 讨伐声

在国外也有许多人也反对restful，搜一下就可以看到。

1. &#x20;[Why REST Sucks - Troy A. Griffitts - Virtual Manuscript Room Collaborative Research Environment (VMR CRE)](https://vmrcre.org/web/scribe/home/-/blogs/why-rest-sucks "Why REST Sucks - Troy A. Griffitts - Virtual Manuscript Room Collaborative Research Environment (VMR CRE)")

2. [the restful is big lie](https://mmikowski.github.io/the_lie/ "the restful is big lie")

![](https://vison-blog.oss-cn-beijing.aliyuncs.com/image_k1Duew8lNl.png)

## 意义在哪

- restful 作者 HTTP协议（1.0版和1.1版）的主要设计者，可以看到restful与http网络协议细节密切相关。我们实际的业务编码都是在解决业务问题，我们其实希望越少关心底层技术细节越好。理想条件下，人人都不用关心底层技术实现，那这种技术可以作为普通工具为广大人群所使用。

- 它提供了一套规范，而且仅仅是规范。却似乎对于应用实践没有其他方面提升，它不能提供便利和性能提升。

- 某些规范是为了在混乱中建立秩序，而有些规范看起来是在建立强权。就拿ROI来看：

&#x20;  我们认为PHP PSR 这种编码规范与之对比，客观计算：假设投入成本为C 、收益回报为E、风险为R

&#x20;    PSR ： C是1、E是2、R是0    ，低投入有回报无风险。

&#x20;   RESTFUL： C是3、E是0、R是2 ，较高投入无回报有风险。

- 如果它只约束你，却不告诉你能有什么好处，还在实际当中带来了负面问题。那我们需要它干什么？

## 建议

1. 不要完全遵循restful实践,不要过渡关注。

2. 简单使用GET 及 POST 两种请求方式即可。

3. URL 不要带资源ID，强烈不推荐`/orders/123123121`  这种形式。

4. URL 应该唯一，即使GET和POST不同，URL也不要相同。

5. POST 建议走 playload `application/json` 形式，从日志中拿出请求数据拼装调试更加方便，做objectMapper映射也很自然。

6. URL统一小写，使用中划线分隔， 例如：[/page/restful-api-request](https://restfulapi.cn/page/restful-api-request "/page/restful-api-request")

7. 返回包体 封装状态码，并且异常错误与正常状态格式保持结构保持一致。除开某些特定情况建议都走200状态码，特定情况 eg：服务器限流熔断操作。

8. 请求及返回字段，统一使用小写加下划线。

## 参考

[https://restfulapi.cn/page/restful-api-request](https://restfulapi.cn/page/restful-api-request "https://restfulapi.cn/page/restful-api-request")
