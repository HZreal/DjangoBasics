# 和当前子应用相关
from django.apps import AppConfig


class BookConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'book'
    # 用于设置该应用直观可读的名字，此名字在Django提供的Admin管理站点中会显示
    verbose_name = 'book子应用：图书管理'

    def ready(self):
        """
        子类可以重写此方法来执行初始化任务。只要注册表被填满就会调用此方法
        比如类似注册信号、定时任务
        """
        print('11111111111111')
        for i in self.get_models():
            print(i)






