# crm

crm其实就是一个组件，就是对数据库实现增删改查的组件，它分为两部分，一部分是怎删改查页面，一部分是权限管理页面。增删改查页面其实就是对数据库实现增删改查，当然还有高级一点的一些组合搜索等功能，而且可以自定义，也就是实现再配置文件里面随意修改

知识点：

* django Admin

### curd页面

问题一：如何显示数据库内容

我们的curd增删改查页面是实现在页面上对数据库进行增删改查的，那么，就要首先将数据库中的内容在页面上显示出来，以前我们在页面上显示内容都是在后台获取数据库数据，然后在前端循环取出展示，但是，这样有一个弊端，就是我们这样只能取出特定的一些数据，在增加数据库或者改变数据的情况下就不好用了，不够灵活，我们期望的结果就是通过改变配置，可以以任何形式，不管数据库如何变化，都能有效的显示数据库内容以及自动生成URL

可以参考Django的admin进行自定义配置



### curd页面知识点

#### 单例模式

单例模式，也就是单一的实例模式，每次实例化之后永远都使用的是同一个实例（对象），有三种形式：

1. 模块形式

```python
# 创建一个模块（文件）v1，在里面写类
class NBSite(object):
    def __init__(self):
        self.name = 'nb'
        self.namespace = 'nb'
        self._registry= {}
        
    def register():
      	pass
        
# 然后在模块中实例化
site=NBSite()


# 然后在其他文件不管多少个，只要调用，都使用的是同一个对象
a1 = v1.site.register()
a2 = v1.site.register()
```

2. 类形式，给类添加一个判断属性，然后添加类方法进行实例化，这种方法太麻烦

```python
class Foo:
    _instance = None

    def __init__(self):
        pass

    @classmethod
    def get_instance(cls):
        if cls._instance:
            return cls._instance

        else:
            obj = cls()
            cls._instance = obj
            return obj

if __name__ == '__main__':
    a1 = Foo.get_instance()
    a2 = Foo.get_instance()
```

3. 由于上述方法太过抽象，实例化很麻烦因此将上述方法进行了改造，原理是利用`__new__` 方法比init方法更早执行的原理

```python
class Foo:
    _instance = None

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):   # 当你执行Foo()进行实例化的时候，__new__()是最先执行的
        if cls._instance:
            return cls._instance

        else:
            obj = object.__new__(cls, *args, **kwargs)
            cls._instance = obj
            return obj
          
if __name__ == '__main__':
    obj1 = Foo()
    obj1 = Foo()
```

#### ready

如果我们按照如下格式重写ready方法的话，django会第一步就搜索所有的app中的arya.py文件并执行

```python
class AryaConfig(AppConfig):
    name = 'arya'

    def ready(self):
        from django.utils.module_loading import autodiscover_modules
        autodiscover_modules('arya')
```



#### yield

...

#### model_form 前端循环

model_form 在后端是可以循环的

### pupup

pupup可以实现一些网页之间传输信息的小窗口

url和视图函数

```python
def p1(request):
    return render(request,'p1.html')
  
def p2(request):
    if request.method == "GET":
        return render(request,'p2.html')
    elif request.method == "POST":
        # 在数据库中增加
        from app01 import models
        obj = models.UserGroup.objects.create(title=request.POST.get('city'))
        return render(request,'popup_response.html',{'obj':obj})


urlpatterns = [
    url(r'^p1/', p1),
    url(r'^p2/', p2)
]
```

p1.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
   
</head>
<body>
    <h1>p1页面</h1>
    <select id="i1">
        <option>上海</option>
        <option>北京</option>
    </select>
    <input type="button" value="添加" onclick="popupFunc();" />

    <script>
        function popupFunc() {
            window.open('/p2/','asdfadf',"status=1, height:500, width:600, toolbar=0, resizeable=0")
        }
        
        function xxxxxxxxxx(name) {
            var op = document.createElement('option');
            op.innerHTML = name;
            op.setAttribute('selected','selected');
            document.getElementById('i1').appendChild(op);
        }
    </script>
    
</body>
</html>
```

p2.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
   
</head>
<body>
    <form method="POST">
        {% csrf_token %}
        <input type="text" name="city" />
        <input type="submit" value="提交" />
    </form>
</body>
</html>
```

popup_response.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>正在返回</title>

</head>
<body>
<script>
    (function () {
        var name = "{{ obj.title }}";
        window.opener.xxxxxxxxxx(name);
        window.close();
    })()
</script>
</body>
</html>
```

整个传输过程是这样的

* 首先，进入p1页面，在页面中给input标签绑定了点击事件onclick="popupFunc()，一旦点击，会执行popupFunc函数
* popupFunc函数打开了一个窗口，URL和窗口大小可以自己定义，我们定义给p2，
* 执行p2的URL，然后执行p2的视图函数，函数判断出是get方式请求，返回p2页面
* p2页面显示了一个input框，可以输入内容，然后提交回p2的视图函数
* p2函数判断为post提交，首先将数据存入数据库，然后将表的对象发送给popup_response.html页面
* popup_response.html页面有个自执行函数，一旦页面加载就会执行，window.opener.xxxxxxxxxx(name);语句是将取到的name发送给窗口打开的页面，也就是初始页面的xxxx函数，然后关闭自己的窗口
* 跳转到初始页面，执行xxxx函数

对象通过索引取值

#### 反向生成url，可以通过给URL命名的方式反向生成url

* 首先给需要获得的URL命名

  ```python
  urlpatterns = [
      url(r'^admin/', admin.site.urls),
      url(r'^index/', index),
      url(r'^test/', test, name='xx'),
  ]
  ```

* 然后在视图函数中生成URL

  ```python
  def index(request):
      from django.urls import reverse  # 导入模块
      test_url = reverse('xx')   # 生成URL
      return HttpResponse(test_url)	
  ```

* 在前端使用

  ```html
  <a href="{% url %}"></a>
  ```

  ​

* 如果是正则匹配的URL

  ```python
  urlpatterns = [
      url(r'^admin/', admin.site.urls),
      url(r'^index/', index),
      url(r'^test/(\d+)/test/(\d+)', test, name='xx'),
  ]
  ```

  ```python
  # 生成URL的时候需要传入参数
  def index(request):
      from django.urls import reverse
      test_url = reverse('xx', args=(1, 9))
      return HttpResponse(test_url)
  ```

  ```html
  <!--在前端使用-->
  <a href="{% url 'xx' 1 9 %}"></a>
  ```

  ​

* 如果给正则匹配分组命名

  ```python
  urlpatterns = [
      url(r'^admin/', admin.site.urls),
      url(r'^index/', index),
      url(r'^test/(?P<a1>\d+)/test/(?P<a2>\d+)', test, name='xx'),
  ]

  #  生成URL的时候需要按照名字传参，而且参数改为kwargs
  def index(request):
      from django.urls import reverse
      test_url = reverse('xx', kwargs={'a1': 4, 'a2': 9})
      return HttpResponse(test_url)
    
    
  # 在前端使用
      <a href="{% url 'xx' a1=1 a2=9 %}"></a>
  ```

* 如果出现了name_space，则给这样写

  ```
  test_url = reverse('xx:name_space', kwargs={'a1': 4, 'a2': 9})
  ```

如何判断一个变量是否是函数

* 使用callable

```python
>>> v = 'alskdjf'
>>> callable(v)
False
>>> v = lambda x:x
>>> callable(v)
True
```

* 使用isindtance

```python
>>> from types import FunctionType
>>> a = 'asdf'
>>> isinstance(a,FunctionType)
False
>>> a = lambda x:x
>>> isinstance(a,FunctionType)
True
```

取函数名

```python
>>> def a():
...     pass
... 
>>> a.__name__
'a'
```

反射：

getattr(), setattr()

模板渲染inclusion_tag，他会自动找到index_test.html，然后将index的返回值传给index_test.html然后交给{% index %}

```python
from django.template.library import Library
register = Library()


@register.inclusion_tag('index_test.html')
def index(request):
    return 'result'

  
# 在前端渲染
{% index %}
```

类里面函数和方法的区别

```python
class Func:
    def __init__(self, name):
        self.name = name

    def foo(self):
        print(self.name)

if __name__ == '__main__':
    func = Func('alex')
    Func.foo(func)   # 这是一个函数，必须要self，传一个对象

    func.foo()   #  这是一个方法，它自动传self，不用手动传
```

制作分页：

保留原来的搜索条件

request.GET.urlencode()可以拿到URL的值

如果设置request.GET._mutable=True的话还可以修改URL的值

copy模块

添加页面：

写添加页面的时候注意要将URL的值传过去，

#### 使用类定义生成器

```python
class Foo:
    def __iter__(self):
        yield 1
        yield 2
        yield 3


if __name__ == '__main__':
    obj = Foo()
    for i in obj:
        print(i)
```

既然有iter方法的都是可迭代对象，那么我们就给类定义iter方法，让他变成一个可迭代对象，这样我们在实例化这个类的时候，他会自动执行iter方法，让可迭代对象变成一个迭代器，因此，实例化后的对象就变成了一个迭代器，可以有next方法，也可以使用for循环

### 权限管理

首先进行登录验证，验证成功之后可以显示自己的权限列表

### 套业务