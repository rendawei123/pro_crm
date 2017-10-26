### curd插件使用方法

1. 将项目拷贝到项目中
2. 注册app生成数据库
3. 在app中创建arya.py文件，
4. 在arya中注册model

```python
from arya.service.sites import site
from . import models

site.register(models.UserInfo)
```

4. 在URL中写匹配关系

```python
from django.conf.urls import url
from app01 import views
from arya.service.sites import site

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^arya/', site.urls),
    url(r'^index/', views.index),
]
```

5. 如果想该模板渲染，则在最外面的templete里面也创建文件夹，命名为arya，然后里面的模板也命名为layout进行修改

6. 访问

7. 自定义显示哪几列内容

   ```python
   class UserInfoConfig(sites.AryaConfig):  
     # 显示name,username,email字段并且加上checkbook框
       list_display = ['name', 'username', 'email']

   sites.site.register(models.UserInfo, UserInfoConfig)
   ```

8. 扩展（查看个人信息）直接自定义URL和视图函数进行修改

   首先定义URL

   ```python
   url(r'^user_info/(\d+)', views.user_info),
   ```

   然后定义视图函数

   ```python
   def user_info(request, pk):
       obj = models.UserInfo.objects.filter(pk=pk)[0]
       return render(request, 'user_info.html', {'obj': obj})
   ```

   最后模板渲染

   ```html
   <body>
       {{ obj.id }}
       {{ obj.email }}
   </body>
   ```

9. 扩展（查看个人信息）使用我门前面预定好的扩展URL进行扩展

   ```python
   from . import models
   from django.shortcuts import render, HttpResponse


   class UserInfoConfig(sites.AryaConfig):
       list_display = ['name', 'username', 'email']

       def detail_view(self, request, pk):
           obj = self.model_class.objects.filter(pk=pk)[0]
           return render(request, 'user_info.html', {'obj': obj})

       def extra_urls(self):
           from django.conf.urls import url
           app_model_name = self.model_class._meta.app_label, self.model_class._meta.model_name
           urlpatterns = [
               url(r'^(.+)/detail/$', self.wrapper(self.detail_view), name="%s_%s_delete" % app_model_name),
           ]
           return urlpatterns

   sites.site.register(models.UserInfo, UserInfoConfig)
   ```

   然后就可以按照修改的URL进行访问

10. 重写添加页面，如果不想要以前添加的逻辑，就需要重写添加页面

    ```python
    class UserInfoConfig(sites.AryaConfig):
        list_display = ['name', 'username', 'email']

        def add_view(self, request, *args, **kwargs):
            return HttpResponse(...)
    ```

    ​