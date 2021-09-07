# 路由相关

# ROOT_URLCONF是进入本项目的入口URL,在setting.py中

"""bookmanager URL Configuration (此文件是本项目的URL)

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    直接引导
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')

Class-based views
    类视图引导
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')

Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include


# 路由列表：浏览器中输入的路径会和路由列表中的每一项进行匹配。匹配成功则引导到相应的模块，匹配失败(遍历路由列表没有取到)则返回404

# Django1.x中：  urlpatterns中元素是url()
# 该url()函数传递了四个参数，两个必需：regex和view，以及两个可选：kwargs，和name。
#                           第一个参数regex是正则(r：转义    ^ 严格开始    $ 严格结束)
#                           第二个参数view是匹配成功的视图函数(内部还会继续匹配)
# 浏览器输入的路由 http://ip:port/path/?key=value&key=value...
# 其中只有path参与正则匹配，正则匹配成功则引导到子应用中继续匹配，成功则返回相应视图，失败则往下一个工程匹配，直到最终匹配不到则返回404
# from django.conf.urls import url
# urlpatterns = [
#     url(r'^admin/', admin.site.urls),
#     url(r'^', include('book.urls')),
# ]

# 现版本2.x以后的re_path相当于1.x的url
# from django.urls import re_path
# urlpatterns = [
# #     re_path(r'^admin/', admin.site.urls),
# #     re_path(r'^', include('book.urls')),
# # ]

# 版本2.x以后，urlpatterns中元素使用新的变量path指定路由，若需要用到正则时用re_path代替以前的url
# path()函数有四个参数，两个必须参数：route 和 view，两个可选参数：kwargs 和 name
#                               第一个参数 route 是一个匹配URL的准则，不会匹配GET和POST参数或域名，用的是非正则表达式可以表示的普通路由路径
#                                               如果路径和转换器语法都不足以定义的URL模式，那么就需要使用正则表达式，这时候就需要使用re_path()
#                               第二个参数 view 是匹配成功调用的视图函数
#                               第三个参数 kwargs 任意个关键字参数可以作为一个字典传递给目标视图函数
#                               第四个参数 namespace 为你的URL取名能使你在 Django 的任意地方唯一地引用它

# 参数在路由中，给视图函数传参，亦即提取url中特定部分：
# 1.x版本采用正则分组传参：  url(r'^articles/(?P<year>[0-9]{4})/$', views.archive), archive函数接收到的year参数作为参数需要对year做类型转换year=int(year)
# 2.x新语法采用path路径转换器Path converter传参：  path('articles/<int:year>/', views.archive), 支持url参数的类型转化。archive函数接收到的year参数作为参数，并且会自动转换year为整型而不是字符串。
# path转换器规则：
#           1.在url里使用尖括号“<>”来捕获，尖括号捕获值的格式<converter:name>。
#           2.其中converter为路径转换器(转换类型或值)，作用就是对拦截到的参数进行转换再传递给视图。name为传递的参数名，如<int:year>。
#             若没有指定转换器类型，默认的转换器是str 那么它会匹配除了斜杠"/"外的所有字符作为捕获的值。
#           3.url不需要以斜杠开头

# path()的另一种以字典的方式给视图函数传参：
# path('index/',views.index,{'user':'lisi','pwd':'234'})        # urls.py
# def index(request, user, pwd):                                # view.py
#     result = 'name={},pwd={}'.format(user,pwd)
#     return HttpResponse(result)

# 以前url()正则分组传参，现用re_path()代替url()，语法相同：
# re_path(r'^index/(?P<id>\d+)/(?P<username>\w+)/$',views.index)      # urls.py
# def index(request,id,username):                                     # view.py
#     result = 'id={},username={}'.format(id,username)
#     return HttpResponse(result)


# include()第一个参数引导的路由
#          第二个参数namespace解决多个路由定义别名重名的问题，习惯写子应用名(不会和其他子应用重名)
# 在include()中指定命名空间而不提供app_name是不被允许的,即设置namespace同时必须设置app_name,且(urls,app_name)构成元祖


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('book.urls', 'book'), namespace='book')),          # 必须指定 app_name
    # path('pay/', include('pay.urls')),
    # path('login/', include('login.urls'))
]



