from book import views

# 早期版本下用url
# from django.conf.urls import url
# urlpatterns = [
#     # url('^index/$', index)
# ]
# 现版本的re_path相当于1.x的url
# from django.urls import re_path
# urlpatterns = [
    # url('^index/$', index)
# ]

from django.urls import path, re_path
from django.views.decorators.csrf import csrf_exempt      # scrf_exempt是用来解决视图可以进行跨域请求

# django默认配置有一个设置：APPEND_SLASH 即针对浏览器输入请求的地址URL末尾是否自动添加斜杠
# APPEND_SLASH=True表示自动添加(默认)，APPEND_SLASH=False则不会自动添加斜杠
# 浏览器输入请求的地址末尾不带斜杠时，根据django默认的配置，会进行判断：尝试添加斜杠时，会不会访问到资源，如果加了斜杠能访问到资源的话，就会重定向到加了斜杠的地址。
# 但如果加了斜杠都无法访问到资源的话，就不会进行重定向的操作

urlpatterns = [
    # name就是给url起别名，这个别名name指向这个路由，哪怕修改了此路由,依然可以通过别名name找到此路由
    # 为你的URL取名能使你在 Django 的任意地方唯一地引用它，尤其是在模板中。这个有用的特性允许你只改一个文件就能全局地修改某个URL模式。
    path('home/', views.index, name='index'),

    # 以正则分组的方式 将url中需要的部分 按顺序位置传参给视图函数views.detail_1
    re_path(r'^(1)/(100)/$', views.detail_1),
    # re_path(r'^(\d+)/(\d+)/$', views.detail_1),

    # 以正则分组的方式指定分组名 将url中需要的部分 按关键字传参给视图函数views.detail_2  可以避免位置传参的顺序混乱错误
    re_path(r'^(?P<category_id>\d+)/(?P<book_id>\d+)/$', views.detail_2),

    # 以path转换器传参(参数名需和视图函数参数名一致)
    path('<str:category>/<int:year>/', views.detail_3),

    # 指向 views.detail_4 5 6 7 8
    re_path(r'^\d+/\d+/$', views.detail_8),

    # 第一次请求，设置cookie
    path('set_cookie/', views.set_cookie),
    # 第二次及之后的请求，获取cookie
    path('get_cookie/', views.get_cookie),

    # 第一次请求，设置session
    # path('set_session/', views.set_session),
    # 第二次及之后的请求，获取cookie
    # path('get_session/', views.get_session),

    # 类视图的url引导：
    # 第二个参数：类名.as_view()  返回的是一个函数名view，而函数view()的返回是一个函数dispatch
    # 当发送请求的时候就触发了函数view的执行view()
    # view执行到最后会调用dispatch，函数dispatch将此次的请求方式与请求列表进行匹配，匹配成功则执行类视图中对应的请求函数，若未匹配成功则返回状态码405(详情看源码)
    path('login/', views.LoginView.as_view(), name='login'),
    # re_path(r'^login/$', views.LoginView.as_view()),

    path('center/', views.CenterView.as_view()),

    # 模板
    path('index/', views.HomeView.as_view()),

    # 将session信息保存在redis库中
    path('set_session/', views.SetSession.as_view()),
    path('get_session/', views.GetSession.as_view()),

    # csrf_exempt 解决跨域请求的方法3
    path('crossdomain/', csrf_exempt(views.CrossDomainView.as_view())),

    # axios请求
    path('axios/', views.AxiosView.as_view()),

    # axios请求接收
    path('recv_axios/', views.ReceiveAxiosView.as_view())
]














