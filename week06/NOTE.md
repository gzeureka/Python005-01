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
