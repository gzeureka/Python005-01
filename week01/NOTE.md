## 学习笔记
### Python 环境
#### Python 的版本
[Python Documentation by Version | Python.org](https://www.python.org/doc/versions/)

#### Python 的安装
[Download Python | Python.org](https://www.python.org/downloads/)
注意：
	* 安装目录不要有中文、空格、特殊字符
	* 非必要情况下尽可能只安装一个 Python 解释器
	* 安装了多个版本的 Python 需要注意 PATH 环境变量的配置

#### REPL
	* python 命令：Python 的解释器，官方采用 CPython 版本
	* IPython 可以扩展 Python 的交互功能

#### pip
	* 方便安装第三方库
	* 国内常见的镜像站
		* 豆瓣：[Simple Index](http://pypi.doubanio.com/simple)
		* 清华：[pypi | 镜像站使用帮助 | 清华大学开源软件镜像站 | Tsinghua Open Source Mirror](https://mirrors.tuna.tsinghua.edu.cn/help/pypi/)
	* 升级 pip 的方法
		* 方法一：
`pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pip -U`
		* 方法二：		
```
pip config set global.index-url http://pypi.doubanio.com/simple/
pip install pip -U
```
	* pip 安装加速
		* 配置文件
			* Windows：`c:\Users\xxx\pip\pip.ini`
			* Linux：`~/.pip/pip.conf`
		* 配置文件格式
```
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
```

#### IDE
	* Visual Studio Code
	* PyCharm
	* Jupiter Notebook

#### 虚拟环境配置
在生产环境中虚拟环境是保持环境一致性的必备工具
	* 创建虚拟环境
	`python3 -m venv venv1`
	* 激活虚拟环境
	`source venv1/bin/activate`
	* 列出当前使用的包，以便迁移
	`pip3 freeze > requirements.txt`
	* 迁移：在另一个虚拟环境下，安装依赖的包
	`pip install -r requirements.txt`

### 语法基础
#### 基本数据类型
	* **None** 空对象
	* **Bool** 布尔值
	* **数值** 整数、浮点数、复数
	* **序列** 字符串、列表、元组
	* **集合** 字典
	* **可调用** 函数

#### 高级数据类型
	* **collections** 容器数据类型
	* **nametuple** 命名元组
	* **deque** 双端队列
	* **Counter** 计数器
	* **OrderedDict** 有顺序的字典

[collections — 容器数据类型 — Python 3.8.6 文档](https://docs.python.org/zh-cn/3.8/library/collections.html)

#### 控制流
	* **条件语句** `if…else`
	* **循环语句** `for…in`, `while`
	* **导入库、包、模块** `import`

注意：Python 使用缩进作为语句块的分隔

### 标准库常用模块
	* time
	* datetime
	* logging
	* random
	* json
	* pathlib
	* os.path
	* signal
	* re

### 手动实现守护进程
#### PEP 参考
[PEP 3143 — Standard daemon process library | Python.org](https://www.python.org/dev/peps/pep-3143/)

#### 基本步骤
参考 [APUE第13章 守护进程Deameon - 简书](https://www.jianshu.com/p/fbe51e1147af)
	1. 调用umask将文件模式创建屏蔽字设置为一个指定值。因为守护进程如果要创建文件，那么该文件必须指定权限，确保文件权限是自己期望的。
	2. 调用fork，然后使父进程exit，这是使得守护进程不关联终端的前提条件。另外，如果守护进程从终端命令行启动，那么父进程exit会使得shell认为该命令执行完毕从而正常返回。
	3. 调用setsid创建新会话，并丢掉控制终端。
	4. 将进程当前工作目录更改为根目录，因为进程可能启用于一个临时挂载的目录，如果进程一直执行，那么挂载目录就无法卸载。
	5. 5.关闭不再需要的文件描述符，主要防止守护进程误写。
	6. 打开/dev/null 文件，使得进程具有文件描述符0,1,2，这样做是为了预防守护进程调用的第三方接口或者库组件尝试从标准输入输出读写。

