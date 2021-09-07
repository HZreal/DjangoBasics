# 和当前子应用相关


from django.apps import AppConfig


class BookConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'book'
    # 用于设置该应用直观可读的名字，此名字在Django提供的Admin管理站点中会显示
    verbose_name = 'book子应用：图书管理'