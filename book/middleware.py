# 中间件：是一个轻量级、底层的插件系统
# 可以介入Django的请求和响应处理过程，修改Django的输入或输出。中间件的设计为开发者提供了一种无侵入式的开发方式
# 每次请求前和响应后的时候都会调用

# 请求前的执行顺序是按照注册顺序从上到下，请求后的执行顺序是按照注册倒序从下到上

# 中间件定义： 在类视图外面再套一个函数
def simple_middleware(get_response):

    # 此处编写的代码仅在Django第一次配置和初始化的时候执行一次
    # print('init...')

    # 视图函数
    def middleware(request):

        # 此处编写的代码会在每个请求处理视图前被调用，
        # Code to be executed for each reuquest before,the view (and later middleware) are called
        print('begin1111111111')
        # username = request.COOKIES.get('username')
        # if username is None:
        #     print('username is None...')
        # else:
        #     print('username is exist...')

        # 此时会去执行请求对应的视图函数
        response = get_response(request)

        # 此处编写的代码会在每个请求处理视图之后被调用
        # Code to be executed for each reuquest/response after, the view is called
        print('end11111111111')

        return response

    return middleware


def simple_middleware2(get_response):

    def middleware(request):

        print('begin222222222222')

        response = get_response(request)

        print('end222222222222')

        return response

    return middleware

























































