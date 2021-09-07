# 此文件名记得不要取jinja2.py ！！！否则系统模块jinja2.py无法使用

# 导入Django模板里的date过滤器
from django.template.defaultfilters import date
# 导入jinja2的环境类
from jinja2 import Environment

def environment(**options):

    # 1.创建Environment实例
    env = Environment(**options)      # 参数必不可少

    # 2.设置jinja2的函数指向Django模板的指定过滤器
    env.globals.update({
        'date': date,            # date需要导入Django模板里的date过滤器

    })

    # 将自定义的过滤器添加到环境中
    # env.filters['do_listreverse'] = do_listreverse

    # 3.返回对象
    return env


# 自定义过滤器：
def do_listreverse(li):
    if li == 'B':
        return 'haha'

















