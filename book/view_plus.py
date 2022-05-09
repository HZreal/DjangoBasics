from io import BytesIO
from django.contrib.sessions.backends.db import SessionStore
from django.core.files.uploadedfile import UploadedFile
from django.core.handlers.wsgi import WSGIRequest
from django.http import QueryDict
from django.utils.datastructures import MultiValueDict
from django.views import View


# 对于Web框架来说，它负责把environ中的wsgi.input中内容进行解析，因为wsgi.input这个对象中含有客户端发送过来的HTTP请求报文，解析了请求报文就可以拿到客户端传递的参数信息已经文件等。然后把这些有用的参数都保存在request对象的实例属性中。
# 对于Web服务器来说，它负责把接受客户端的连接，然后把客户端发送的http报文封装到envion的wsgi.input字段中，然后把这个environ和一个回调函数start_response传入到web框架的入口application中，然后调用application(environ, start_response)返回一个response对象，最后再把取出response对象中的数据，构造成HTTP响应报文发送到客户端。



# GET，POST， COOKIES， FILES这几个是非数据属性描述符
# 在request被实例化出来的时候并不是request的实例属性，而是在request.GET/POST/COOKIES/FILES时才去实际把这些请求参数或者cookie或者上传的文件,从wsgi.input中读取出来封装成QueryDict和MultiValueDict类型的实例对象，
# 同时会把这些QueryDict和MultiValueDict对象保存在request的实例属性中，下次再调用request.GET/POST/COOKIES/FILES时就直接从request.__dict__中取出即可

# 本质上是一种懒加载机制+缓存的机制，只有当用到的时候才去真正执行取参数的操作，然后再把取得参数结果保存在request对象的实例属性中

class LearnWSGIRequest_View(View):

    def get(self, request: WSGIRequest):
        """WSGIRequest properties"""

        cookies = request.COOKIES()
        session: SessionStore = request.session                               # <SessionStore object>
        meta = request.META                                                       # dict
        # META常用属性
        # - CONTENT_LENGTH: 请求的正文的长度(是一个字符串)
        # - CONTENT_TYPE: 请求的正文的MIME类型
        # - HTTP_ACCEPT: 响应课结束后肚饿Context - Type
        # - HTTP_ACCEPT_LANGUAGE: 响应可接收的语言
        # - HTTP_ACCEPT_ENCODING: 响应可接收的编码
        # - HTTP_HOST: 客户端发送的HOST值
        # - HTTP_REFETRT: 在访问这个页面上一个页面的url
        # - QUERY_STRING: 单个字符串形式的查询字符串(未解析过的形式)
        # - REMOTE_ADDR: 客户端的IP地址, 如果服务器做反向代理或者负载均衡, 那么返回值是127.0.0.1, 这时使用HTTP_X_FORWARDFD_FOR来获取


        server_host = request.get_host()                        # '192.168.200.229:8804'
        full_path = request.get_full_path()                     # '/wsgirequest/properties'
        full_path_info = request.get_full_path_info()           # '/wsgirequest/properties'
        raw_uri = request.get_raw_uri()                         # 'http://192.168.200.229:8804/wsgirequest/properties'

        is_ajax_request = request.is_ajax()                     # False
        is_https_protocol = request.is_secure()                 # False


    def post(self, request: WSGIRequest):
        """post_data/FILES 解析"""

        body = request.body

        # request.POST第一次调用时返回_load_post_and_files，去解析数据、文件等，并分别写入实例属性_post，_files，在内存缓存，后续调用直接取实例属性
        post_data: QueryDict = request.POST
        data = post_data.get('data')


        # request.FILES第一次调用时返回_load_post_and_files，解析数据、文件等，并分别写入_post，_files，在内存缓存，后续调用直接取实例属性
        files: MultiValueDict = request.FILES
        file = files.get('file')            # TemporaryUploadedFile or InMemoryUploadedFile (concrete subclass of UploadedFile) 对应的处理器分别是 TemporaryFileUploadHandler and MemoryFileUploadHandler
        _file = file.file
        with open('', 'wb') as f:
            for chunk in file.chunks():
                f.write(chunk)



        data = BytesIO(self._body)
        _data, _file = request.parse_file_upload(request.META, post_data=data)











