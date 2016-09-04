#python 学习笔记6之 Web开发 异步IO

#HTTP请求：
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
    start_response('200 OK', [('Content-Type', 'text/html')])
    return [b'<h1>Hello, web!</h1>']

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

if __name__ == '__main__':
    app.run()

'''常见的Python Web框架：
Django：全能型Web框架；
web.py：一个小巧的Web框架；
Bottle：和Flask类似的Web框架；
Tornado：Facebook的开源异步Web框架。'''



#使用模板
#MVC：Model-View-Controller，“模型-视图-控制器”


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













 

















































