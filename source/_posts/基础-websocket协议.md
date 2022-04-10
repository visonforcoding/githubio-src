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

我们用java来实现下websocket的协议。

```java
package com.vison.magpie.websocket;

import lombok.extern.slf4j.Slf4j;
import org.apache.log4j.Logger;

import java.io.IOException;
import java.lang.management.ManagementFactory;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.HashMap;
import java.util.Map;

@Slf4j
public class WsServer {


    private static Map<String, Socket> sockMap = new HashMap();

    private static int port = 9527;

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) throws IOException {
        String name = ManagementFactory.getRuntimeMXBean().getName();
        int port = WsServer.port;
        ServerSocket ss = new ServerSocket(port);
        log.info(String.format("server is running in %s of %s", port,name));
        for (;;) {
            Socket sock = ss.accept();
            log.info("connected from " + sock.getRemoteSocketAddress());
            Handler t = new Handler(sock);
            t.start();
        }
    }
}

```

```java
package com.vison.magpie.websocket;

import lombok.extern.slf4j.Slf4j;
import org.apache.commons.codec.digest.MessageDigestAlgorithms;

import java.io.*;
import java.net.Socket;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.Base64;
import java.util.Scanner;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

@Slf4j
public class Handler extends Thread {
    Socket sock;

    public Handler(Socket sock) {
        this.sock = sock;
    }

    public void run() {
        try (InputStream input = this.sock.getInputStream()) {
            try (OutputStream output = this.sock.getOutputStream()) {
                handle(input, output);
            }
        } catch (Exception e) {
            System.out.print(e.getClass());
            try {
                this.sock.close();
            } catch (IOException ioe) {
            }
            System.out.println("client disconnected.");
        }
    }

    private void handle(InputStream input, OutputStream output) throws IOException, InterruptedException {
        log.info("Process new http request...");
        var writer = new BufferedWriter(new OutputStreamWriter(output, StandardCharsets.UTF_8));
        Scanner s = new Scanner(input, StandardCharsets.UTF_8);
        String data = s.useDelimiter("\r\n").next();
        Matcher get = Pattern.compile("^GET").matcher(data);
        if (get.find()) {
            log.info("match get");
            String matchWebsocketKey = "";
            while (s.hasNext()) {
                String thisLine = s.next();
                Matcher matchWebsocket = Pattern.compile("Sec-WebSocket-Key: (.*)").matcher(thisLine);
                if (matchWebsocket.find()) {
                    matchWebsocketKey = matchWebsocket.group(1);
                    System.out.print(matchWebsocket.group());
                    handlerWebsocket(matchWebsocketKey,writer);
                    while (true){
                        int count=-1;
                        byte[] buff=new byte[1024];
                        count=input.read(buff);
                        System.out.println("接收的字节数："+count);
                        for(int i=0;i<count-6;i++){
                            buff[i+6]=(byte)(buff[i%4+2]^buff[i+6]);
                        }
                        System.out.println("接收的内容："+new String(buff, 6, count-6, "UTF-8"));
                        Thread.sleep(100);
                    }
                }
            }
        }
    }

    private void handlerWebsocket(String secWebSocketKey, BufferedWriter writer) throws IOException {
        log.info("hand with header");
        String secWebSocket = "";
        try {
            byte[] secWebSocketKeyByte = (secWebSocketKey + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11").getBytes(StandardCharsets.UTF_8);
            var digest = MessageDigest.getInstance(MessageDigestAlgorithms.SHA_1).
                    digest(secWebSocketKeyByte);
            secWebSocket = Base64.getEncoder().encodeToString(digest);
            System.out.print(secWebSocket);
        } catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
        }
        writer.write("HTTP/1.1 101 Switching Protocols\r\n");
        writer.write("Connection: Upgrade\r\n");
        writer.write("Upgrade: websocket\r\n");
        writer.write("Sec-WebSocket-Accept: " + secWebSocket + "\r\n");
        writer.write("\r\n"); // 空行标识Header和Body的分隔
        writer.flush();

    }

}
```

这里我们看到,我们在建立`websocket`连接之后，使用了一个轮训的方式进行数据读取和处理。

这与浏览器端友好的事件驱动形的API不同。那么如何实现服务端的事件驱动呢?

后续还需要继续探讨。