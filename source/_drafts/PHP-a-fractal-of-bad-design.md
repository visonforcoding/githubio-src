---
title: 'PHP: 糟糕设计的典型'
date: 2021-09-14 16:32:23
tags:
---

## 写在前面

我的脾气很暴躁，我抱怨很多事情。世界上有很多我不喜欢的技术，这真的在意料之中。
编程是一门非常年轻的学科，我们没有人知道我们在做什么。

结合斯特金定律(Sturgeon's Law)(译者注,该定律认为：任何事物,特别是用户创造的内容，90%都是垃圾),我有一生值得抱怨的东西。


这是不一样的。 PHP 不仅使用起来很笨拙，或者不适合我想要的东西，或者不是最理想的，或者违背我的宗教信仰。

 我可以告诉你所有关于我避免使用的语言的好东西，以及所有关于我喜欢的语言的坏事。
继续，问！它可以进行有趣的对话。

PHP 是唯一的例外。几乎 PHP 中的每个功能都以某种方式被破坏了。语言、框架、生态系统都很糟糕。
 我什至不能指出任何该死的事情，因为损害是如此系统性。每次我尝试编译 PHP 抱怨列表时，我都会陷入这种深度优先搜索，发现越来越多令人震惊的琐事。 （因此，分形。）
PHP 是一种尴尬，对我的手艺来说是一种折磨。它是如此破碎，但受到每个尚未学习其他任何东西的有能力的业余爱好者的称赞，以至于令人抓狂。它几乎没有什么可取之处，我宁愿忘记它的存在。
但我必须从我的系统中清除它。就这样，最后一次尝试。
一个类比

我只是脱口而出向梅尔解释了我的沮丧，她坚持要我在这里复制它。
我什至说不出 PHP 有什么问题，因为——好吧。

想象一下，你有一个工具箱。一套工具。看起来不错，里面有标准的东西。
你拿出一把螺丝刀，你会发现它是那些奇怪的三头东西之一。好吧，这对你来说不是很有用，但你猜它有时会派上用场。
你拔出锤子，但令你沮丧的是，它的两侧都有爪子部分。仍然可以使用，我的意思是，您可以用头部中间将其侧向固定。
你拔出钳子，但它们没有锯齿状表面；它平坦而光滑。这不太有用，但它仍然可以很好地转动螺栓，所以无论如何。
你去吧。盒子里的所有东西都有些古怪和古怪，但也许还不足以让它完全一文不值。并且整个系列没有明显的问题；它仍然拥有所有工具。
现在想象一下，你遇到数百万使用这个工具箱的木匠，他们告诉你“嘿嘿，这些工具有什么问题？他们都是我用过的，而且效果很好！”木匠向您展示他们建造的房屋，每个房间都是五边形，屋顶是倒置的。你敲前门，它只是向内倒塌，他们都因为你打破了他们的门而大喊大叫。
这就是 PHP 的错误所在。
姿态
我断言以下品质对于使语言变得高效和有用很重要，而 PHP 却疯狂地违反了这些品质。如果你不能同意这些是至关重要的，那么，我无法想象我们将如何达成一致。


原文 : https://www.pixelstech.net/article/1334166417-PHP%3A-a-fractal-of-bad-design
