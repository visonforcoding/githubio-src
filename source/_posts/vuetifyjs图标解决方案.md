---
title: vuetifyjs图标解决方案
date: 2020-08-24 10:24:41
tags:  web前端
---

![](http://img.rc5j.cn/blog20200824102537.png)

vuetifyjs官方提供的方法实际运用当中似乎会存在一些兼容问题，比如使用Font Awesome时有些图标就不会正常显示。

<!--more-->

## Font Awesome

```html
    <!-- 官方 -->
    <v-icon>fas fa-php</v-icon>
    <!-- 替代 -->
    <i class="fab fa-php v-icon"></i>
```
有些图标不显示的问题可以使用上述方法替代解决

## 使用阿里巴巴字体

阿里巴巴字体非常多非常庞大，基本想要的都有，而国外的很多不能用。所以可以使用阿里巴巴字体替代。

第一步：拷贝项目下面生成的fontclass代码：

可以在public/index.html 下用 link 标签引入

//at.alicdn.com/t/font_8d5l8fzk5b87iudi.css

第二步：挑选相应图标并获取类名，应用于页面：

<i class="iconfont icon-xxx"></i>