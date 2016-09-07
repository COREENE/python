#python 学习笔记6之 Web开发 异步IO

#概况介绍
﻿'''TCP 三次握手连接 点对点 无大小限制 可靠
UDP 无连接 可广播发送 有大小限制 不可靠

socket “套接字”  由一个IP地址和一个端口号确定  
应用层与TCP/IP协议通信的中间软件抽象层 是一组接口（门面模式）
ClientSocket ServerSocket
套接字连接过程：服务端监听——客户端请求——连接确认

HTTP协议 建立在TCP协议之上 短连接
HTTP使用“请求（方法，url，协议版本，相关mime样式）——响应
 （消息的协议版本，一个成功和失败码，相关mime样式）”方式
HTTP/1.0为每一次HTTP的请求/响应建立一条新的TCP链接，因此一个
       包含HTML内容和图片的页面将需要建立多次的短期的TCP链接
HTTP/1.1提出了可持续链接的实现方法


结论：HTTP是应用层协议，其传输都是被包装成TCP协议传输。可以用SOCKET实现
HTTP。SOCKET是实现传输层协议的一种编程API，可以是TCP，也可以是UDP。'''




#HTTP协议简介：
'''1.浏览器发给服务器请求：
方法：GET仅请求资源，POST会附带用户数据；
路径：/full/url/path；
域名：由Host头指定：Host: www.sina.com.cn
以及其他相关的Header；
如果是POST，那么请求还包括一个Body，包含用户数据。'''
GET / HTTP/1.1
#GET表示一个读取请求，/表示首页，HTTP/1.1指示采用的HTTP协议版本是1.1
Host: www.sina.com.cn
#表示请求的域名是www.sina.com.cn

'''2.服务器返回的原始响应数据：
响应代码：200表示成功，3xx表示重定向，4xx表示客户端发送的请求有错误，
5xx表示服务器端处理时发生了错误；
响应类型：由Content-Type指定；
以及其他相关的Header；
通常服务器的HTTP响应会携带内容，也就是有一个Body，包含响应的内容，
网页的HTML源码就在Body中。'''
HTTP/1.1 200 OK
#200表示一个成功的响应，后面的OK是说明
Content-Type: text/html
#Content-Type指示响应的内容

'''3.如果浏览器还需要继续向服务器请求其他资源，比如图片，
就再次发出HTTP请求，重复步骤1、2'''



#HTTP格式 
#一个HTTP包含Header和Body两部分，其中Body是可选的。
#HTTP GET请求的格式：(换行符是\r\n)
GET /path HTTP/1.1
Header1: Value1
Header2: Value2
Header3: Value3
#HTTP POST请求的格式：
POST /path HTTP/1.1
Header1: Value1
Header2: Value2
Header3: Value3

body data goes here... #body通过\r\n\r\n来分隔
#HTTP响应的格式：
200 OK
Header1: Value1
Header2: Value2
Header3: Value3

body data goes here...




#HTML
#CSS是Cascading Style Sheets（层叠样式表）控制页面元素样式
#JavaScript是为了让HTML具有交互性而作为脚本语言添加的




# WSGI接口
def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    return [b'<h1>Hello, web!</h1>']
''''environ：一个包含所有HTTP请求信息的dict对象；
start_response：发送HTTP响应的Header。只能调用一次,因为Header只能发送一次，
start_response()函数接收两个参数，一个是HTTP响应码，一个是一组
list表示的HTTP Header。每个Header用一个包含两个str的tuple表示。
然后，函数的返回值b'<h1>Hello, web!</h1>'将作为HTTP响应的Body发送给浏览器'''



#运行WSGI服务
1.# hello.py  实现Web应用程序的WSGI处理函数：
def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])   #HTTP响应的Header
    body = '<h1>Hello, %s!</h1>' % (environ['PATH_INFO'][1:] or 'web') 
    #HTTP响应的Body
    return [body.encode('utf-8')]  

2.# server.py  启动WSGI服务器，加载application()函数：
# 从wsgiref模块导入:
from wsgiref.simple_server import make_server
# 导入我们自己编写的application函数:
from hello import application
# 创建一个服务器，IP地址为空，端口是8000，处理函数是application:
httpd = make_server('', 8000, application)
print('Serving HTTP on port 8000...')
# 开始监听HTTP请求:
httpd.serve_forever()

#hello.py没有import任何包，说明这个文件改起来测试起来容易。
#serve包含的都是引入服务器的一些固定代码，调通一次就没必要改动了





#使用Web框架
#Flask
from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return '<h1>Home</h1>'

@app.route('/signin', methods=['GET'])
def signin_form():
    return '''<form action="/signin" method="post">
              <p><input name="username"></p>
              <p><input name="password" type="password"></p>
              <p><button type="submit">Sign In</button></p>
              </form>'''

@app.route('/signin', methods=['POST'])

def signin():
    # 需要从request对象读取表单内容：
    if request.form['username']=='admin' and request.form['password']=='password':
        return '<h3>Hello, admin!</h3>'
    return '<h3>Bad username or password.</h3>'

#运行python app.py，Flask自带的Server在端口5000上监听:
if __name__ == '__main__':
    app.run()

'''常见的Python Web框架：
Django：全能型Web框架；
web.py：一个小巧的Web框架；
Bottle：和Flask类似的Web框架；
Tornado：Facebook的开源异步Web框架。'''




#使用模板
#MVC：Model-View-Controller，“模型-视图-控制器”
#V就是VIEW层，负责展示HTML，C是控制层，负责调度url，M是model层


#jinja2
'''在Jinja2模板中，用{{ name }}表示一个需要替换的变量,用{% ... %}表示指令'''
{% for i in page_list %}
    <a href="/page/{{ i }}">{{ i }}</a>
{% endfor %}

'''常用模板：
Mako：用<% ... %>和${xxx}的一个模板；
Cheetah：也是用<% ... %>和${xxx}的一个模板；
Django：Django是一站式框架，内置一个用{% ... %}和{{ xxx }}的模板。'''












# 异步IO
'''多线程和异步，是处理大并发的两种不同的方式。多线程的处理方式一般是这样：
一个主线程，负责监听，一旦请求来了，就起一个线程，处理完，就将这个线程回收。
而异步是在同一个线程里，轮番接受请求，再交给业务逻辑去处理，“多路复用”'''
'''阻塞和非阻塞是等待方式的区别.阻塞是同步的，异步一定是非阻塞的'''



#协程 Coroutine
#Python对协程的支持是通过generator实现的
'''Python中的协程三个阶段
1.最初的生成器变形yield/send
2.引入@asyncio.coroutine和yield from
3.在最近的Python3.5版本中引入async/await关键字'''

def consumer():  #是一个generator
    r = ''
    while True:
        print('r---->%s' % r) #启动后执行到这里，遇见yield暂停
        n = yield r  #接受到n后执行
        if not n:
            print('a')
            return
        print('[CONSUMER] Consuming %s...' % n)
        r = '200 OK'
def produce(c):
    c.send(None) #等价于next(c),启动生成器
    n = 0
    while n < 2:
        n = n + 1
        print('[PRODUCER] Producing %s...' % n)
        r = c.send(n) #将n发送给c,作为当前中断的yield表达式的返回值
        print('[PRODUCER] Consumer return: %s' % r)
    c.close()
c = consumer()
produce(c)
#结果：
r---->
[PRODUCER] Producing 1...
[CONSUMER] Consuming 1...
r---->200 OK
[PRODUCER] Consumer return: 200 OK
[PRODUCER] Producing 2...
[CONSUMER] Consuming ...
r---->200 OK
[PRODUCER] Consumer return: 200 OK

'''yield表达式本身没有返回值，它的返回值需要等到下次调用generator函数时，
由send(args)函数的参数赋予。
n1 = yield r是两个操作:
1是执行yield r，执行完后没有返回值，但是把r作为generator函数的执行结果返回。
2是下次send(n)调用generator函数时首先给n1赋值。'''

'''c.send(n)将n发送给c，作为c中当前中断的yield表达式的返回值'''


#asyncio 库
import asyncio
@asyncio.coroutine
def sleep3s():
    print('begin sleep 3s')
    yield from asyncio.sleep(3.0)
    print('end sleep 3s')
@asyncio.coroutine   
def sleep5s():
    print('begin sleep 5s')
    yield from asyncio.sleep(5.0)
    print('end sleep 5s')
loop=asyncio.get_event_loop()
tasks = [sleep3s(), sleep5s()] #多个coroutine封装成一组Task然后并发执行
loop.run_until_complete(asyncio.wait(tasks))
loop.close()
#执行结果：
begin sleep 3s
begin sleep 5s
(暂停3s)
end sleep 3s
(暂停2s)
end sleep 5s

'''yield from用于重构生成器,还可以像一个管道一样将send信息传递给内层协程，
并且处理好了各种异常情况'''

'''利用@asyncio.coroutine修饰以后，这个函数可以支持await或者 yield from语法,一旦
执行yield from 语法以后，asyncio将会挂起当前的coroutine，去执行其他的coroutine'''

'''asyncio 库：event loop
asyncio库一个重要的概念就是事件循环,只有启动事件循环以后，才可以让coroutine任务
得以继续执行，如果event loop停止或者暂停，那么整个异步io也停止或者暂停'''

'''当开始运行event loop以后：
1.开始执行sleep3s
2.当程序开始进入睡眠以后，event loop不会停止当前线程，而是挂起当前函数，执行
下一个coroutine,即sleep5s
3.sleep5s开始进入睡眠，挂起当前的函数
4.event loop检测到sleep 3s时间已经到了,于是重新执行被挂起的sleep3s,sleep3s执行完毕
5.sleep5s时间已经到了,于是重新执行被挂起的sleep5s,sleep5s执行完毕'''


#async/await
'''只需要做两步简单的替换：
1.把@asyncio.coroutine替换为async；2.把yield from替换为await'''

@asyncio.coroutine
def hello():
    print("Hello world!")
    r = yield from asyncio.sleep(1)
    print("Hello again!")
#重新编写：
async def hello():
    print("Hello world!")
    r = await asyncio.sleep(1)
    print("Hello again!")
 

#aiohttp
import asyncio
from aiohttp import web

async def index(request):
    await asyncio.sleep(0.5) #模拟耗时操作
    return web.Response(body=b'<h1>Index</h1>')

async def hello(request):
    await asyncio.sleep(0.5):
    text='<h1>hello,%s</h>'%request.match_info['name']
    return web.Response(body=text.encode('utf-8'))

async def init(loop): #初始化函数init()也是一个coroutine
    app=web.Application(loop=loop)
    app.router.add_route('GET','/',index)
    app.router.add_route('GET','/hello/{name}',hello)
    srv=await loop.creat_server(app.make_handler(),'127.0.0.1',8000)
    #loop.creat_server()利用asyncio创建TCP服务。
    print('Server staarted at http://127.0.0.1:8000...')
    return srv

loop=asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()















































