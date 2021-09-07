# 和视图相关: 实现业务逻辑


from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from book.models import BookInfo, PersonInfo
from django.urls import reverse


# 视图函数:第一个参数就是HttpRequest的实例对象
#          函数的返回值是HttPResponse的实例对象/子类实例对象
def index(request):
    # reverse()反解析  通过路由别名name动态返回别名指向的路由  参数viewname=name
    # path = reverse(viewname='index')
    path = reverse(viewname='book:index')              # include()里设置了namespace
    # print(path)
    # 跳转页面： 登陆成功或者注册成功跳转到首页
    redirect(path)            # 此路由是指定了别名的路由，通过别名进行跳转。即使原路由名改变，只要别名不变，此跳转逻辑不会变！

    # 根据明确的路由跳转
    # return redirect('/index/')

    # 跳转到百度
    # return redirect('http://www.baidu.com')

    return HttpResponse('index......')



# -------------------------------------HttpResquest请求---------------------------------------------------

# retail_1视图函数接收路由位置参数
def detail_1(request, category_id, book_id):
    print(category_id, book_id)
    return HttpResponse('detail_1视图函数接收路由位置参数----------')


# retail_2视图函数接收路由关键字参数
def detail_2(request, category_id, book_id):
    print(category_id, book_id)
    return HttpResponse('detail_2视图函数接收路由关键字参数----------')


# retail_3视图函数以path转换器接收参数
def detail_3(request, category, year):
    print(type(category), category, type(year), year)
    return HttpResponse('detail_3视图函数以path转换器接收参数----------')


# retail_4视图函数接收GET请求查询字符串参数 http://localhost:8000/11/1145/?username=huang&password=123&username=ge&password=456
# 查询字符串不区分请求方式，即假使客户端进行POST方式的请求，依然可以通过request.GET获取请求中的查询字符串数据。
def detail_4(request):
    query_params = request.GET
    print(query_params)
    # 返回字典 <QueryDict: {'username': ['huang', 'ge'], 'password': ['123', '456']}>  其中value是一个列表，当有多个同名参数时，它们的值放在列表中

    # QueryDict的get()方法获取一键一值，若有多值，则只能获取最后一个。
    # username = query_params['username']
    username = query_params.get('username')
    print(username)                               # 只能得到value列表中最后的元素 'ge'

    # QueryDict的getlist()方法获取一键多值
    password = query_params.getlist('password')
    print(password)                               # 得到value列表所有元素 ['123', '456']

    return HttpResponse('detail_4视图函数接收GET请求查询字符串参数----------')


# detail_5视图函数接收POST请求体数据：form表单
# 请求带有参数时(detail_4,5,6三种均带参)，路由路径最后一定要有'/'   详见BUG-6
# postman中，POST-->输入路由-->Body-->form-data-->输入表单数据key,value
def detail_5(request):
    # Django可以自动解析表单类型的请求体数据，即可用request.POST直接获取表单数据
    body = request.POST                           # 直接返回字典供处理 < QueryDict: {'username': ['huang'], 'password': ['123']} >
    print(body)
    return HttpResponse('detail_5视图函数接收POST请求体数据：form表单-----------')


# detail_6视图函数接收POST请求体数据：json数据
# postman中，POST-->输入路由-->Body-->raw-->JSON-->输入json数据
# 注意json数据字符串必须使用双引号，最后一个元素后没有逗号
import json
# json.dumps()     将字典转换为json字符串
# json.loads()     将json字符串转换为字典
def detail_6(request):
    # 对于非表单类型的请求体数据，Django无法自动解析，故不能用request.POST获取，只能通过request.body获取，且获取的是bytes数据
    # 然后自行根据请求体格式（JSON、XML等）进行解析，如json数据则需要request.body.decode()转为字典
    # data = request.POST                     # 不可取，返回<QueryDict: {}>

    body = request.body                       # 取请求体数据，类型为二进制bytes
    print(body, type(body))

    body_str = body.decode()                  # 对二进制解码，返回数据字符串
    print(body_str, type(body_str))

    data = json.loads(body_str)               # 返回python数据：字典，可取值
    print(data, type(data))

    return  HttpResponse('detail_6视图函数接收POST请求体数据：json数据-----------')


# detail_7视图函数接收请求头header中的数据
# 可以在postman的Headers中发送自定义头部信息，并通过META字典获取
def detail_7(request):
    meta = request.META                            # 返回字典,得到系统的数据
    # 常见的请求头有： CONTENT_LENGTH， CONTENT_TYPE， HTTP_ACCEPT， HTTP_ACCEPT_ENCODING， HTTP_ACCEPT_LANGUAGE， HTTP_HOST ...
    content_type = meta['CONTENT_TYPE']
    print(content_type)

    # 常用HttpRequest对象属性
    print(request.method)                           # 获取请求方式 POST / GET
    print(request.user)                             # 请求的用户对象
    print(request.body)                             # 请求体的内容
    print(request.path)                             # 一个字符串,表示请求的页面的完整路径，不包含域名和参数部分
    print(request.encoding)                         # 一个字符串，表示提交的数据的编码方式。若为None则表示使用浏览器的默认设置，一般为utf-8。此设置可改
    print(request.FILES)                            # 一个类似于字典的对象，包含所有的上传文件
    print(request.get_host())
    print(request.get_port())
    # 更多Ctrl+b详看HttpRequest对象

    return HttpResponse('detail_7视图函数接收请求头header中的数据-------------')


# -----------------------------------HttpResponse响应--------------------------------------

def detail_8(request):
    data = {'name': 'huang'}

    # HttpResponse对象参数：
    # 1.响应体content  接收二进制数据，字符串数据,不要传递对象和字典
    # 2.状态码status  必须是系统指定的100-599
    # 3.响应体数据类型content_type  是MIME类型，语法为：大类/小类
    # 如 text/html  text/css  text/javascript
    # 如 application/json  image/png  image/jpg
    return HttpResponse(content=data, status=200, content_type='text/html')             # data为字典，只显示了name

    # HttpResponse的子类JsonResponse
    # 默认设置content_type='application/json'且默认对content内容进行解析data=json.dumps(data)转成json字符串
    # return JsonResponse(data=data)                   # 全部显示{"name": "huang"}



# 浏览器请求服务器是无状态的,指一次用户请求时，浏览器、服务器无法知道之前这个用户做过什么，每次请求都是一次新的请求
# 原因：浏览器与服务器是使用Socket套接字进行通信的，服务器将请求结果返回给浏览器之后，会关闭当前的Socket连接，而且服务器也会在处理页面完毕之后销毁页面对象
# 有时需要保持下来用户浏览的状态，比如用户是否登录过，浏览过哪些商品等

# 实现状态保持主要有两种方式：
# 1.Cookie  指某些网站为了辨别用户身份、进行session跟踪而储存在用户本地终端上的数据（通常经过加密）
# 服务器可以知道该用户是否是合法用户以及是否需要重新登录等。服务器可以利用Cookies包含信息的任意性来筛选并经常性维护这些信息，以判断在HTTP传输中的状态
# Cookie的特点：
#         Cookie以键值对的格式进行信息的存储，存储大小有限制
#         Cookie基于域名安全，不同域名的Cookie是不能互相访问
#         浏览器请求某网站时，会将浏览器存储的跟网站相关的所有Cookie信息提交给网站服务器

# Cookie流程：
#     ①浏览器第一次请求服务器时，没有携带cookie信息
#     ②服务器接收第一次请求后，发现请求中没有cookie信息
#     ③服务器会设置cookie信息，以响应报文发送给浏览器
#     ④浏览器接收响应，将cookie信息保存
#     ⑤第二次以及之后的浏览器请求该服务器，都会携带cookie信息，服务器看到cookie信息就知道是谁在访问了

# 效果：(通过network请求报文响应报文以及Google浏览器cookie内容可见)

# 从http协议角度深入掌握cookie原理： 通过network查看请求报文响应报文
# 第一次请求，Request Headers没有携带任何cookie信息，但Response Headers有set_cookie信息发送给浏览器
# 第二次以及之后的请求，Request Headers携带了cookie信息，服务器没有再设置cookie信息，那么Response Headers中也没有了cookie

# 面试题：谈一谈cookie  1.概念  2.流程  3.在哪使用  4.你用到比较深刻的地方

# 第一次请求，设置cookie信息
def set_cookie(request):
    # 判断是否有cookie信息

    # 获取用户名
    # username = request.GET.get('username')
    username = request.user

    # 没有cookie信息，服务器通过HttpResponse对象设置
    response = HttpResponse(content='set_cookie..........')
    # max_age设置cookie有效期，从服务器接收请求开始计算.默认没有设置max_age时浏览器关闭则删除cookie信息
    response.set_cookie(key='username', value=username, max_age=3600)

    # 删除cookie，本质是设置max_age=0
    # response.delete_cookie(key)
    # response.set_cookie(key, value, max_age=0)


    # 返回响应，携带cookie信息
    return response


# 第二次及之后的请求，服务器接收查看cookie信息
def get_cookie(request):

    cookies = request.COOKIES             # 返回字典
    username = cookies.get('username')
    return HttpResponse(content=username + '\t' + 'get_cookie...........')



# 2.Session  在服务器端保存的与不同客户端交互时的数据的对象叫做Session
# 服务器为不同的客户端创建了用于保存该用户数据的Session对象。并将用于标识该对象的唯一SessionId发回给与该对象对应的客户端。
# 当浏览器再次发送请求时，SessionId也会被发送过去。服务器凭借这个唯一的SessionId找到与之对应的Session对象
# session需要依赖于cookie， 禁用cookie会导致session无法使用

# 若浏览器删除了sessionid，能获取session信息吗？ 不能
# 换了浏览器能获取到session信息吗？不能，因为换了的浏览器没有对应的cookie信息，请求时没有sessionid服务器无法验证

# session的特点：
#           1. session用于存储一次会话的多次请求的数据，存在服务器端
#           2. session可以存储任意类型，任意大小的数据

# session流程：
#         ①客户端第一次请求时，没有携带cookie信息
#         ②服务器接收请求后，会在服务器端为该用户创建session信息，保存在数据库
#         ③同时会将指向该用户session信息的唯一标识sessionid通过响应头的cookie信息发送给客户端浏览器
#         ④客户端接收后会将cookie信息保存
#         ⑤浏览器第二次以及之后的请求，都会携带含有sessionid的cookie信息发送给服务器
#         ⑥服务器接收请求，通过sessionid匹配服务器保存的session，从而识别身份

# 效果：第一次请求后在浏览器cookie中能够看到sessionid信息，且network中响应报文cookie信息中含有sessionid

# 从http协议角度理解session原理：
# 第一次请求时，Request Headers中没有cookie信息，但是服务器返回的Response Headers中含有set_cookie
# 第二次以及之后的请求，Request Headers中有cookie：sessionid=iiesw4u1mbhx402e5qdvfr5ibtx4e80b

# 第一次请求，设置session信息
def set_session(request):
    # 1.第一次请求cookie无任何信息，返回空字典
    print(request.COOKIES)

    # 2.对用户名密码验证，这里假设验证通过

    # 3.设置session对象信息，保存在数据库，并将
    user_id = '66666'
    request.session['user_id'] = user_id

    # 4.返回响应
    return HttpResponse(content='已设置了session保存在服务器')



# 第二次以及之后的请求，获取sessionid信息
def get_session(request):
    # 1.请求时会在cookie中携带sessionid以及其值，返回字典
    print(request.COOKIES)

    # 2.验证成功获取sessionid信息

    session = request.session            # 返回字典对象
    print(type(session))

    user_id = session['user_id']           # 字典操作
    # user_id = session.get('user_id')
    print(user_id)

    # 获取用户session的随机字符串
    # session_key = session.session_key

    # 检查用户session的随机字符串 在数据库中是否
    # isexist = request.session.exists("session_key")

    # 删除当前用户的所有Session数据
    # request.session.delete("session_key")

    return HttpResponse('get_session..........')


# -----------------------------类视图--------------------------------------
# 不同的逻辑用不同的视图函数，但来自同一路由，只是请求方式不同，用多个视图函数不方便
def show_login(request):                        # GET请求获取注册登录页面
    return HttpResponse('注册登录页面')
def veri_login(request):                        # POST请求验证登录逻辑
    return redirect('首页')

# 一个视图对应的路径提供了多种不同HTTP请求方式的支持时，便在一个函数中编写不同的业务逻辑，如下：
# 通过判断请求方式区分业务逻辑(面向过程)
def login(request):
    if request.method == 'GET':                 # GET请求获取注册登录页面
        return HttpResponse('注册登录页面')
    else:                                       # POST请求验证注册登录逻辑
        return redirect('首页')

# 通过类视图(面向对象)：使用类视图可以将视图对应的不同请求方式以类中的不同方法来区别定义
# 自定义视图类，继承自父类View
# 直接把请求方式的名字作为函数名，在函数体中书写对应逻辑
# 第二个参数必须是请求实例对象request
# 类视图的方法必须有返回值(HttpResponse类或其子类)
from django.views import View
class LoginView(View):               # LoginView继承View，故有父类的as_view()方法

    # 处理GET请求，返回注册页面
    def get(self, request):                      # CSRF防护相关在这里
        # 生成一个随机码
        ms_csrf_token = get_token(request)
        # 把随机码传给模板中的{{ms_csrf_token}}
        context = {
            'ms_csrf_token': ms_csrf_token,

        }
        response = render(request, 'login.html', context)
        # 把随机码以cookie发给客户
        response.set_cookie('ms_csrf_token', ms_csrf_token)
        return response

    # 处理POST请求，返回注册逻辑

    def post(self, request):
        # 获取用户提交的表单数据
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not (username == 'huangzhen' and password == '123456'):
            tag = 0                             # 标识用户名密码不正确
            context = {
                'tag': tag,
                'desc': '<script>alert("请输入用户名和密码")</script>',
            }
            response = render(request, 'login.html', context)
            return response

        user_sms_code = request.POST.get('input_code')                  # 获取用户输入的验证码
        server_sms_code = request.COOKIES.get('ms_csrf_token')        # 获取存在cookie中的随机码，即服务器随机码
        # server_sms_code = request.POST.get('ms_csrf_token')                 # 获取POST请求中csrftoken的值，也是服务器随机码
        if not user_sms_code == server_sms_code:
            tag = 1                           # 标识验证码不正确
            context = {
                'tag': tag,
                'desc': '<script>alert("验证码错误")</script>',
            }
            response = render(request, 'login.html', context)
            return response
            # return redirect(reverse('book:login'))                # 跳转到登录页面

        return HttpResponse(f'用户：{username}' + '\t登陆成功......')


    def put(self,request):            # put请求方式
        return HttpResponse('put请求......')

    # 这里目前没有定义patch、delete等其他请求方式的逻辑函数，若以patch请求，则返回状态码405，状态描述Method Not Allowed


# MRO顺序继承，dispatch重写
from django.contrib.auth.mixins import LoginRequiredMixin
class CenterView(LoginRequiredMixin, View):                 # LoginRequiredMixin 必须在 View 之前
    # view函数返回的dispatch函数在本类CenterView中没有，则会优先去第一个父类LoginRequiredMixin寻找调用，
    # 在执行父类LoginRequiredMixin中的dispatch()时，进行了用户验证，并返回super().dispatch()，故而又调用了View类中的dispatch()
    def get(self, request):
        return HttpResponse('个人中心页面显示......')

    def post(self, request):
        return HttpResponse('个人中心修改......')



# 将session数据保存在redis数据库
class SetSession(View):

    def get(self, request):
        # 增加以及修改
        request.session['name'] = 'huangzhen'
        request.session['id'] = '201503368'
        request.session['age'] = '22'
        request.session['pic'] = 'www.baidu.com/pic/'

        # session信息在redis数据库中以String类型存储，key对应sessionid，value对应设置的session信息(经过编码加密)
        # key = :1:django.contrib.sessions.cached09sxt6bzhzrcnmzpjwyap5wf3w2va70
        # value = \x80\x04\x95O\x00\x00\x00\x00\x00\x00\x00}\x94(\x8c\x04name\x94\x8c\thuangzhen\x94\x8c\x02id\x94\x8c\t201503368\x94\x8c\x03age\x94\x8c\x0222\x94\x8c\x03pic\x94\x8c\x12www.baidu.com/pic/\x94u.

        # session设置过期时间,默认2个星期，参数为秒
        # request.session.set_expiry(300)

        # 在redis库中删除session的部分value信息
        # del request.session['name']
        # 在redis库中删除session中的所有value信息
        # request.session.clear()
        # 刷新内存，一切清空。把整个redis库中session信息连同key全部删除
        # request.session.flush()

        return HttpResponse('设置session信息，存储在redis库中...')


class GetSession(View):

    def get(self, request):

        # 获取数据
        name = request.session.get('name')
        pic = request.session.get('pic')

        return HttpResponse(content=f'获取session信息: name = {name}, pic = {pic}')



# ---------------------------------------模板---------------------------------------
from datetime import date,datetime
class HomeView(View):
    def get(self, request):
        # 获取数据
        username = request.user
        # 组织数据
        context = {
            'username': username,
            'age': 18,
            # 'birthday': date.today(),            # 年月日
            'birthday': datetime.now(),           # 年月日时分
            'friends': ['Tom', 'Jack', 'Rose'],
            'money': {
                '2018': 8888,
                '2019': 9999,
                '2020': 12222,
            },
            'desc': '<script>alert("hot")</script>'

        }

        return render(request, 'index.html', context=context)
        # 查看base.html与detail.html模板的继承关系
        # return render(request, 'base.html')
        # return render(request, 'detail.html')



# 需求：
# 在http:www.aa:8080/index.html里面的js代码发起了http:api:aa:9999/index_data这个地址的请求，
# 结果是：我们是得不到数据的
# 理解：同源策略是浏览器的策略，和服务器没有关系，跨域不是服务器不给数据，也不是浏览器发现了跨域，不进行了请求，而是浏览器根据协议发现不同域传来的数据直接丢弃了
# 解决：可以通过对服务器的响应头配置，让浏览器接收这次数据(后端解决办法)
# 在Django中解决方法：
from django.views.decorators.csrf import csrf_exempt           # scrf_exempt是用来解决视图可以进行跨域请求
# 方法1： 对基于函数的视图，直接装饰
@csrf_exempt
def looog():
    pass

# 方法2： 对类视图，装饰dispatch()
class CrossDomainView(View):
    def get(self,request):
        pass
    def post(self,request):
        pass

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(CrossDomainView, self).dispatch(*args, **kwargs)

# 方法3： 在urls.py中设置
# 见book.urls.py


# ---------------------------------发送axios请求---------------------------
# Axios是用于前端页码局部刷新，返回json数据给前端，不要返回页面给前端(整体刷新)
class AxiosView(View):
    def get(self,request):
        return render(request, 'axios.html')

    def post(self,request):
        pass

class ReceiveAxiosView(View):
    def get(self,request):
        # 接收get请求查询字符串参数
        data = request.GET
        username = data.get('username')
        password = data.get('password')
        info = {'username': username, 'password': password}

        #TODO 接收二进制数据，用JsonResponse对象返回自动解码为json数据
        return JsonResponse(info)                  # Axios是用于前端页码局部刷新，返回json数据给前端调用
        # return HttpResponse(f'username: {username} password: {password}')               # 不要返回页面给前端(整体刷新)

# ！！！查看效果需要打开network查看响应response，前端有接收json数据(不显示在页面)

    def post(self,request):
        # 接收post请求请求体body数据
        binary_body = request.body                     # 二进制数据

        #TODO body内容为二进制数据，需要json解码
        body_str = binary_body.decode()
        data = json.loads(body_str)

        name = data.get('name')
        age = data.get('age')
        info = {'name': name, 'age': age}
        return JsonResponse(info)
















































