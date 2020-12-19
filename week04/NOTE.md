# 使用 Django 展示豆瓣电影中某个电影的短评和星级等相关信息：
1. 要求使用 MySQL 存储短评内容（至少 20 条）以及短评所对应的星级；

https://github.com/gzeureka/Python005-01/blob/main/week04/t1.sql

2. 展示高于 3 星级（不包括 3 星级）的短评内容和它对应的星级；

https://github.com/gzeureka/Python005-01/blob/main/week04/MyDjango/Douban/views.py
```
from django.shortcuts import render

# Create your views here.
from .models import T1
from django.db.models import Avg

def books_short(request):
    ###  从models取数据传给template  ###
    # shorts = T1.objects.all()
    # 展示高于 3 星级（不包括 3 星级）的短评内容和它对应的星级；
    shorts = T1.objects.filter(**{'n_star__gt': 3})
    # 评论数量
    counter = T1.objects.all().count()

    # 平均星级
    # star_value = T1.objects.values('n_star')
    star_avg =f" {T1.objects.aggregate(Avg('n_star'))['n_star__avg']:0.1f} "
    # 情感倾向
    sent_avg =f" {T1.objects.aggregate(Avg('sentiment'))['sentiment__avg']:0.2f} "

    # 正向数量
    queryset = T1.objects.values('sentiment')
    condtions = {'sentiment__gte': 0.5}
    plus = queryset.filter(**condtions).count()

    # 负向数量
    queryset = T1.objects.values('sentiment')
    condtions = {'sentiment__lt': 0.5}
    minus = queryset.filter(**condtions).count()

    # return render(request, 'douban.html', locals())
    return render(request, 'result.html', locals())
```

# 学习笔记 - Django Web 开发

## 开发环境配置
### Django 的特点
* 采用了 MTV (Model Template View) 的框架
* 强调快速开发和代码复用 DRY （Do not Repeat Yourself）
* 组件丰富
	* ORM 映射类构件数据模型
	* URL 支持正则表达式
	* 模板可继承
	* 内置用户认证，提供用户认证和权限功能
	* admin 管理系统
	* 内置表单模型、Cache 缓存系统、国际化系统等

### Django 的版本
Django 最新版本 3.0，目前用得比较多的是 2.2.13(LTS)

```
$ pip install --upgradedjango=2.2.13

>>> import django
>>> django.__version__
```

## 创建项目和目录结构
```
$ django-admin startproject MyDjango

$ python manage.py help

$ python manage.py startapp index

$ python manage.py runserver

$ python manager.py runserver 0.0.0.0:80
```

## 主要配置文件 settings.py
内容包括：
* 项目路径
* 密钥
* 域名访问权限
* App 列表
* 静态资源，包括 CSS、JavaScript、图片等
* 模板文件
* 数据库配置
* 缓存
* 中间件

## urls 调度器 (URLConf)
### Django 如何处理一个请求
当一个用户请求 Django 站点的一个页面：
1. 如果传入 HttpRequest 对象拥有 urlconf 属性（通过中间件设置），它的值将被用来代替 ROOT_URLCONF 设置。
2. Django 加载 URLConf 模块并寻找可用的 urlpatterns，Django 依次匹配每个 URL 模式，在与请求的 URL 匹配的第一个模式停下来。
3. 一旦有 URL 匹配成功，Django 导入并调用相关的视图，视图会获得如下参数：
    * 一个 HttpRequest 对象
    * 一个或多个位置参数
4. 如果有没 URL 被匹配，或者匹配过程中出现了异常，Django 会调用一个适当的错误处理视图。

### 增加项目的 urls
```
from django.urls import path, include

urlpatterns = [
    path('', include('index.urls'))
]
```

### 增加 index 的 urls
```
# index/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index)
]

# index/views.py
from django.shortcuts import render
from django.http import HttpResponse
def index(request):
    return HttpResponse('Hello Django!')
```

## 模块和包
* 模块：`.py` 结尾的 Python 程序
* 包： 存放多个模块的目录
* `__init__.py` 包运行的初始化文件，可以是空文件

常见的导入方式：
```
import ...

from ... import ...

from ... import ... as ...
```

## 让 URL 支持变量
URL 变量类型包括：
* str
* int
* slug
* uuid
* path

```
path('<int:year>', views.myyear)
```

## URL 正则和自定义过滤器
### 正则
```
# urls.py

re_path('(?P<year>[0-9]{4}.html)', views.myyear, name='urlyear')

# views.py
def myyear(request, year):
    return render(request, 'yearview.html')

# Templates 文件夹增加 yearview.html
<a href="{% url 'urlyear' 2020 %}">2020 booklist</a>
```

### 自定义匹配规则
```
# urls.py

from django.urls import path, re_path, register_converter
from . import views, converters

register_converter(converters.IntConverter, 'myint')

urlpatterns = [
    path('<myint:year>', views.year)
]

# converters.py

class IntConverter:
    regex = '[0-9]+'

    def to_python(self, value):
        return int(value)
    
    def to_url(self, value):
        return str(value)
```

## view 视图快捷方式
Django 快捷函数：
* render() 将给定的模板与给定的上下文字典组合在一起，并以渲染的文本返回一个 HttpResponse 对象
* redirect() 将一个 HttpResponseRedirect 返回到传递的参数的适当的 URL
* get_object_or_404() 在给定的模型管理器（model manager）上调用 get()，但它会引发 Http 404 而不是模型的 DoesNotExist 异常 

## 使用 ORM 创建数据表
* 每个模型都是一个 Python 的类，这些类继承 djanogo.db.models.Model
* 模型类的每个属性都相当于一个数据库的字段
* 利用这些，Django 提供了一个自动生成访问数据库的 API

常见报错
1. `django.core.exceptions.ImproperlyConfigured: Error loading MySQLdb module: No module named 'MySQLdb'`
解决方法：在 __init__.py 文件中添加以下代码即可
```
import pymysql
pymysql.install_as_MySQLdb()
```

2. `version = Database.version_info`
打开 `venv/lib/python3.8/site-packages/django/db/backends/mysql/base.py` 添加注释：
```
# if version < (1, 3, 13):
# raise ImproperlyConfigured('mysqlclient 1.3.13 or newer is required; you have %s.' % Database.__version__)
```

3. `AttributeError: 'str' object has no attribute 'decode'`
出现这个错误之后可以根据错误提示找到文件位置，打开 `/venv/lib/python3.8/site-packages/django/db/backends/mysql/operations.py` 文件，找到以下代码添加注释：
```
def last_executed_query(self, cursor, sql, params):
    query = getattr(cursor, '_executed', None)
    # if query is not None:
    #     query = query.decode(errors='replace')
    return query
```

## Django 模板开发
* 模板变量 {{ variables }}
* 从 URL 获取模板变量 {% url 'yrlyear' 2020 %}
* 读取静态资源内容 {% static "css/header.css" %}
* for 遍历标签 {% for type in type_List %} {% endfor %}
* if 判断标签 {% if name.type=type.type %} {% endif %}
