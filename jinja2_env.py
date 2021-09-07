# 此文件名记得不要取jinja2.py ！！！否则系统模块jinja2.py无法使用

from django.templatetags.static import static
from django.urls import reverse

from jinja2 import Environment

# date过滤器
from django.template.defaultfilters import date

def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': static,
        'url': reverse,
        'date':date,                   # date需要导入Django模板里的date过滤器
    })
    return env