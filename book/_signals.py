# django 信号量
# Django 中内置一个 信号调度器，它可以帮助应用程序在框架中的其他地方发生某些固定操作时能够得到通知。简而言之：信号允许某些发送器通知一组接收器某些操作已经发生。当接受器接受到这一通知时可以做响应的处理


# 内置的信号集
from django.db.models import signals
from django.db.models.signals import pre_init, post_init, pre_save, post_save, pre_delete, post_delete, pre_migrate, post_migrate
from django.core.signals import request_finished, request_started, got_request_exception


def my_callback(sender, **kwargs):
    """
    该函数接受一个 sneder 参数以及关键字参数（**kwargs），所有信号处理程序都必须接受这些参数
    """
    print('hello world')


# 使用 Signal.connect()方法注册一个接收器函数，当发送信号时调用接收器。信号的所有接收器函数都会按照注册时的顺序一个接一个调用
        # receiver：将连接到此信号的回调函数
        # sender：指定要从其接收信号的特定发送方
        # weak：Django默认将信号处理程序存储为弱引用，因此如果你的接收器函数时本地函数，则可能会对其进行垃圾回收。如果想避免这种情况发生可以当你要调用connct()方法时传入weak = False
        # disptch_uid：在可能发送重复信号的情况下，信号接收器的唯一标识
pre_save.connect(receiver=my_callback, sender=None, weak=True, dispatch_uid=None)



# 连接接受函数
# Django 提供两种方法可以将接收器连接到信号:

# 方式一：
post_save.connet(my_callback)
request_finished.connect(my_callback)

# 方式二：
# receiver(sigal)
# 参数 signal：一个用于连接函数的信号包含多个信号列表
# 接受函数和连接接受函数放在 在一起
from django.dispatch import receiver
from book.models import BookInfo
@receiver(post_save, sender=BookInfo)
def my_callback(sender, instance, **kwargs):
  print('hello world')

# 以上两种方式都能到达 my_callback 函数在每次请求完成时被调用






# django 信号量实际使用:
# 1.监听某个模型中某个字段的变化
# 假设我们有一个 User 模型，当我们用户名发生改变时需要重置 token，这时我们只需要监听 User 中 token 是否变化，如果变化则重置 token，使用信号来实现这一需求


# 用户模型
from django.db import models
class User(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=32, verbose_name='用户名')
    areaCode = models.CharField(max_length=10, blank=True, verbose_name='手机区号')
    phone = models.CharField(max_length=20, verbose_name='用户手机号', blank=True)
    email = models.EmailField(max_length=50, verbose_name='用户邮箱', blank=True)
    avatar = models.CharField(max_length=255, verbose_name='用户头像')
    token = models.CharField(max_length=50, verbose_name='token')


@receiver(post_init, sender=User)
def init_signal(sender, instance, **kwargs):
    # 在模型初始化时将 name 赋值给 __origin_name
    instance.__origin_name = instance.name


@receiver(post_save, sender=User)
def save_signal(sender, instance, **kwargs):

    # 当模型被保存时查看此时的 name 和 __origin_name 是否相等，如果不相等则重置 token
    if instance.__origin_name and instance.__origin_name != instance.name:
        # 重置 token
        pass