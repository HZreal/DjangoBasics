# 和视图相关： 实现业务逻辑
# Create your views here.

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from book.models import BookInfo, PersonInfo


# 视图函数就是python函数：
#           函数的第一个参数就是请求request(HttpRequest的实例对象)
#           函数的返回值是HttpResponse的实例对象/子类实例对象
def index(request):
    # 1.先查询数据库所有书籍select * from bookinfo 此查询由ORM操作
    # object是Manager类型的对象，objects = Modes.Manage()   返回的是实例对象，Queryset类型
    books = BookInfo.objects.all()

    # 2.组织数据
    name = 'Siri '
    # context 将字典内容传递给模板，模板通过模板语言使用
    context = {
        'name': name,
        'books': books,
    }

    # 3.将组织的数据传递给模板
    # render()有三个参数：
    #               1.当前请求对象request  2.模板文件名template_name  3.传递参数context,是一个字典,传递给模板
    # 系统自动根据模板文件名寻找模板文件
    # render()函数内部本身就有返回值return HttpResponse(request，name, context)
    # return render(request, 'index.html',context=context)

    # 返回响应体内容
    return HttpResponse('index')


'''
Django的manage工具提供了shell命令，类似于ipython,帮助我们配置好当前工程的运行环境(如连接好数据库等),
使我们方便在终端测试查看内容
执行语句 python manage.py shell进入shell模式， 然后执行python语句获取结果
'''

# 模型类里定义了objects，如BookInfo里隐藏着objects = BookInfoManager()
# 调用objects实际就是 初始化BookInfoManager对象，内含各种操作方法，如save()


# 新增数据
# 方式一：
# 1.初始化类，返回生成的对象
book1 = BookInfo(name='PyLearn', pub_date='2020-5-5')
# 2.需要手动调用save()方法入库
book1.save()

# 方式二：
# 利用管理类objects(对模型的增删改查),也有返回值，但内部封装了save方法，直接入库
BookInfo.objects.create(name='Django', pub_date='2019-8-24')

# 修改数据
# 方式一：
# 1.先查询数据 select * from bookinfo where id = 1
book2 = BookInfo.objects.get(id=1)
# 2.修改数据
book2.read_count = 20
# 3.调用save()方法存储到库
book2.save()

# 方式二：直接修改入库
# filter()过滤，相当于where条件
BookInfo.objects.filter(id=1).update(read_count=100, comment_count=200)

# 删除数据
# 方式一：
# 1.先查询获取
book3 = BookInfo.objects.get(id=6)
# 2.再删除
book3.delete()
# book.save() 删除操作不需要调用save

# 方式二：直接删除
BookInfo.objects.filter(id=6).delete()

# 查询数据(大多都是查询数据)
# 一、基本查询：
# get()获取单一对象
try:
    book4 = BookInfo.objects.get(id=1)
# except Exception as e:
#     pass
except BookInfo.DoesNotExist:
    pass

# all()获取对象集，返回的是一个列表，是一个Queryset对象
book5 = BookInfo.objects.all()

# count()获取数据条数
BookInfo.objects.all().count()
BookInfo.objects.count()

# 二、条件查询
# 语法：  filter(字段名__运算符=值)
# filter()筛选过滤，返回符合条件的结果，返回的是一个列表
BookInfo.objects.filter(id__exact=1)  # exact精确的，就是等于
# 等同于BookInfo.objects.filter(id=1)
BookInfo.objects.filter(name__contains='湖')  # contains 表示名字包含'湖'
BookInfo.objects.filter(name__endswith='部')  # endswith 表示名字以'部'结尾
BookInfo.objects.filter(name__isnull=True)  # isnull 表示名字为空
BookInfo.objects.filter(id__in=[1, 3, 5])  # in 表示id为1或3或5
BookInfo.objects.filter(id__gt=3)  # gt即greater than 表示id大于3
BookInfo.objects.filter(id__gte=3)  # gte即greater than equal 表示id大于等于3
BookInfo.objects.filter(id__lt=3)  # lt即less than 表示id小于3
BookInfo.objects.filter(id__lte=3)  # lte 表示id小于等于3
BookInfo.objects.filter(pub_date__year='1980')  # __year 表示发表日期是1980年的，date类型中还有__day __month
BookInfo.objects.filter(pub_date__gt='1980-1-1')  # 表示发表日期是1980年一月一号以后的，格式必须是YY-MM-DD

# get() 返回的是一个单一对象
BookInfo.objects.get(id__exact=1)
# 等同于BookInfo.objects.get(id=1)

# exclude()排除符合条件的数据，返回不符合条件的结果，相当于filter的取反
BookInfo.objects.exclude(id__exact=3)
# 等同于BookInfo.objects.exclude(id=3)

# values(*fields)
# 返回一个ValuesQuerySet —— QuerySet 的一个子类，迭代时返回字典而不是模型实例对象
# values 接收可选的位置参数*fields，它指定SELECT 应该限制哪些字段。如果指定字段，每个字典将只包含指定的字段的键/值。如果没有指定字段，每个字典将包含数据库表中所有字段的键和值。
# ValuesQuerySet 用于你知道你只需要字段的一小部分，而不需要用到模型实例对象的函数。只选择用到的字段当然更高效
BookInfo.objects.values('pub_date', 'read_count').order_by('pub_date')
# values_list(*fields, flat=False)
# 与values() 类似，只是在迭代时返回的是元组而不是字典。每个元组包含传递给values_list() 调用的字段的值 —— 所以第一个元素为第一个字段
BookInfo.objects.values_list('id').order_by('id')

# 三、一个表中两个字段比较的查询，用F对象
# 语法形式：  filter(字段名__运算符=F('字段名'))
from django.db.models import F

BookInfo.objects.filter(read_count__gt=F('comment_count'))  # 表示阅读量大于评论量
BookInfo.objects.filter(read_count__gt=F('comment_count') * 2)  # 表示阅读量大于2倍评论量

# 四、一个表中多个条件的查询  用Q对象
# 需求： id>2且阅读量>40
# 方式一：
BookInfo.objects.filter(id__gt=2).filter(read_count__gt=40)
BookInfo.objects.filter(id__gt=2, read_count__gt=40)

# 方式二：用Q对象
# 语法形式：  Q(字段名__运算符=值)
#    逻辑或   Q()|Q() ...
#    逻辑与   Q()&Q() ...
#    逻辑非  ~Q()
from django.db.models import Q

BookInfo.objects.filter(Q(id__gt=2) | Q(read_count__gt=40))
BookInfo.objects.filter(Q(id__gt=2) & Q(read_count__gt=40))
BookInfo.objects.filter(~Q(id=2))

# 五、聚合函数   Sum, Max, Min, Avg, Count
# 语法形式：  aggragte(Xxx('字段'))                  # aggragte意思是聚集汇总
from django.db.models import Sum, Avg, Max, Min, Count

BookInfo.objects.aggregate(Sum('read_count'))  # 返回字典{'read_count__sum': 214}

# 六、排序(开发使用较多)
BookInfo.objects.all().order_by('read_count')  # 升序
BookInfo.objects.all().order_by('-read_count')  # 降序

# 七、基本关联查询(两个表联表查询)--------------------
# 思维总结：此方法先获取条件表，再通过条件表的属性获取查询表。而条件表的属性对于主表而言是'从表名小写__set'，对于从表而言是'外键名'
# 书籍(主表)和人物(从表)关系是 1：n    人物表中有关于书表的字段即外键
# 1.已知条件主表关联查询从表    如通过书籍查询人物
# 语法形式：  主表模型(实例).关联模型类名小写_set
# 需求：查询书籍id为1的人物信息
# PersonInfo.objects.filter(book_id=1)    # 以前查询
# ①.先查询书籍
book6 = BookInfo.objects.get(id=1)
# ②.再根据书籍关联查询人物信息
person1 = book6.personinfo_set  # 返回人物对象集
person1.all()

# 2.已知条件从表关联查询主表    如通过人物查询书籍
# 语法形式：  从表模型(实例).外键
# 需求：查询人物id为1的书籍信息
# ①.先查询人物
person2 = PersonInfo.objects.get(id=1)
# ②.再根据人物关联查询书籍信息
book7 = person2.book_id  # 返回书籍对象
book7.name

# 关联查询的筛选--------------------
# ！！！思维总结：此方法直接返回查询表对象，以条件表属性作为参数。其中条件表属性(语法是由查询表指向的)对于主表(此时是从表指向)是'外键名__主表字段'，对于从表(此时是主表指向)是'从表名小写__从表字段'！！！
# 1.已知条件从表关联查询主表信息
# 语法形式：  filter(关联模型类名小写__字段__运算符=值)
# 如查询人物为郭靖的书籍，查询描述信息有'八'的书籍
BookInfo.objects.filter(personinfo__name__exact='郭靖')
BookInfo.objects.filter(personinfo__description__contains='八')

# 2.已知条件主表关联查询从表信息
# 语法形式：  filter(外键__字段__运算符=值)
# 如查询书名为天龙八部的所有人物，查询图书阅读量大于50的所有人物
PersonInfo.objects.filter(book_id__name__exact='天龙八部')
PersonInfo.objects.filter(book_id__read_count__gt=50)

# 八、查询结果集Queryset--------表示从数据库中获取的对象集合
# 以下方法均返回查询集
# all()：返回所有数据。
# filter()：返回满足条件的数据。
# exclude()：返回满足条件之外的数据。
# order_by()：对结果进行排序
# 查询集特点：
# 1.惰性执行：创建查询集不会访问数据库，直到调用数据时，才会访问数据库
books = BookInfo.objects.all()  # 此时没有查询数据库
for book in books:  # 此时用到books才会去查询数据库
    print(book)

# 2.缓存：使用同一个查询集，第一次使用时会发生数据库的查询，然后Django会把结果缓存下来，再次使用这个查询集时会使用缓存的数据，减少了数据库的查询次数
# 这样写没有缓存
list = [book.id for book in BookInfo.objects.all()]
# 再次执行依然会再次查询数据库
list = [book.id for book in BookInfo.objects.all()]

# 这样写会缓存
books = BookInfo.objects.all()  # books变量保存在内存中
[book.id for book in books]
# 再次执行时不会去数据库中查询，因为已缓存到内存，从实时日志可见
[book.id for book in books]
[book.id for book in books]

# 限制查询集----------------------比如列举正在热播显示前六个电视剧
# 可以对查询集进行取下标或切片操作，等同于sql中的limit和offset子句
BookInfo.objects.all()[0]
BookInfo.objects.all()[0:2]

# 九、分页
from django.core.paginator import Paginator

# Paginator是一个类。参数object_list指结果集, per_page指每页的记录条数
books = BookInfo.objects.all()  # 6条数据
p = Paginator(object_list=books, per_page=2)  # 每页2条
# 获取第几页的数据
books_page1 = p.page(1)  # 返回一个列表，即一页
books_page1[0]  # 第1页第1条数据
books_page1[1]  # 第1页第2条数据
