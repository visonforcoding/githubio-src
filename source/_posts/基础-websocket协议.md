---
title: 基础|websocket协议
date: 2022-04-06 14:54:02
tags:
---

## 历史

- 2008年,`websocket`首次提出来是在HTML5规范里。
- 2009年12也，chrome浏览器第一个支持了websocket标准。

## 浏览器支持情况

![](https://vison-blog.oss-cn-beijing.aliyuncs.com/20220406150025.png)

到2011年，市面上所有的浏览器都支持了websocket.

## 协议

客户端请求

```
GET /chat HTTP/1.1
Host: server.example.com
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Key: x3JJHMbDL1EzLkh9GBhXDw==
Sec-WebSocket-Protocol: chat, superchat
Sec-WebSocket-Version: 13
Origin: http://example.com
```

服务应答

```
HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: HSmrc0sMlYUkAGmm5OPpG2HaGWk=
Sec-WebSocket-Protocol: chat
```

websocket由http协议升级而成，client的请求头必须包含`Upgrade: websocket`

除了 Upgrade 头部外，客户端还发送一个包含 base64编码的随机字节的 `Sec-WebSocket-Key` 头部，服务器用 `Sec-WebSocket-Accept`头部中的密钥散列作为响应。这是为了防止缓存代理重新发送以前的 WebSocket 对话，并且不提供任何身份验证、隐私或完整性。散列函数将固定字符串`258eafa5-e914-47da-95ca-c5ab0dc85b11`(一个 UUID)附加到来自 Sec-WebSocket-Key 报头的值(不从 base64解码) ，应用 sha-1散列函数，并使用 base64对结果进行编码。

`Rfc6455`标准要求密钥必须是一个 nonce，由随机选择的16字节值组成，该值已经以 base64编码，即 base64中的24字节(最后两个字节为 = =)。虽然一些宽松的 HTTP 服务器允许显示较短的密钥，但许多现代 HTTP 服务器会拒绝请求，并出现错误“无效的 Sec-WebSocket-Key 标头”。

一旦连接建立起来，客户端和服务器就可以以全双工模式来回发送 WebSocket 数据或文本帧。

## 实现
