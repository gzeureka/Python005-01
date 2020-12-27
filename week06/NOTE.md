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

