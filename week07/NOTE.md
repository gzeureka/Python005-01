# 学习笔记
## 变量的赋值
* 可变数据类型
	* 列表 list
	* 字典 dict
* 不可变数据类型
	* 整形 int
	* 浮点型 float
	* 字符串 string
	* 元组 tuple

## 容器序列的深浅复制
### 序列分类
* 容器序列：list, tuple, collections.deque 等，能存放不同类型的数据
* 扁平序列：str, bytes, bytearray, memoryview（内存视图）,array.array 等，**只能存放相同类型的数据**。

### 可变类型存在深拷贝、浅拷贝问题
注意：不可变类型（数字、字符串、元组）没有拷贝问题

```python
import copy

copy.copy(object)
copy.deepcopy(object)
```
## 字典与扩展内置数据类型
### 字典与哈希
key 必须是不可变的数据类型

### 扩展内置数据类型
使用 collections
* namedtuple
* Counter
* deque

### 计算3维空间内两点之间的距离
* 使用 numpy
* 使用 namedtuple 实现
```python
from collections import namedtuple
from math import sqrt
Point = namedtuple('Ponit', ['x','y','z'])

class Vector(Point):
    def __init__(self, p1, p2, p3):
        super(Vector).__init__()
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
    
    def __sub__(self, other):
        tmp = (self.p1 - other.p1)**2+(self.p2 - other.p2)**2+(self.p3 - other.p3)**2
        return sqrt(tmp)

p1 = Vector(1, 2, 3)
p2 = Vector(4, 5, 6)

p1-p2
```

## 函数的调用
函数是可调用对象，自定义的类可以通过实现 `__call__` 魔术方法让类实例可作为函数使用

## 变量作用域
高级语言对变量的使用：
* 变量声明
* 定义类型（分配内存空间大小）
* 初始化（赋值、填充内存）
* 引用（通过对象名称调用对象内存数据）

Python 和高级语言由很大差别，在模块、类、函数中定义，才有作用域的概念。

```python

# L G
x = 'Global'
def func2():
    x = 'Enclosing'

    def func3():
        x = 'Local'

        print (x)
    func3()
print(x)
func2()



# E
x = 'Global'
def func4():
    x = 'Enclosing'
    def func5():
        return x
    return func5

var = func4()
print( var() )


# B
print (dir (__builtins__) )
```

## 函数工具与高阶函数
### 偏函数
`functors.partial` 返回一个可调用的 partial 对象
使用方法：`partial(func, *args, **kw)`
注意：
	* func 是必需的参数
	* 至少需要一个 args 或 kw 参数

### 高阶函数
#### Lambda 表达式
Lambda 只是表达式，不是所有的函数逻辑都能封装进去
```python
k = lambda x:x+1
print(k(1))
```

Lambda 表达式后面只能有一个表达式
* 实现简单函数的时候可以使用 Lambda 表达式代替
* 使用高阶函数的时候一般使用 Lambda 表达式

#### 高阶函数
高阶：参数是函数，或者返回值是函数
常见的高阶函数：map, reduce, filter, apply
apply 在 Python 2.3 被移除，reduce 被放在 functools 包中
推导式和生成器表达式可以替代 map 和 filter 函数

```python
# map
def square(x):
    return x**2

m = map(square, range(10))
next(m)
list(m)
[square(x) for x in range(10)]
dir(m)

# reduce
# reduce(f, [x1, x2, x3]) = f(f(x1, x2), x3)
from functools import reduce
def add(x, y):
    return x + y

reduce(add, [1, 3, 5, 7, 9])
#25


# filter
def is_odd(n):
    return n % 2 == 1

list(filter(is_odd, [1, 2, 4, 5, 6, 9, 10, 15]))


# 偏函数
def add(x, y):
    return x + y

import functools
add_1 = functools.partial(add, 1)
add_1(10)

import itertools
g = itertools.count()
next(g)
next(g)
auto_add_1 = functools.partial(next, g)
auto_add_1()


sorted(['bob', 'about', 'Zoo', 'Credit'])
sorted(['bob', 'about', 'Zoo', 'Credit'], key=str.lower)
sorted(['bob', 'about', 'Zoo', 'Credit'], key=str.lower, reverse=True)
```

## 闭包
### 返回值
#### 返回的关键字
* `return`
* `yield`

#### 返回的对象
* 可调用对象——闭包（装饰器）

```python
# 如果line()的定义中引用了外部的变量
def line_conf():
    b = 10
    def line(x):
        return 2*x+b
    return line       

my_line = line_conf()
print(my_line(5))

# 编译后函数体保存的局部变量
# ('x',)
print(my_line.__code__.co_varnames)

# 编译后函数体保存的自由变量
# ('b', ) line_conf 中定义的 b
print(my_line.__code__.co_freevars)

# 自由变量真正的值
# 10
print(my_line.__closure__[0].cell_contents)
```

```python
# 函数和对象比较有哪些不同的属性
# 函数还有哪些属性
def func(): 
    pass
func_magic = dir(func)

# 常规对象有哪些属性
class ClassA():
    pass
obj = ClassA()
obj_magic = dir(obj)

# 比较函数和对象的默认属性
# {'__get__', '__call__', '__kwdefaults__', '__globals__', '__defaults__', '__name__', '__code__', '__closure__', '__qualname__', '__annotations__'}
set(func_magic) - set(obj_magic)
```

`nonlocal`
```python
# 内部函数对外部函数作用域里变量的引用（非全局变量）则称内部函数为闭包
def counter(start=0):
   count=[start]
   def incr():
       count[0]+=1
       return count[0]
   return incr

c1=counter(10)

print(c1())
# 结果：11
print(c1())
# 结果：12

# nonlocal访问外部函数的局部变量
# 注意start的位置，return的作用域和函数内的作用域不同
def counter2(start=0):
    def incr():
        nonlocal start
        start+=1
        return start
    return incr

c1=counter2(5)
# 6
print(c1())
# 7
print(c1())

c2=counter2(50)
# 51
print(c2())
# 52
print(c2())

# 8
print(c1())
# 9
print(c1())

# 53
print(c2())
# 54
print(c2())
```


## 被装饰函数带参数和返回值的处理
```python
# 被修饰函数带参数
def outer(func):
    def inner(a,b):
        print(f'inner: {func.__name__}')
        print(a,b)
        func(a,b)
    return inner

@outer
def foo(a,b):
    print(a+b)
    print(f'foo: {foo.__name__}')
    
# inner: foo
# 1 2
# 3
# foo: inner    
foo(1,2)

# 'inner'
foo.__name__

############################################

# 被修饰函数带不定长参数
def outer2(func):
    def inner2(*args,**kwargs):
        func(*args,**kwargs)
    return inner2

@outer2
def foo2(a,b,c):
    print(a+b+c)

# 9
foo2(1,3,5)

############################################

# 被修饰函数带返回值
# 通用的装饰器框架
def outer3(func):
    def inner3(*args,**kwargs):
        ###
        ret = func(*args,**kwargs)
        ###
        return ret
    return inner3

@outer3
def foo3(a,b,c):
    return (a+b+c)

# 9
print(foo3(1,3,5))
```

```python
# 装饰器带参数 
def outer_arg(bar):
    def outer(func):
        def inner(*args,**kwargs):
            ret = func(*args,**kwargs)
            print(bar)
            return ret
        return inner
    return outer

# 相当于outer_arg('foo_arg')(foo)()
@outer_arg('foo_arg')
def foo(a,b,c):
    return (a+b+c)
    
print(foo(1,3,5))

############################################

# 装饰器堆叠
@classmethod
@synchronized(lock)
def foo(cls):
    pass


def foo(cls):
    pass
foo2 = synchronized(lock)(foo)
foo3 = classmethod(foo2)
foo = foo3
```

## Python 内置装饰器
### `functools.wraps`
```python
# 内置的装饰方法函数

# functools.wraps
# @wraps接受一个函数来进行装饰
# 并加入了复制函数名称、注释文档、参数列表等等的功能
# 在装饰器里面可以访问在装饰之前的函数的属性
# @functools.wraps(wrapped, assigned=WRAPPER_ASSIGNMENTS, updated=WRAPPER_UPDATES)
# 用于在定义包装器函数时发起调用 update_wrapper() 作为函数装饰器。 
# 它等价于 partial(update_wrapper, wrapped=wrapped, assigned=assigned, updated=updated)。

from time import ctime,sleep
from functools import wraps
def outer_arg(bar):
    def outer(func):
        # 结构不变增加wraps
        @wraps(func)
        def inner(*args,**kwargs):
            print("%s called at %s"%(func.__name__,ctime()))
            ret = func(*args,**kwargs)
            print(bar)
            return ret
        return inner
    return outer

@outer_arg('foo_arg')
def foo(a,b,c):
    """  __doc__  """
    return (a+b+c)
    
print(foo.__name__)


########################
# flask 使用@wraps()的案例
from functools import wraps
 
def requires_auth(func):
    @wraps(func)
    def auth_method(*args, **kwargs):
        if not auth:
            authenticate()
        return func(*args, **kwargs)
    return auth_method

@requires_auth
def func_demo():
    pass

########################

from functools import wraps
 
def logit(logfile='out.log'):
    def logging_decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            log_string = func.__name__ + " was called"
            print(log_string)
            with open(logfile, 'a') as opened_file:
                opened_file.write(log_string + '\n')
            return func(*args, **kwargs)
        return wrapped_function
    return logging_decorator
 
@logit()
def myfunc1():
    pass
 
myfunc1()
# Output: myfunc1 was called
 
@logit(logfile='func2.log')
def myfunc2():
    pass
 
myfunc2()

# Output: myfunc2 was called



##########################
# 可以使用wrapt包替代@wraps
# # wrapt包 https://wrapt.readthedocs.io/en/latest/quick-start.html
#  @wrapt.decorator
#  def wrapper(func, instance, args, kwargs):

import wrapt

def with_arguments(myarg1, myarg2):
    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        return wrapped(*args, **kwargs)
    return wrapper

@with_arguments(1, 2)
def function():
    pass
```

### `functools.lru_cache`
```python
# functools.lru_cache
# 《fluent python》的例子
# functools.lru_cache(maxsize=128, typed=False)有两个可选参数
# maxsize代表缓存的内存占用值，超过这个值之后，旧的结果就会被释放
# typed若为True，则会把不同的参数类型得到的结果分开保存
import functools
@functools.lru_cache()
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-2) + fibonacci(n-1)

if __name__=='__main__':
    import timeit
    print(timeit.timeit("fibonacci(6)", setup="from __main__ import fibonacci"))

```

## 类装饰器
### 用类装饰器来装饰函数
* 在类装饰器中需要实现  `__call__` 魔术方法，把类实例做成可调用对象来模拟函数
```python
# Python 2.6 开始添加类装饰器
from functools import wraps

class MyClass(object):
    def __init__(self, var='init_var', *args, **kwargs):
        self._v = var
        super(MyClass, self).__init__(*args, **kwargs)
    
    def __call__(self, func):
        # 类的函数装饰器
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            func_name = func.__name__ + " was called"
            print(func_name)
            return func(*args, **kwargs)
        return wrapped_function

def myfunc():
    pass

# 与 `@` 语法糖的效果相同
MyClass(100)(myfunc)()

# 其他经常用在类装饰器的python自带装饰器
# classmethod
# staticmethod
# property

# 另一个示例
class Count(object):
    def __init__(self,func):
        self._func = func
        self.num_calls = 0
    
    def __call__(self, *args, **kargs):
        self.num_calls += 1
        print(f'num of call is {self.num_calls}')
        return self._func(*args, **kargs)

@Count
def example():
    print('hello')

example()
print(type(example))


# 其他常用的排序和计数相关用法
a = (1, 2, 3, 4)
a.sort()
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
# AttributeError: 'tuple' object has no attribute 'sort'
sorted(a)
# [1, 2, 3, 4]
# sorted 支持更多场景  多维list 字典混合list list混合字典


# 计数有没有更优雅、更Pythonic的解决方法呢？
# 答案是使用collections.Counter。
from collections import  Counter
Counter(some_data)
# 利用most_common()方法可以找出前N个出现频率最高的元素以及它们对应的次数
Counter(some_data).most_common(2)
```

### 用装饰器来装饰类
```python
# 装饰类
def decorator(aClass):
    class newClass(object):
        def __init__(self, args):
            self.times = 0
            self.wrapped = aClass(args)
            
        def display(self):
            # 将runtimes()替换为display()
            self.times += 1
            print("run times", self.times)
            self.wrapped.display()
    return newClass

@decorator
class MyClass(object):
    def __init__(self, number):
        self.number = number
    # 重写display
    def display(self):
        print("number is",self.number)

six = MyClass(6)
for i in range(5):
    six.display()

```

## 官方文档中的装饰器代码阅读指南
* PEP557 Data Class
```python
# 官方文档装饰器的其他用途举例

# 向一个函数添加属性
def attrs(**kwds):
    def decorate(f):
        for k in kwds:
            setattr(f, k, kwds[k])
        return f
    return decorate

@attrs(versionadded="2.2",
       author="Guido van Rossum")
def mymethod(f):
    pass

##############################

# 函数参数观察器
import functools
def trace(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        print(f, args, kwargs)
        result = f(*args, **kwargs)
        print(result)
    return decorated_function
@trace
def greet(greeting, name):
    return '{}, {}!'.format(greeting, name)

greet('better','me')

############################################

# Python3.7 引入 Data Class  PEP557

class MyClass:
    def __init__(self, var_a, var_b):
        self.var_a = var_a
        self.var_b = var_b

    def __eq__(self, other):
        if self.__class__ is not other.__class__:
            return False
        return (self.var_a, self.var_b) == (other.var_a, other.var_b)
        
var3 = MyClass('x','y')
var4 = MyClass('x','y')

var3 == var4

from dataclasses import dataclass
@dataclass
class MyClass:
    var_a: str
    var_b: str

var_1 = MyClass('x','y')
var_2 = MyClass('x','y')

# 不用在类中重新封装 __eq__

var_1 == var_2
# 存在的问题: var_a var_b不能作为类属性访问，只能作为实例属性访问

##########################

# 如下的类装饰器实现了一个用于类实例属性的Private声明
# 属性存储在一个实例上，或者从其一个类继承而来
# 不接受从装饰的类的外部对这样的属性的获取和修改访问
# 但是，仍然允许类自身在其方法中自由地访问那些名称
# 类似于Java中的private属性

traceMe = False
def trace(*args):
    if traceMe:
        print('['+ ' '.join(map(str,args))+ ']')

def Private(*privates):
    def onDecorator(aClass):
        class onInstance:
            def __init__(self,*args,**kargs):
                self.wrapped = aClass(*args,**kargs)
            def __getattr__(self,attr):
                trace('get:',attr)
                if attr in privates:
                    raise TypeError('private attribute fetch:'+attr)
                else:
                    return getattr(self.wrapped,attr)
            def __setattr__(self,attr,value):
                trace('set:',attr,value)
                if attr == 'wrapped': # 这里捕捉对wrapped的赋值
                    self.__dict__[attr] = value
                elif attr in privates:
                    raise TypeError('private attribute change:'+attr)
                else: # 这里捕捉对wrapped.attr的赋值
                    setattr(self.wrapped,attr,value)
        return onInstance
    return onDecorator

if __name__ == '__main__':
    traceMe = True

    @Private('data','size')
    class Doubler:
        def __init__(self,label,start):
            self.label = label
            self.data = start
        def size(self):
            return len(self.data)
        def double(self):
            for i in range(self.size()):
                self.data[i] = self.data[i] * 2
        def display(self):
            print('%s => %s'%(self.label,self.data))

    X = Doubler('X is',[1,2,3])
    Y = Doubler('Y is',[-10,-20,-30])
    print(X.label)
    X.display()
    X.double()
    X.display()
    print(Y.label)
    Y.display()
    Y.double()
    Y.label = 'Spam'
    Y.display()

    # 这些访问都会引发异常
    print(X.size())
    print(X.data)
    X.data = [1,1,1]
    X.size = lambda S:0
    print(Y.data)
    print(Y.size())

# 这个示例运用了装饰器参数等语法，稍微有些复杂，运行结果如下：
# [set: wrapped <__main__.Doubler object at 0x03421F10>]
# [set: wrapped <__main__.Doubler object at 0x031B7470>]
# [get: label]
# X is
# [get: display]
# X is => [1, 2, 3]
# [get: double]
# [get: display]
# X is => [2, 4, 6]
# [get: label]
# Y is
# [get: display]
# Y is => [-10, -20, -30]
# [get: double]
# [set: label Spam]
# [get: display]
```
