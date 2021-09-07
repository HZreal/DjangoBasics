# 和后台相关


from django.contrib import admin
# Register your models here.

from book.models import BookInfo, PersonInfo
# 注册模型：admin.site.register(模型类)
admin.site.register(BookInfo)
admin.site.register(PersonInfo)