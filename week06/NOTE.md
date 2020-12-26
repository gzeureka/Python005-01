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
• `__getattribute__()`
• `__getattr__()`

异同：
• 都可以对实例属性进行获取拦截
• `__getattr__()`  适用于未定义的属性
• `__getattribute__() ` 对所有属性的访问都会调用该方法

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

# 如果同时存在，执行顺序是 __getattribute__ > __get_attr__ > __dict__
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
