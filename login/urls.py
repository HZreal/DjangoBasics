from django.urls import path, include

from login import views



extra1_urls = [
    path()
]

extra2_urls = [
    path()
]


urlpatterns = [
    path('login/', views.login),

    # 一个子app中有url前缀相同时，也可以分组
    # path('group2', include('login.groupUrls')),
    # path('group1', include(extra1_urls)),
    # path('group2', include(extra2_urls)),

    # path第三个参数向视图传递参数
    # path('pass_extra_params_to_view/<int: id>', views.UrlParamsToView.as_view(), {'params': 'hello'}),
    # 向include中传递参数
    # path('pass_extra_params_to_include/<int: id>', include('login.groupUrls'), {'params': 'hello'}),

]



