#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Coreene Wong'

'''
async web application.
'''

# 设置日志等级,默认为WARNING.只有指定级别或更高级的才会被追踪记录
import logging; logging.basicConfig(level=logging.INFO) # 输出到logfile文件

import asyncio, os, json, time
from datetime import datetime

from aiohttp import web  

from jinja2 import Environment, FileSystemLoader ## 从jinja2模板库导入环境与文件系统加载器

from config import configs

import orm
from coroweb import add_routes, add_static

from handlers import cookie2user, COOKIE_NAME

# 选择jinja2作为模板, 初始化模板; janja2相当于MVC的V
def init_jinja2(app, **kw):
    logging.info("init jinja2...")
    # 初始化模板配置，包括模板运行代码的开始结束标识符，变量的开始结束标识符等
    options = dict(
        # 是否转义设置为True，就是在渲染模板时自动把变量中的<>&等字符转换为&lt;&gt;&amp;        
        autoescape = kw.get("autoescape", True),     # 自动转义xml/html的特殊字符
        block_start_string = kw.get("block_start_string", "{%"), # 代码块开始标志
        block_end_string = kw.get("block_end_string", "%}"),     # 代码块结束标志
        variable_start_string = kw.get("variable_start_string", "{{"), # 变量开始标志
        variable_end_string = kw.get("variable_end_string", "}}"),     # 变量结束标志
        # Jinja2会在使用Template时检查模板文件的状态，如果模板有修改， 则重新加载模板。如果对性能要求较高，可以将此值设为False
        auto_reload = kw.get("auto_reload", True) # 每当对模板发起请求,加载器首先检查模板是否发生改变.若是,则重载模板
        )
    # 从参数中获取path字段，即模板文件的位置
    path = kw.get("path", None) 
    if path is None:
        # 若路径不存在,则默认为当前文件目录下的 templates 目录
        # os.path.abspath(__file__), 返回当前脚本的绝对路径(包括文件名)
        # os.path.dirname(), 去掉文件名,返回目录路径
        # os.path.join(), 将分离的各部分组合成一个路径名
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
    logging.info("set jinja2 template path: %s" % path)
    # Environment是Jinja2中的一个核心类，它的实例用来保存配置、全局对象，以及从本地文件系统或其它位置加载模板。
    # 这里把要加载的模板和配置传给Environment，生成Environment实例
    # 加载器负责从指定位置加载模板, 此处选择FileSystemLoader,顾名思义就是从文件系统加载模板,前面我们已经设置了path
    env = Environment(loader = FileSystemLoader(path), **options)
    # 从参数取filter字段
    # filters: 一个字典描述的filters过滤器集合, 如果非模板被加载的时候, 可以安全的添加filters或移除较早的.
    filters = kw.get("filters", None)
    # 如果有传入的过滤器设置，则设置为env的过滤器集合
    if filters is not None:
        for name, f in filters.items():
            env.filters[name] = f
    # 给webapp设置模板
    app["__templating__"] = env


# ------------------------------------------拦截器middlewares设置-------------------------
# 创建应用时,通过指定命名关键字为一些"middle factory"的列表可创建中间件Middleware
# 每个middle factory接收2个参数,一个app实例,一个handler, 并返回一个新的handler
# 以下是一些middleware(中间件), 可以在url处理函数处理前后对url进行处理

# 在处理请求之前,先记录日志
@asyncio.coroutine
def logger_factory(app, handler): #这就是个装饰器
    @asyncio.coroutine
    def logger(request):
        # 记录日志,包括http method, 和path.    eg: INFO:root:Request: GET /
        logging.info("Request: %s %s" % (request.method, request.path))
        # 日志记录完毕之后, 调用传入的handler继续处理请求
        return (yield from handler(request))
    return logger

# 是为了验证当前的这个请求用户是否在登录状态下，或是否是伪造的sha1
@asyncio.coroutine
def auth_factory(app, handler):
    @asyncio.coroutine
    def auth(request):
        logging.info('check user: %s %s' % (request.method, request.path))
        request.__user__ = None
        # 获取到cookie字符串
        cookie_str = request.cookies.get(COOKIE_NAME)
        if cookie_str:
            # 通过反向解析字符串和与数据库对比获取出user
            user = yield from cookie2user(cookie_str)
            if user:
                logging.info('set current user: %s' % user.email)
                # user存在则绑定到request上，说明当前用户是合法的
                request.__user__ = user
        if request.path.startswith('/manage/') and (request.__user__ is None or not request.__user__.admin):
            return web.HTTPFound('/signin')
        # 执行下一步
        return (yield from handler(request))
    return auth

# 解析数据
@asyncio.coroutine
def data_factory(app, handler):
    @asyncio.coroutine
    def parse_data(request):
        # 解析数据是针对post方法传来的数据,若http method非post,将跳过,直接调用handler处理请求
        if request.method == "POST":
            # content_type字段表示post的消息主体的类型, 以application/json打头表示消息主体为json
            # request.json方法,读取消息主题,并以utf-8解码
            # 将消息主体存入请求的__data__属性
            if request.content_type.startswith("application/json"):
                request.__data__ = yield from request.json()
                logging.info("request json: %s" % str(request.__data__))
            # content type字段以application/x-www-form-urlencodeed打头的,是浏览器表单
            # request.post方法读取post来的消息主体,即表单信息
            elif request.content_type.startswith("application/x-www-form-urlencoded"):
                request.__data__ = yield from request.post()
                logging.info("request form: %s" % str(request.__data__))
        # 调用传入的handler继续处理请求
        return (yield from handler(request))
    return parse_data

# 上面2个middle factory是在url处理函数之前先对请求进行了处理,以下则在url处理函数之后进行处理
# 其将request handler的返回值转换为web.Response对象
@asyncio.coroutine
def response_factory(app, handler):
    @asyncio.coroutine
    def response(request):
        logging.info("Response handler...")
        # 调用相应的handler处理request
        r = yield from handler(request)
        # 如果响应结果为web.StreamResponse类，则直接把它作为响应返回
        if isinstance(r, web.StreamResponse):
            return r
        # 如果响应结果为字节流，则把字节流塞到response的body里，设置响应类型为流类型，返回
        if isinstance(r, bytes):
            resp = web.Response(body=r)
            resp.content_type = "application/octet-stream"
            return resp
        # 若响应结果为字符串
        if isinstance(r, str):
            # 先判断是不是需要重定向，是的话直接用重定向的地址重定向
            if r.startswith("redirect:"):
                return web.HTTPFound(r[9:])
            # 不是重定向的话，把字符串当做是html代码来处理
            resp = web.Response(body = r.encode("utf-8"))
            resp.content_type = "text/html;charset=utf-8"
            return resp
        # 如果响应结果为字典
        if isinstance(r, dict):
            # 如果响应结果为字典
            template = r.get("__template__") 
            # 如果没有，说明要返回json字符串，则把字典转换为json返回，对应的response类型设为json类型
            if template is None:
                resp = web.Response(body=json.dumps(r, ensure_ascii=False, default=lambda o: o.__dict__).encode("utf-8"))
                resp.content_type = "application/json;charset=utf-8"
                return resp
            else:
                # user在进入index()函数前就通过middleware绑定到request对象了
                r['__user__'] = request.__user__
                # 如果有'__template__'为key的值，则说明要套用jinja2的模板，'__template__'Key对应的为模板网页所在位置
                resp = web.Response(body=app["__templating__"].get_template(template).render(**r).encode("utf-8"))
                resp.content_type = "text/html;charset=utf-8"
                # 以html的形式返回
                return resp
        # # 如果响应结果为int
        # 此时r为状态码,即404,500等
        if isinstance(r, int) and r >=100 and r<600:
            return web.Response
        # 若响应结果为元组,并且长度为2
        if isinstance(r, tuple) and len(r) == 2:
            t, m = r
            # t为http状态码,m为错误描述
            if isinstance(t, int) and t>= 100 and t < 600:
                # 返回状态码与错误描述
                return web.Response(t, str(m))
        # default: 默认直接以字符串输出
        resp = web.Response(body=str(r).encode("utf-8"))
        resp.content_type = "text/plain;charset=utf-8"
        return resp
    return response

# 响应处理
# 总结下来一个请求在服务端收到后的方法调用顺序是:
#       logger_factory->response_factory->RequestHandler().__call__->get或post->handler
# 那么结果处理的情况就是:
#       由handler构造出要返回的具体对象
#       然后在这个返回的对象上加上'__method__'和'__route__'属性，以标识别这个对象并使接下来的程序容易处理
#       RequestHandler目的就是从URL函数中分析其需要接收的参数，从request中获取必要的参数，调用URL函数,然后把结果返回给response_factory
#       response_factory在拿到经过处理后的对象，经过一系列对象类型和格式的判断，构造出正确web.Response对象，以正确的方式返回给客户端
# 在这个过程中，我们只用关心我们的handler的处理就好了，其他的都走统一的通道，如果需要差异化处理，就在通道中选择适合的地方添加处理代码。


# 时间过滤器
def datetime_filter(t):
    # 定义时间差
    delta = int(time.time()-t)
    # 针对时间分类
    if delta < 60:
        return u"1分钟前"
    if delta < 3600:
        return u"%s分钟前" % (delta // 60)
    if delta < 86400:
        return u"%s小时前" % (delta // 3600)
    if delta < 604800:
        return u"%s天前" % (delta // 86400)
    dt = datetime.fromtimestamp(t)
    return u"%s年%s月%s日" % (dt.year, dt.month, dt.day)

#初始化协程
@asyncio.coroutine
def init(loop):
    # 创建连接池, db参数传配置文件里的配置db
    yield from orm.create_pool(loop = loop, **configs.db)
    # 创建web应用  循环类型是消息循环
    app = web.Application(loop=loop, middlewares=[logger_factory, auth_factory, response_factory]) 
    # middlewares(中间件)设置3个中间处理函数(都是装饰器)
    # middlewares中的每个factory接受两个参数，app 和 handler(即middlewares中的下一个handler)
    # 譬如这里logger_factory的handler参数其实就是auth_factory
    # middlewares的最后一个元素的handler会通过routes查找到相应的，其实就是routes注册的对应handler
    # 这其实是装饰模式的典型体现，logger_factory, auth_factory, response_factory都是URL处理函数前（如handler.index）的装饰功能
    # 设置模板为jiaja2，并以时间为过滤器
    init_jinja2(app, filters = dict(datetime = datetime_filter))
    # 添加请求的handlers，即各请求相对应的处理函数
    add_routes(app, 'handlers') 
    # 添加静态文件所在地址
    add_static(app)
    # 调用子协程：创建一个TCP服务器，绑定到"127.0.0.1:9000"socket,并返回一个服务器对象
    srv = yield from  loop.create_server(app.make_handler(), '127.0.0.1', 9000)
    '''app.make_hander()中对middleware的处理: (装饰器原理)
    for factory in reversed(self._middlewares):
        handler = yield from factory(app, handler)
    resp = yield from handler(request)

    middleware的代码示意：m1( m2( m3( doFoo())))
    middleware调用流程：
        req -> m1 -> m2 -> m3 -> doFoo()- 一路return 原路返回
        <- m1 <- m2 <- m2 <- resq - <-'''
    logging.info('server started at http://127.0.0.1:9000...')
    return srv

# 入口，固定写法
# 获取eventloop然后加入运行事件
loop = asyncio.get_event_loop()    
loop.run_until_complete(init(loop)) 
loop.run_forever() 