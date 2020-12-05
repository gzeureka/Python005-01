# 学习笔记

## Socket API

* socket()
* bind()
* listen()
* accept()
* recv()
* send()
* close()

## requests 库
[Requests: HTTP for Humans](https://requests.readthedocs.io/en/master/)

## 异常捕获
[参考文档](https://docs.python.org/zh-cn/3.6/library/exceptions.html) 

### 异常处理机制的原理
* 异常也是一个类
* 异常捕获过程
	1. 异常类把错误消息打包到一个对象
	2. 然后该对象会自动查找到调用栈
	3. 直到运行系统找到明确声明如何处理这些类异常的位置 
* 所有异常继承自 BaseException
* Traceback 显示了出错的位置，显示的顺序和异常信息对象传播的方向是相反的

### 异常信息与异常捕获
* 异常信息在 Traceback 信息的最后一行，有不同的类似
* 捕获异常可以使用 `try...except`  语法
* `try...except`  支持多重异常处理
* 常见的异常类型主要有：
	1. LookupError 下的 IndexError 和 KeyError
	2. IOError
	3. NameError
	4. TypeError
	5. AttributeError
	6. ZeroDivisionError

### pretty_errors
[美化异常输出](https://github.com/onelivesleft/PrettyErrors/)

## 深入了解 HTTP 协议
### 基本概念
    1. 传输数据和建立连接：统一资源标识符（Uniform Resource Identifiers, URI）
    2. 消息请求 Reuest
    3. 消息响应 Response
    4. 状态码
    5. HTTP 请求方法

### requests 库
使用 requests 库进行 HTTP 请求：
    1. 发送请求
    2. 传递 URL 参数
    3. 定制请求头
    4. POST 请求
    5. 响应状态
    6. cookie
    7. 请求超时处理
    8. 错误和异常处理

## 使用 XPath 匹配网页内容 & 实现翻页功能

##  使用自顶向下的设计思维拆分项目代码
### 什么是自顶向下设计？
* 从整体分析一个比较复杂的大问题
* 分析方法可以重用
* 拆分到你能解决的范畴

### 实战将爬虫代码拆解模拟 Scrapy 框架
* 什么是 Scrapy？
* Scrapy [架构介绍](http://ibloodline.com/articles/2017/12/14/Scrapy-Architecture.html)
* 为什么要模拟 Scrapy？
