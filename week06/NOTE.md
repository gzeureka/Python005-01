# 学习笔记

## 类属性与对象属性
```python
class Human(object):
    # 静态字段
    live = True

    def __init__(self, name):
        # 普通字段
        self.name = name

man = Human('Adam')
woman = Human('Eve')

# 有静态字段，live 属性
Human.__dict__
# 有普通字段， name 属性
man.__dict__

# 实例可以使用普通字段也可以使用静态字段
man.name
man.live = False # 不会改变类的静态字段的值

# 查看实例属性
man.__dict__ # 普通字段有 live 变量
man.live # False
woman.live # True

# 类可以使用静态字段
Human.live

# 可以为类添加静态字段
Human.newattr = 1
```

## 类的属性作用域
* 可以为类添加静态字段
* 内置类型不能增加属性和方法
* 显示 object 类的所有子类

* 单下划线 `_` 开头的属性，人为约定不可修改
* 双下划线 `__` 开头的属性是私有属性，会被 Python 自动改名
* 魔术方法：双下划线 `__` 开头和结尾，不会自动改名

显示 object 类的所有子类
```python
print( ().__class__.__bases__[0].__subclasses__() )
```

## 类方法描述器
* 普通方法：至少一个 self 参数，表示该方法的对象
* 类方法：至少一个 cls 参数，表示该方法的类
* 静态方法：由类调用，无参数

三种方法在内存中都归属于类
```python
class Foo:
	def instance_method(self):
		...

	@classmethod
	def class_method(cls):
		...

	@staticmethod
	def class_method():
		...
```

## 静态方法描述器
用于放置与类相关的逻辑，改善代码的内聚性，但不能访问类及实例的属性。

## 描述器高级应用 __getattribute__
### 属性的处理
在类中，需要对**实例**获取属性这一行为进行操作，可以使用：
* `__getattribute__()`
* `__getattr__()`

异同：
* 都可以对实例属性进行获取拦截
* `__getattr__()`  适用于未定义的属性
* `__getattribute__() ` 对所有属性的访问都会调用该方法

```python
class Human2(object):
	'''
	__getattribute__ 对任意读取的属性进行截获
	'''

	def __init__(self):
		self.age = 18

	def __getattribute__(self, item):
		print(f'__getattribute__ called item:{item}')

h1 = Human2()

h1.age # age 的访问也会被截获

h1.noattr
```

```python
class Human2(object):
	'''
	拦截已存在的属性
	'''

	def __init__(self):
		self.age = 18

	def __getattribute__(self, item):
		print(f'__getattribute__ called item:{item}')
		return super().__getattribute__(item)

h1 = Human2()

print(h1.age) # 存在的属性返回取值

print(h1.noattr) # 不存在的属性抛出 AttributeError
```

```python
class Human2(object):
	'''
	将不存在的属性设置为 100 并返回，模拟 getattr 行为
	'''

	def __init__(self):
		self.age = 18

	def __getattribute__(self, item):
		print('Human2:__getattribute__')
		try:
			return super().__getattribute__(item)
		except Exception as e:
			self.__dict__[item] = 100
			return 100

h1 = Human2()

print(h1.age) # 存在的属性返回取值

print(h1.noattr) # 100
```

## 描述器高级应用 __getattr__
```python
class Human2(object):
	'''
	属性不再市里的 __dict__ 中， __getattr__ 被调用
	'''

	def __init__(self):
		self.age = 18

	def __getattr__(self, item):
		print(f'__getattr__ called item:{item}')
		# 不存在的属性返回默认值 'OK'
		return 'OK'

h1 = Human2()
print(h1.age) # 18
print(h1.noattr) # 'OK'
```

```python
class Human2(object):
	'''
	同时存在的调用顺序
	'''

	def __init__(self):
		self.age = 18

	def __getattr__(self, item):
		print('Human2:__getattr__')
		return 'Err 404'

	def __getattribute__(self, item):
		print('Human2:__getattribute__')
		return super().__getattribute__(item)

h1 = Human2()

# 如果同时存在，执行顺序是 __getattribute__ > __getattr__ > __dict__
# 输出
# Human2:__getattribute__
# 18
print(h1.age)

# 注意输出, noattr 的调用属性
# 输出
# Human2:__getattribute__
# Human2:__getattr__
# Err 404
print(h1.noattr)
```

描述器原理 & 属性描述符
### 属性描述符 property
实现特定协议（描述符）的类
property 类需要实现以下方法
* `__get__`
* `__set__`
* `__delete__`

```python
class Teacher:
	def __init__(self, name):
		self.name = name

	def __get__(self):
		return self.name

	def __set__(self, value):
		self.name = value

pythonteacher = Teacher('yin')
pythonteacher.name = 'wilson'
print(pythonteacher.name)
```

###  Django 中的 property

```python
# site-packages/django/db/models/base.py

class Model(metaclass=ModelBase):
	def _get_pk_val(self, meta=None):
		meta = meta or self._meta
		return getattr(self, meta.pk.attname)

	def _set_pk_val(self, value):
		return setattr(self, self._meta.ok.attname, value)

	pk = property(_gt_pk_val, _set_pk_val)
```

### __getattribute__ 的底层原理是描述器

```python
class Desc(object):
	'''
	通过打印来展示描述器的访问流程
	'''

	def __init__(self, name):
		self.name = name

	def __get__(self, instance, owner):
		print(f'__get__{instance} {owner}')
		return self.name

	def __set__(self, isntanc, value):
		print(f'__set__{instance} {value)')
		self.name = value

	def __delete__(self, instance):
		print(f'__delete__{instance}')
		del self.name

class MyObj(object):
	a = Desc('aaa')
	b = Desc('bbb')

my_object = MyObj()
print(my_object.a)

my_object.a = 456
print(my_object.a)
```

### property 用作装饰器

```python
class Human(object):
	def __init__(self, name):
		self.name = name

	# 将方法封装成属性
	@property
	def gender(self):
		return 'M'

h1 = Human('Adam')
h2 = Human('Eve')
h1.gender

# AttributeError
h2.gender = 'F'
```

```python
class Human2(object):
	def __init__(self):
		self._gender = None

	# 将方法封装成属性
	@property
	def gender2(self):
		print(self._gender)

	# 支持修改
	@gender2.setter
	def gender(self, value):
		self._gender = value

	# 支持删除
	@gender2.deleter
	def gender2(self):
		del self._gender

h = Human2()
h.gender = 'F'
h.gender
del h.gender
```

**另一种 property 写法**
```python
gender = property(get_, set_, del_, ‘other property’)
```

**建议**
* 被装饰函数建议使用相同的 `gender2`
* 使用 setter 并不能真正意义上实现无法写入， `gender` 被改名为 `_Article__gender`

property 本质并不是函数，而是特殊类（实现了数据描述符的类），如果一个对象同时定义了 `__get__()`  和  `__set()__` 方法，则成为**数据描述符**，如果仅定义了 `__get()__` 方法（例如 `__getattribute__`），则称为**非数据描述符**。

property 的优点：
* 代码更简洁，可读性、可维护性更强
* 更好的管理属性的访问
* 控制属性访问权限，提高数据安全性

## 面向对象编程 —— 继承
### 特性
#### 封装
* 将内容封装到某处
* 从某处调用被封装的内容

#### 继承
* 基本继承
* 多重继承

#### 重载
* Python 无法在语法层面实现数据类型重载，需要在代码逻辑上实现
* Python 可以实现参数个数重载

#### 多态
* Pyhon 不支持 Java 和 C# 这一类强类型语言中多态的写法，
* Python 使用“鸭子类型”

### 新式类
#### 新式类和经典类的区别
当前类或者父类继承了 object 类，那么该类便是新式类，否则便是经典类

#### object 和 type 的关系
* object 和 type 都属于 type 类 (class 'type')
* type 类由 type **元类**自身创建的。object 类是由元类 type 创建
* object 的父类为空，没有继承任何类
* type 的父类为 object 类 (class 'object')

### 类的继承
* 单一继承
* 多重继承
* 菱形继承（钻石继承）
* 继承机制 MRO
* MRO 的 C3 算法

```python
# 父类
class People(object):
    def __init__(self):
        self.gene = 'XY'
    def walk(self):
        print('I can walk')

# 子类
class Man(People):
    def __init__(self,name):
        self.name = name
    def work(self):
        print('work hard')

class Woman(People):
    def __init__(self,name):
        self.name = name    
    def shopping(self):
        print('buy buy buy')

p1 = Man('Adam')
p2 = Woman('Eve')

# 问题1 gene有没有被继承？
# 没有，子类的 __init__ 覆盖了父类的 __init__
p1.gene

# 问题2 People的父类是谁？
# object

# 问题3 能否实现多重层级继承
# 能

# 问题4 能否实现多个父类同时继承
# 能

```

Man 继承父类 People 的 `gene`
```python
class Man(People):
	def __init__(self, name):
		# 找到 Man 的父类 People，把 People 的对象转换为类 Man 的对象
		super().__init__(name)

	def work(self):
		print('work hard')
```

```python
>>> print('object', object.__class__, object.__bases__)
object <class 'type'> ()

>>> print('type', type.__class__, type.__bases__)
type <class 'type'> (<class 'object'>,)
```

多重继承
```python
class Son(Man, Woman):
	pass
```

继承顺序
```python
# 钻石继承
class BaseClass(object):
    num_base_calls = 0
    def call_me(self):
        print ("Calling method on Base Class")
        self.num_base_calls += 1

class LeftSubclass(BaseClass):
    num_left_calls = 0
    def call_me(self):
        print ("Calling method on Left Subclass")
        self.num_left_calls += 1

class RightSubclass(BaseClass):
    num_right_calls = 0
    def call_me(self):
        print("Calling method on Right Subclass")
        self.num_right_calls += 1

class Subclass(LeftSubclass,RightSubclass):
    pass

a = Subclass()
# Calling method on Left Subclass
a.call_me()

# MRO Method Resolution Order
print(Subclass.mro())
# 经典类使用深度优先，新式类使用广度优先
# 广度优先， 另外Python3 中不加(object)也是新式类，但是为了代码不会误运行在python2下产生意外结果，仍然建议增加
# >>> Subclass.mro()
# [<class '__main__.Subclass'>, <class '__main__.LeftSubclass'>, <class '__main__.RightSubclass'>, <class '__main__.BaseClass'>, <class 'object'>]

#  修改RightSubclass 的 父类为 Object
# >>> Subclass.mro()
# [<class '__main__.Subclass'>, <class '__main__.LeftSubclass'>, <class '__main__.BaseClass'>, <class '__main__.RightSubclass'>, <class 'object'>]

```

没有实现重载
```python
class  Klass(object):
    def A(self):
        pass
    def A(self,a, b):
        print(f'{a},{b}')


inst = Klass()
# 没有实现重载
# TypeError: A() missing 2 required positional arguments: 'a' and 'b'
inst.A()
```

## SOLID 设计原则与设计模式 & 单例模式
### SOLID 设计原则
* 单一责任原则 The Single Responsibility Principle
* 开放封闭原则 The Open Closed Principle
* 里氏替换原则 The Liskov Substitution Principle
* 依赖倒置原则 The Dependency Inversion Principle
* 接口分离原则 The Interface Segregation Principle

### 设计模式
* 设计模式用于解决普遍性问题
* 设计模式保证结构的完整性

### 单例模式
1. 对象只存在一个实例
2. __init__ 和 __new__ 的区别：
	* __new__ 是实例创建之前被调用，返回该实例对象，是静态方法
	* __init__ 是实例对象创建完成后被调用，是实例方法
	* __new__ 先被调用，__init__ 后被调用
	* __new__ 的返回值（实例）将传递给 __init__ 方法的第一个参数，__init__ 给这个 实例设置相关参数

### 装饰器实现单例模式
```python
def singleton(cls):
	instances = {}

	def getinstance():
		if cls not in instances:
			instances[cls] =  cls()
			return instances[cls]

	return getinstance

@singleton
class MyClass:
	pass

m1 = MyClass()
m2 = MyClass()
# m1, m2 的 id 相同
print(id(m1))
print(id(m2))
```

### __new__ 实现单例模式
`__new__` 和 `__init__` 的关系
```python
class Foo(object):
	def __new__(cls, name):
		print('trace __new__')
		return super().__new__(cls)

	def __init__(self, name):
		print('trace __init__')
		super().__init__()
		self.name = name

# 输出：
# trace __new__
# trace __init__
bar = Foo('test')

# 输出：
# 'test'
bar.name

# 相当于执行下面的操作
bar = Foo.__new__(Foo, 'test')
if isinstance(bar, Foo):
	Foo.__init__(bar, 'test')

```

`__new__` 方式实现单例模式
```python
class Singleton2(object):
	__ininstance = False # 默认没有被实例化
	def __new__(cls, *args, **kwargs):
		if cls.__isinstance:
			return cls.isinstance # 返回实例化对象
		cls.__isinstance = object.__new__(cls) # 实例化
		return cls.__isinstance
```

object 定义了一个名为 Singleton 的单例，它满足单例的 3 个需求
1. 只能有一个实例
2. 它必须自行创建这个实例
3. 它必须自行向整个系统提供这个实例
```python
# 方法1，实现 __new__ 方法
# 并在将一个类的实例绑定到类变量 _instance 上，
# 如果 cls._instance 为 None，说明该类还没有实例化，实例化该类并返回
# 如果 cls._instance 不为 None，直接返回 cls._instance
class Singleton(object):
	_instance = None

	def __new__(cls, args, **kwargs):
		if not cls._instance:
			cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
		return cls._instance

if __name__ == '__main__':
	s1 = Singleton()
	s2 = Singleton()
	assert id(s1) == id(s2)
```

以上单例模式只能用于单线程环境，多线程需要进行加锁
```python
import threading

class Singleton(object):
	objs = {}
	objs_locker = threading.Lock()

	def __new__(cls, *args, **kwargs):
		if cls in cls.objs:
			return cls.objs[cls]
		cls.objs_locker.acquire()
		try:
			if cls in cls.objs: ## double check locking
				return cls.objs[cls]
			cls.objs[cls] = object.__new__(cls)
		finally:
			cls.objs_locker.release()
```

上例利用双检查锁机制，确保了在并发环境下 Singleton 的正确实现，但这个方案还有以下两个问题：
1. 如果 Singleton 的子类重载了 `__new__()` 方法，会覆盖或者干扰 Singleton 类中 `__new__()` 的执行
2. 如果子类有 `__init__()` 方法，那么每次实例化该 Singleton 的时候 `__init__()` 都会被调用，这是**不应该**的，`__init__()` 只应该在创建实例的时候被调用一次

这两个问题当然可以解决，比如通过文档告知其他程序员，子类化  Singleton 的时候，请务必记得调用父类的 `__new__()` 方法；而第二个问题也可以通过替换掉 `__init__()` 方法来确保它只被调用一次。但是，为了实现一个单例，做大量的、水面下的工作让人感觉相当不 Pythonic。这也引起了 Python 社区的反思，有人开始重新审视 Python 的语法元素，发现模块采用的其实是天然的单例实现方式：
	* 所有的变量都会绑定到模块
	* 模块只初始化一次
	* import 机制是线程安全的
```python
# World.py
import Sun

def run():
	while True:
		Sun.rise()
		Sun.set()

# main.py

import World
World.run()
```

## 工厂模式
### 静态工厂模式
```python
class Human(object):
	def __init__(self):
		self.name = None
		self.gender = None

	def getName(self):
		return self.name

	def getGender(self):
		return self.gender

class Man(Human):
	def __init__(self, name):
		print(f'Hi, man {name}')

class Woman(Human):
	def __init__(self, name):
		print(f'Hi, woman {name}')

class Factory:
	def getPerson(self, name, gender):
		if gender == 'M':
			return Man(name)
		elif gender == 'F':
			return Woman(name)
		else:
			pass

if __name == '__main__':
	factory = Factory()
	person = factory.getPerson('Adam', 'M')
```

### 类工厂模式
```python
# 返回在函数内动态创建的类
def factory2(func):
	class klass: pass
	#setattr 需要三个参数：对象，key，value
	print(func)
	setattr(klass, func.__name__, func)
	return klass

def say_foo(self):
	print('bar')

Foo = factory2(say_foo)
foo = Foo()
foo.say_foo()
```

## 元类
* 元类是关于类的类，是类的模板。
* 元类是用来控制如何创建类的，正如类是创建对象的模板一样。
* 元类的实例为类，正如类的实例为对象
* 创建元类的两种方法
	1. type
		* type（类名，父类的元组（根据继承的需要，可以为空），包含属性的字典（名字和值））
	2. class

```python
# 使用 type 元类创建类
def hi():
	print('Hi metaclass')

# type 的三个参数：类名，父类的元组，类的成员
Foo = type('Foo', (), {'say_hi':hi})
foo = Foo
foo.say_hi()

# 元类 type 首先是一个类，所以比类工厂的方法更灵活多变，可以自由创建子类来扩展元类的能力
```

```python
def pop_value(self, dict_value):
	for key in self.keys():
		if self.__getitem__(key) == dict_value:
			self.pop(key)
			break

# 元类要求，必须继承自 type
class DelValue(type):
	# 元类要求，必须实现 __new__ 方法

	def __new__(cls, name, bases, attrs):
		attrs['pop_value'] = pop_value
		return type.__new__(cls, name, bases, attrs)

class DelDictValue(dict, metaclass=DelValue):
	# python2 的用法，在 python3 不支持
	# __metaclass__ = DelValue
	pass

d = DelDictValue()
d['a'] = 'A'
d['b'] = 'B'
d['c'] = 'C'
d.pop_value('C')
for k,v in d.items():
	print(k,v)
```

