#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Coreene Wong'

import asyncio, os, logging
import functools # 高阶函数模块, 提供常用的高阶函数, 如wraps
# python中的自省模块，类似完成Java一样的反射功能。具有类型判断、获取元信息等功能，具体建议查看下方提供的官方文档
# https://docs.python.org/3/library/inspect.html
import inspect 

from urllib import parse # 从urllib导入解析模块

from aiohttp import web

from apis import APIError #APIS: application programe interfaces程序应用接口

# 定义装饰器@get
# 将一个函数映射为一个URL处理函数
def get(path):
	'''
	装饰函数，函数经次函数装饰后即带上了__method__、__route__属性
	Define decorator @get('/path)
	'''
	def decorator(func):
		@functools.wraps(func)
		def wrapper(*args, **kw):
			return func(*args, **kw)
		# 通过装饰器加上__method__属性,用于表示http method
		wrapper.__method__ = 'GET'
		# 通过装饰器加上__route__属性,用于表示path
		wrapper.__route__ = path
		return wrapper
	return decorator

def post(path):
	'''
    Define decorator @post('/path')
    '''
	def decorator(func):
		@functools.wraps(func)
		def wrapper(*args, **kw):
			return func(*args, **kw)
		wrapper.__method__ = 'POST'
		wrapper.__route__ = path
		return wrapper
	return decorator

# ---------------------------- 使用inspect模块中的signature方法来获取函数的参数，实现一些复用功能--
# 关于inspect.Parameter 的 kind 类型有5种：
# POSITIONAL_ONLY        只能是位置参数
# POSITIONAL_OR_KEYWORD  可以是位置参数也可以是关键字参数
# VAR_POSITIONAL         相当于是 *args
# KEYWORD_ONLY           命名关键字参数，相当于是 *,key
# VAR_KEYWORD            相当于是 **kw

# def foo(a, *, b:int, **kwargs)...; signature(foo)==(a, *, b:int, **kwargs)
# signature(foo).parameters==OrderedDict([('a', <Parameter "a">), ('b', <Parameter "b:int">), ('kwargs', <Parameter "**kwargs">)])

def get_required_kw_args(fn):
    # 如果url处理函数需要传入关键字参数，且默认是空得话，获取这个key
    args = []
    params = inspect.signature(fn).parameters
    for name, param, in params.items():
        # param.default == inspect.Parameter.empty这一句表示参数的默认值要为空
        if param.kind == inspect.Parameter.KEYWORD_ONLY and param.default == inspect.Parameter.empty:
            args.append(name)
    return tuple(args)

def get_all_kw_args(fn):
    # 如果url处理函数需要传入关键字参数，获取这个key
    args = []
    params = inspect.signature(fn).parameters
    for name, param, in params.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY:
            args.append(name)
    return tuple(args)

def has_kw_args(fn):
    # 判断是否有关键字参数
    params = inspect.signature(fn).parameters
    for name, param in params.items():
        if param.kind == inspect.Parameter.KEYWORD_ONLY:
            return True

def has_var_kw_arg(fn):
    # 判断是否有关键字变长参数，VAR_KEYWORD对应**kw
    params = inspect.signature(fn).parameters
    for name, param in params.items():
        if param.kind == inspect.Parameter.VAR_KEYWORD:
            return True

def has_request_arg(fn):
    # 函数fn是否有'request'参数,并且该参数要在其他普通的位置参数之后
    sig = inspect.signature(fn)
    params = sig.parameters
    found = False
    for name, param in params.items():
        if name == "request": # 找到名为"request"的参数,置found为真
            found = True
            continue
        # 该参数要在其他普通的位置参数之后。如果判断为True，则表明param只能是位置参数POSITIONAL_ONLY
        if found and (param.kind != inspect.Parameter.VAR_POSITIONAL and param.kind != inspect.Parameter.KEYWORD_ONLY and param.kind != inspect.Parameter.VAR_KEYWORD):
            raise ValueError("request parameter must be the last named parameter in function: %s%s" % (fn.__name__, str(sig)))
    return found

# 定义RequestHandler类,封装url处理函数。
# 是适配器，它把用户自定义参数的各种奇形怪状handler适配成了标准的 handler(request)调用
# RequestHandler目的是从URL处理函数（如handlers.index）中分析其需要接收的参数，从web.request对象中获取必要的参数
# 调用url参数,然后把结果转换为web.Response对象，这样，就完全符合aiohttp框架的要求：
class RequestHandler(object):
# RequestHandler是一个类，由于定义了__call__()方法，因此可以将其实例视为函数。
    def __init__(self, app, fn):
        self._app = app
        self._func = fn 
        self._has_request_arg = has_request_arg(fn)
        self._has_var_kw_arg = has_var_kw_arg(fn)
        self._has_kw_args = has_kw_args(fn)
        self._all_kw_args = get_all_kw_args(fn)
        self._required_kw_args = get_required_kw_args(fn)

    @asyncio.coroutine
    def __get_request_content(self, request):
        request_content = None 
        # 确保有参数
        if self._has_var_kw_arg or self._has_kw_args or self._required_kw_args:
            
            # ------阶段1：POST/GET方法下正确解析request的参数，包括位置参数和关键字参数------
            #
            # http method 为 post的处理
            if request.method == "POST":
                # 判断是否村存在Content-Type（媒体格式类型）:text/html; charset:utf-8; ...;
                if not request.content_type:
                    return web.HTTPBadRequest("Missing Content-Type")
                ct = request.content_type.lower() 
                # 以下为检查post请求的content type字段
                # application/json表示消息主体是序列化后的json字符串
                if ct.startswith("application/json"):
                    params = yield from request.json() # request.json方法的作用是读取request body, 并以json格式解码
                    if not isinstance(params, dict): # 解码得到的参数不是字典类型, 返回提示信息
                        return web.HTTPBadRequest("JSON body must be object.")
                    request_content = params 
                # 以下2种content type都表示消息主体是表单
                elif ct.startswith("application/x-www-form-urlencoded") or ct.startswith("multipart/form-data"): 
                    # request.post方法从request body读取POST参数,即表单信息,并包装成字典赋给request_content变量
                    params = yield from request.post()  # 调用post方法，注意此处已经使用了装饰器
                    request_content = dict(**params)
                else:
                    return web.HTTPBadRequest("Unsupported Content-Type: %s" % request.content_type)

            # http method 为 get的处理
            if request.method == "GET":
                # request.query_string表示url中?后面的键值对内容
                # 比如"https://www.google.com/#newwindow=1?q=google",其中q=google就是query_string
                qs = request.query_string  
                if qs:
                    request_content = dict() 
                    # 解析query_string,以字典的形式保存到request_content
                    for k, v in parse.parse_qs(qs, True).items():
                        request_content[k] = v[0]
        return request_content

    # __call__方法的代码逻辑:
    # 1.定义kw=request_content对象，用于保存参数
    # 2.判断URL处理函数是否存在参数，如果存在则根据是POST还是GET方法将request请求内容保存到kw
    # 3.如果kw为空(说明request没有请求内容)，则将match_info列表里面的资源映射表赋值给kw；如果不为空则把命名关键字参数的内容给kw
    # 4.完善_has_request_arg和_required_kw_args属性
    @asyncio.coroutine
    def __call__(self, request):
        request_content = yield from self.__get_request_content(request)
        # pdb.set_trace()
        if request_content is None:  # 参数为空说明没有从Request对象中获取到必要参数
            '''
            def hello(request):
                    text = '<h1>hello, %s!</h1>' % request.match_info['name']
                    return web.Response() 
            app.router.add_route('GET', '/hello/{name}', hello)
            '''
            '''if not self._has_var_kw_arg and not self._has_kw_arg and not self._required_kw_args:
                # 当URL处理函数没有参数时，将request.match_info设为空，防止调用出错
                request_content = dict()
            '''        
            request_content = dict(**request.match_info) 
            # request.match_info是一个dict 主要是保存像@get('/blog/{id}')里面的id，就是路由路径里的参数
            # 此时request_content指向match_info属性，一个变量标识符的名字的dict列表。Request中获取的命名关键字参数必须要在这个dict当中
            # request_content 不为空,且requesthandler只存在命名关键字的,则只取命名关键字参数名放入request_content
        else:
            # 如果从Request对象中获取到参数了
            # 当没有可变参数，有命名关键字参数时候，request_content指向命名关键字参数的内容
            if not self._has_var_kw_arg and self._all_kw_args: # not的优先级比and的优先级要高
                # remove all unamed request_content, 从request_content中删除URL处理函数中所有不需要的参数
                copy = dict()
                for name in self._all_kw_args:
                    if name in request_content:
                        copy[name] = request_content[name]
                request_content = copy
            # check named arg: 检查关键字参数的名字是否和match_info中的重复
            for k, v in request.match_info.items():
                if k in request_content:
                    logging.warning("Duplicate arg name in named arg and request_content args: %s" % k)                
                request_content[k] = v  # 用math_info的值覆盖request_content中的原值

        if self._has_request_arg: #且参数名未在request_content中,返回丢失参数信息
        # 如果有request这个参数，则把request对象加入request_content['request']    
            request_content["request"] = request
        
        if self._required_kw_args:
        # check required request_content,检查是否有必需关键字参数   
            for name in self._required_kw_args:
                if not name in request_content:
                    return web.HTTPBadRequest("Missing argument: %s" % name)

        # ---------------------------以上代码均是为了获取调用参数----------------------
        logging.info("call with args: %s" % str(request_content))
        
        # 以下调用handler处理,并返回response.
        try:
            r = yield from self._func(**request_content) 
            return r
        except APIError as e:
            return dict(error = e.error, data = e.data, message = e.message)

# 添加CSS等静态文件所在路径
def add_static(app):
    # os.path.abspath(__file__), 返回当前脚本的绝对路径(包括文件名)
    # os.path.dirname(), 去掉文件名,返回目录路径
    # os.path.join(), 将分离的各部分组合成一个路径名
    # 因此以下操作就是将本文件同目录下的static目录(即www/static/)加入到应用的路由管理器中
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
    app.router.add_static("/static/", path)
    logging.info("add static %s => %s" % ("/static/", path))

# URL处理函数, 将处理函数注册到app上 (添加路由)
def add_route(app, fn):
    method = getattr(fn, "__method__", None) # 获取fn.__method__属性,若不存在将返回None
    path = getattr(fn, "__route__", None) 
    # 由于我们定义的处理方法，被@get或@post修饰过，所以方法里会有'__method__'和'__route__'属性
    # http method 或 path 路径未知,将无法进行处理,因此报错 
    if path is None or method is None:
        raise ValueError("@get or @post not defined in %s." % str(fn))
    # 将非协程或生成器的函数变为一个协程.
    if not asyncio.iscoroutinefunction(fn) and not inspect.isgeneratorfunction(fn):
        fn = asyncio.coroutine(fn)
    logging.info("add route %s %s => %s(%s)" % (method, path, fn.__name__, '. '.join(inspect.signature(fn).parameters.keys())))
    # eg-INFO:root:add route GET / => index(request)
    # 正式注册为相应的url处理方法
    # 处理方法为RequestHandler的自省函数 '__call__'
    app.router.add_route(method, path, RequestHandler(app, fn))

# 自动注册所有请求处理函数（添加一个模块的所有路由）
def add_routes(app, module_name):
    # module_name格式 'hhh.handlers'/'handlers'
    # Python rfind() 返回字符串最后一次出现的位置，如果没有匹配项则返回-1
    n = module_name.rfind(".") 
    if n == (-1): # module_name = handlers
        # __import__ 作用同import语句，但__import__是一个函数，并且只接收字符串作为参数, 
        # 其实import语句就是调用这个函数进行导入工作的, 其返回值是对应导入模块的引用
        # __import__('os',globals(),locals(),['path','pip']) ,等价于from os import path, pip'''
        mod = __import__(module_name, globals(), locals())
    else: #eg: module_name = hhh.handlers
        name = module_name[n+1:] # name = handlers
        # 先用__import__表达式导入模块以及子模块 from hhh import handlers
        # 再通过getattr()方法获得 handlers
        mod = getattr(__import__(module_name[:n], globals(), locals(), [name]), name) # getattr(x, 'y') is equivalent to x.y
    # 遍历模块目录
    for attr in dir(mod):
        # dir(mod)返回模块定义的名称列表（函数、类和变量）,这里主要是找处理方法
        # 由于我们定义的处理方法，被@get或@post修饰过，所以方法里会有'__method__'和'__route__'属性
        if attr.startswith("_"): # 忽略以_开头的属性与方法(是私有/特殊)
            continue
        fn = getattr(mod, attr) # 排除私有属性后，就把属性提取出来
        if callable(fn): # 取能调用的，说明是方法 
            method = getattr(fn, "__method__", None)
            path = getattr(fn, "__route__",None)
            if method and path: 
                # 如果都有，说明是我们定义的处理方法 eg:fn = index(request),交给add_route去处理
                add_route(app, fn) 



















