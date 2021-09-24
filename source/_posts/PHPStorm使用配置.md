---
title: PHPStorm使用配置
date: 2021-09-24 17:34:26
tags:
---

最近又开始使用PHPStorm了，为什么是"又"？因为断断续续使用过几次，都中断过。要破解感觉还是麻烦，一直使用netbeans也感觉没什么问题。

由于最近在考虑`doctrine\annotation`,netbeans的支持能力还是不足，所以又开始体验`phpstorm`.
几个在netbeans里喜欢的功能，千方百计开始在phpstorm找回来。以下是记录。

<!--more-->

## 项目名显示git分支

![](https://vison-blog.oss-cn-beijing.aliyuncs.com/20210924174001.png)

如图，由于经常切换分支。有时候可能会在错误的分支上进行开发，项目名后面标上分支名这个功能我很喜欢。

发现phpstorm使用`GitToolBox`可以解决。

## 关闭显示项目路径

但是还有个问题是，项目名会显示项目地址，这点很烦。可以通过自定义phpstorm属性办到。

打开 Help/Edit Custom Properties...

新建 idea.properties file

```ini
project.tree.structure.show.url=false
ide.tree.horizontal.default.autoscrolling=false
```
## 隐藏nbproject

nbproject是netbeans的配置文件夹,在phpstorm项目中显示非常难受。

Preferences->File Types -> Files and Folders to Ignore.




