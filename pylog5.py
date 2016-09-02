#python 学习笔记5之网络编程，电子邮件

#TCP编程 建立可靠连接，并且通信双方都可以以流的形式发送数据

#客户端
#创建一个基于TCP连接的Socket
import socket# 导入socket库:
# 创建一个socket:
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#AF_INET指定使用IPv4协议;IPv6为AF_INET6.SOCK_STREAM指定使用面向流的TCP协议
# 建立连接:
s.connect(('www.sina.com.cn', 80)) #tuple，包含地址和端口号
# 发送数据:
s.send(b'GET / HTTP/1.1\r\nHost: www.sina.com.cn\r\nConnection: close\r\n\r\n')
# 接收数据:
buffer = []
while True:
    # 每次最多接收1k字节:
    d = s.recv(1024) #recv(max)方法，一次最多接收指定的字节数
    if d:
        buffer.append(d)
    else:
        break
data = b''.join(buffer)
# 关闭连接:
s.close()
header, html = data.split(b'\r\n\r\n', 1)
print(header.decode('utf-8'))
# 把接收的数据写入文件:
with open('sina.html', 'wb') as f:
    f.write(html)

#服务器
import socket,threading,time
def tcplink(sock, addr):  #tcplink定义的代码应该放在调用之前
    print('Accept new connection from %s:%s...' % addr)
    sock.send(b'Welcome!')
    while True:
        data = sock.recv(1024)
        time.sleep(1)
        if not data or data.decode('utf-8') == 'exit':
            break
        sock.send(('Hello, %s!' % data.decode('utf-8')).encode('utf-8'))
    sock.close()
    print('Connection from %s:%s closed.' % addr)

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#监听端口：
s.bind(('127.0.0.1',9999)) #小于1024的端口号必须要有管理员权限才能绑定
#0.0.0.0:所有的网络地址,127.0.0.1:本机地址
s.listen(5) #指定等待连接的最大数量
print('Waiting for nConnection...')
while True:
    # 接受一个新连接:
    sock, addr = s.accept()
    # 创建新线程来处理TCP连接:
    t = threading.Thread(target=tcplink, args=(sock, addr))
    t.start()
#用来测试的客户端程序
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 建立连接:
s.connect(('127.0.0.1', 9999))
# 接收欢迎消息:
print(s.recv(1024).decode('utf-8'))
for data in [b'Michael', b'Tracy', b'Sarah']:
    # 发送数据:
    s.send(data)
    print(s.recv(1024).decode('utf-8'))
s.send(b'exit')
s.close()

#客户端程序运行完毕就退出，服务器程序会永远运行下去，必须按Ctrl+C退出程序
#同一个端口，被一个Socket绑定了以后，就不能被别的Socket绑定了


#UDP编程 面向无连接的协议

#服务器
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# 绑定端口:
s.bind(('127.0.0.1', 9999))
#不需要调用listen()方法，而是直接接收来自任何客户端的数据：
print('Bind UDP on 9999...')
while True:
    # 接收数据:
    data, addr = s.recvfrom(1024)
    print('Received from %s:%s.' % addr)
    s.sendto(b'Hello, %s!' % data, addr)

#客户端
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
for data in [b'Michael', b'Tracy', b'Sarah']:
    # 发送数据: 不需要调用connect()，直接通过sendto()给服务器发数据：
    s.sendto(data, ('127.0.0.1', 9999))
    # 接收数据:
    print(s.recv(1024).decode('utf-8'))
s.close()
 
#服务器绑定UDP端口和TCP端口互不冲突


#电子邮件
#发件人 -> MUA -> MTA -> MTA -> 若干个MTA -> MDA <- MUA <- 收件人
#发邮件时，MUA和MTA使用的协议是SMTP
#收邮件时，MUA和MDA使用的协议有两种：POP，IMAP(可直接操作MDA上存储的邮件)

#SMTP发送邮件 纯文本邮件、HTML邮件以及带附件的邮件
#发送纯文本邮件
from email import encoders
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText  #email负责构造邮件
from email.utils import parseaddr, formataddr
import smtplib #smtplib负责发送邮件
#构造函数_format_addr()格式化邮件地址，不能简单传入name <addr@example.com>，
#因为如果包含中文，需要通过Header对象进行编码。
def _format_addr(s): 
    name, addr = parseaddr(s) #解析字符串中的email地址
    return formataddr((Header(name, 'utf-8').encode(), addr))
#通过SMTP发出
from_addr=input('from:')
password=input('Password:') #密码是授权码
to_addr=input('To:')
smtp_server=input('SMTP server:') # 输入SMTP服务器地址:
#邮件正文：
msg=MIMEText('hello,send by Python...','plain','utf-8')
# MIME的subtype,'plain'表示纯文本 ; utf-8编码保证多语言兼容性
#把From、To和Subject添加到MIMEText中，显示邮件主题、发件人、收件人等信息
msg['From'] = _format_addr('Python爱好者 <%s>' % from_addr)
msg['To'] = _format_addr('管理员 <%s>' % to_addr)#接收的是字符串而不是list
msg['Subject'] = Header('来自SMTP的问候……', 'utf-8').encode()

server=smtplib.SMTP_SSL(smtp_server,465) # qq邮箱SMTP协议默认端口
server.set_debuglevel(1) #打印出和SMTP服务器交互的所有信息
#SMTP协议就是简单的文本命令和响应
server.login(from_addr,password) #登录SMTP服务器
server.sendmail(from_addr,[to_addr],msg.as_string()) #发邮件
#可一次发给多个人传入list; as_string()把MIMEText对象变成str
server.quit()

#发送HTML邮件
msg = MIMEText('<html><body><h1>Hello</h1>' +
    '<p>send by <a href="http://www.python.org">Python</a>...</p>' +
    '</body></html>', 'html', 'utf-8')

#发送附件
#MIMEMultipart邮件本身，MIMEText邮件正文，MIMEBase附件
# 邮件对象:
msg = MIMEMultipart()
msg['From'] = _format_addr('Python爱好者 <%s>' % from_addr)
msg['To'] = _format_addr('管理员 <%s>' % to_addr)
msg['Subject'] = Header('来自SMTP的问候……', 'utf-8').encode()
# 邮件正文是MIMEText:
msg.attach(MIMEText('send with file...', 'plain', 'utf-8'))
# 添加附件就是加上一个MIMEBase，从本地读取一个图片:
with open('lbf.jpg', 'rb') as f:
    # 设置附件的MIME和文件名:
    mime = MIMEBase('image', 'jpg', filename='lbf.jpg')
    # 加上必要的头信息:
    mime.add_header('Content-Disposition', 'attachment', filename='lbf.jpg')
    mime.add_header('Content-ID', '<0>')
    mime.add_header('X-Attachment-Id', '0')
    # 把附件的内容读进来:
    mime.set_payload(f.read())
    # 用Base64编码:
    encoders.encode_base64(mime)
    # 添加到MIMEMultipart:
    msg.attach(mime)

#发送图片
#把邮件作为附件添加进去，在HTML中通过引用src="cid:0"
#如果有多个图片，给它们依次编号，然后引用不同的cid:x即可
msg.attach(MIMEText('<html><body><h1>Hello</h1>' +
    '<p><img src="cid:0"></p>' +
    '</body></html>', 'html', 'utf-8'))

#同时支持HTML和Plain格式
#利用MIMEMultipart就可以组合一个HTML和Plain，指定subtype是alternative
msg = MIMEMultipart('alternative')
msg['From'] = ...
msg['To'] = ...
msg['Subject'] = ...
msg.attach(MIMEText('hello', 'plain', 'utf-8'))
msg.attach(MIMEText('<html><body><h1>Hello</h1></body></html>', 'html', 'utf-8'))
# 正常发送msg对象...

#加密SMTP 先创建SSL安全连接，然后再使用SMTP协议发送邮件
smtp_server = 'smtp.gmail.com'
smtp_port = 587
server = smtplib.SMTP(smtp_server, smtp_port)
server.starttls()
# 剩下的代码和前面的一模一样:
server.set_debuglevel(1)
...

#继承关系
Message
+- MIMEBase  #可以表示任何对象
   +- MIMEMultipart  #多个对象组合
   +- MIMENonMultipart 
      +- MIMEMessage
      +- MIMEText #文本邮件对象
      +- MIMEImage #作为附件的图片


#POP3收取邮件
#1.用poplib把邮件的原始文本下载到本地；2.用email解析原始文本，还原为邮件对象
import poplib
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr

#递归地打印出Message对象的层次结构：
# indent用于缩进显示:
def print_info(msg, indent=0):
    if indent == 0:
        for header in ['From', 'To', 'Subject']:
            value = msg.get(header, '')
            if value:
                if header=='Subject':
                    value = decode_str(value)
                else:
                    hdr, addr = parseaddr(value)
                    name = decode_str(hdr)
                    value = u'%s <%s>' % (name, addr)
            print('%s%s: %s' % ('  ' * indent, header, value))
    if (msg.is_multipart()):
        parts = msg.get_payload()
        for n, part in enumerate(parts):
            print('%spart %s' % ('  ' * indent, n))
            print('%s--------------------' % ('  ' * indent))
            print_info(part, indent + 1)
    else:
        content_type = msg.get_content_type()
        if content_type=='text/plain' or content_type=='text/html':
            content = msg.get_payload(decode=True)
            charset = guess_charset(msg)
            if charset:
                content = content.decode(charset)
            print('%sText: %s' % ('  ' * indent, content + '...'))
        else:
            print('%sAttachment: %s' % ('  ' * indent, content_type))

def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value

def guess_charset(msg):
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset

# 输入邮件地址, 口令和POP3服务器地址:
email = input('Email: ')
password = input('Password: ')
pop3_server = input('POP3 server: ')
# 连接到POP3服务器:
server = poplib.POP3_SSL(pop3_server)
# 可以打开或关闭调试信息:
server.set_debuglevel(1)
# 可选:打印POP3服务器的欢迎文字:
print(server.getwelcome().decode('utf-8'))
# 身份认证:
server.user(email)
server.pass_(password)
# stat()返回邮件数量和占用空间:
print('Messages: %s. Size: %s' % server.stat())
# list()返回所有邮件的编号:
resp, mails, octets = server.list()
# 可以查看返回的列表类似[b'1 82923', b'2 2184', ...]
print(mails)
# 获取最新一封邮件, 注意索引号从1开始:
index = len(mails)

for i in range(len(mails)):
    resp, lines, octets = server.retr(len(mails) - i)
    msg_content = b'\r\n'.join(lines).decode('utf-8')
    msg = Parser().parsestr(msg_content)
    print_info(msg)
    i = i + 1
        
resp, lines, octets = server.retr(index)
# lines存储了邮件的原始文本的每一行,
# 可以获得整个邮件的原始文本:
msg_content = b'\r\n'.join(lines).decode('utf-8')
# 稍后解析出邮件:
msg = Parser().parsestr(msg_content)
# 可以根据邮件索引号直接从服务器删除邮件:
# server.dele(index)

# 关闭连接:
server.quit()



