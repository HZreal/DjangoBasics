# 和模型相关,内嵌了ORM
# ORM框架就是把数据库表的行与相应的对象建立关联,互相转换.使得数据库的操作面向对象
# ORM操作数据库需要驱动程序，而驱动程序就是mysqldb
# ORM框架与数据库对应关系：
#                        类<------>表
#                      属性<------>字段
#                      实例<------>数据行记录


# objects是Manager类型的对象，objects = models.Manage().定义在from django.db import models中，可以自定义。在数据库中则为一个QuerySet类型的对象
# objects是django实现的mvc框架中的数据层，是Model和数据库进行查询的接口.
# 可以有多个过滤条件(构造，过滤，切片等)作为参数传递，这些行为都不会对数据库进行操作。只要你查询的时候才真正的操作数据库
# queryset是数据库对象集，就是传到服务器上的url里面的内容。是查询结果集的缓存区，这里是为了提高查询效率
# 在你创建一个QuerySet对象的时候，Django并不会立即向数据库发出查询命令，只有在你需要用到这个QuerySet的时候才回去数据库查询
# 可以有多个过滤条件(构造，过滤，切片等作为参数传递)，相当于SQL的where条件，这些行为都不会对数据库进行操作。只要你查询的时候才真正的操作数据库


from django.db import models


# 1.定义模型类(继承自models.Model)
class BookInfo(models.Model):
    # 主键：系统会自动生成AutoField类型的id
    # 属性：按数据库对应字段的数据类型写:  属性名 = models.属性类型(选项约束条件)
    # 属性名不要使用关键字，不要使用双下划线__(条件查询数据库参数都是双下划线)，数据库默认创建与属性名同名的字段，但是外键字段名默认额外添加_id
    # 属性类型和mysql对应
    # 选项约束：CharField必须设置max_length,
    #           null=True表示允许为空, unique=True表示唯一不可重复,
    #           default设置默认值, verbose_name设置admin后台站点显示的名称,  choices设置可选选项,
    #           db_index=True表示为此字段创建索引, db_column指定在数据库该字段名称，不指定默认和变量同名,但是Django对于外键字段会默认在变量名后加_id
    #           related_name = ''自定义主表中对从表的关联字段(默认是主表名小写_set)
    name = models.CharField(max_length=10, unique=True, verbose_name='书籍名')
    pub_date = models.DateField(null=True, verbose_name='发表日期')
    read_count = models.IntegerField(default=0, verbose_name='阅读量')
    comment_count = models.IntegerField(default=0, verbose_name='评论量')
    is_delete = models.BooleanField(default=False, verbose_name='逻辑删除')

    # TODO 系统生成的隐藏属性：主表中对从表的关联字段，通过这个属性可以获取从表对象
    # personinfo_set
    # personinfo__name    personinfo__description__contains 等等

    def __str__(self):      # 默认显示BookInfo对象，此函数使之显示为当前对象对应的指定名
        return self.name

    # 原生类：定义元数据(不是字段的数据) -- 比如排序选项, admin 选项等等
    # app_label这个选项只在一种情况下使用，就是你的模型类不在默认的应用程序包下的models.py文件中，这时候你需要指定你这个模型类是那个应用程序
    # db_table是用于指定自定义数据库表名的，模型类在数据库中生成的表名默认是  应用名.类名(book.BookInfo)
    # ordering 告诉Django模型对象返回的记录结果集是按照哪个字段排序的
    # verbose_name就是给你的模型类起一个更可读的名字
    class Meta:
        db_table = 'bookinfo'        # 修改表名
        verbose_name = '书籍信息'


class PersonInfo(models.Model):
    # choices选项,枚举类型
    GENDER_CHOICES = (
        (0, 'male'),
        (1, 'female')
    )
    name = models.CharField(max_length=20, verbose_name='姓名', unique=True)
    gender = models.SmallIntegerField(choices=GENDER_CHOICES, default=0, verbose_name='性别')
    # 外键
    # 参数on_delete：指明主表删除数据时，外键引用表的数据该如何处理
    # on_delete=CASCADE表示级联：删除主表数据时连通一起删除外键表中数据
    # on_delete=PROTECT表示保护：通过抛出ProtectedError异常，来阻止删除主表中被外键应用的数据
    # on_delete=SET_NULL表示设置对应记录的外键字段为NULL：仅在该外键字段null = True允许为null时可用
    book_id = models.ForeignKey(BookInfo, on_delete=models.CASCADE, verbose_name='书籍id', db_column='book_id')
    # TODO PersonInfo实例对象.book_id  返回的是一个主表的书籍对象！！为什么不是外键字段值?
    description = models.CharField(max_length=200, null=True, verbose_name='描述')
    is_delete = models.BooleanField(default=False, verbose_name='逻辑删除')


    class Meta:
        db_table = 'personinfo'
        verbose_name = '人物信息'

    def __str__(self):
        return self.name

# 2.模型迁移
# 2.1 先生成迁移文件 (创建数据库和模型的对应关系，此时并未在数据库中生成表)
# python manage.py makemigrations

# 2.2 再迁移 (在数据库中生成表)
# python manage.py migrate



# 3.操作数据库












