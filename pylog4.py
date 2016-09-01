#python 学习笔记4之正则表达式,常用内建模块，常用第三方模块，virtualenv，图形界面


#正则表达式
'\d' 一个数字
'\w' 一个字母或数字
'.' 任意字符
'*' 任意个字符（包括0个）
'+' 至少一个字符
'{n}' n个字符
'{n,m}' n-m个字符
'\s' 一个空格（也包括Tab等空白符）
#特殊字符在正则表达式中，要用'\'转义
'[0-9a-zA-Z\_]'一个数字、字母或者下划线；
'[0-9a-zA-Z\_]+'至少由一个数字、字母或下划线组成的字符串
'[a-zA-Z\_][0-9a-zA-Z\_]*'由字母或下划线开头，后接任意个
由一个数字、字母或者下划线组成的字符串
'[a-zA-Z\_][0-9a-zA-Z\_]{0, 19}'变量的长度是1-20个字符
'A|B'A或B
'^'表示行的开头,'^\d'表示必须以数字开头
'$'表示行的结束，'\d$'表示必须以数字结束
#py也可以匹配'python'，加上^py$就变成了整行匹配，就只能匹配'py'

>>> import re  #re模块，包含所有正则表达式的功能
>>> re.match(r'^\d{3}\-\d{3,8}$', '010-12345')
<_sre.SRE_Match object; span=(0, 9), match='010-12345'>
>>> re.match(r'^\d{3}\-\d{3,8}$', '010 12345')
>>>
#match()方法判断是否匹配
test = '用户输入的字符串'
if re.match(r'正则表达式', test):
    print('ok')
else:
    print('failed')

#切分字符串
>>> re.split(r'[\s\,\;]+', 'a,b;; c  d')
['a', 'b', 'c', 'd']

#分组
>>> m = re.match(r'^(\d{3})-(\d{3,8})$', '010-12345')
>>> m
<_sre.SRE_Match object; span=(0, 9), match='010-12345'>
>>> m.group(0)
'010-12345'
>>> m.group(1)
'010'
>>> m.group(2)
'12345'

#贪婪匹配  匹配尽可能多的字符
>>> re.match(r'^(\d+)(0*)$', '102300').groups()
('102300', '')
>>> re.match(r'^(\d+?)(0*)$', '102300').groups()
('1023', '00') #非贪婪匹配

#编译
>>> import re
# 编译:
>>> re_telephone = re.compile(r'^(\d{3})-(\d{3,8})$')
# 使用：
>>> re_telephone.match('010-12345').groups()
('010', '12345')
>>> re_telephone.match('010-8086').groups()
('010', '8086')



#常用内建模块

#datetime
>>> from datetime import datetime

>>> now = datetime.now() # 获取当前datetime
>>> print(now)
2015-05-18 16:28:07.198690
>>> print(type(now))
<class 'datetime.datetime'>
>>> dt = datetime(2015, 4, 19, 12, 20) # 用指定日期时间创建datetime
>>> print(dt)
2015-04-19 12:20:00

#datetime与timestamp转换
timestamp = 0 = 1970-1-1 00:00:00 UTC+0:00
timestamp = 0 = 1970-1-1 08:00:00 UTC+8:00 # 对应的北京时间
#timestamp是一个浮点数，它没有时区的概念，而datetime是有时区的
>>> dt = datetime(2015, 4, 19, 12, 20) # 用指定日期时间创建datetime
>>> dt.timestamp()  # 把datetime转换为timestamp
1429417200.0 # 小数位表示毫秒数
>>> t = 1429417200.0
>>> print(datetime.fromtimestamp(t)) #timestamp转换为datetime
2015-04-19 12:20:00

#str与datetime转换 转换后的datetime是没有时区信息的
>>> cday = datetime.strptime('2015-6-1 18:19:59', '%Y-%m-%d %H:%M:%S')
>>> print(cday)
2015-06-01 18:19:59
>>> now = datetime.now()
>>> print(now.strftime('%a, %b %d %H:%M'))
Mon, May 05 16:28

#datetime加减
>>> from datetime import datetime, timedelta
>>> now = datetime.now()
>>> now
datetime.datetime(2015, 5, 18, 16, 57, 3, 540997)
>>> now + timedelta(hours=10)
datetime.datetime(2015, 5, 19, 2, 57, 3, 540997)
>>> now - timedelta(days=1)
datetime.datetime(2015, 5, 17, 16, 57, 3, 540997)
>>> now + timedelta(days=2, hours=12)
datetime.datetime(2015, 5, 21, 4, 57, 3, 540997)

#本地时间转换为UTC时间
>>> from datetime import datetime, timedelta, timezone #时区属性
>>> tz_utc_8 = timezone(timedelta(hours=8)) # 创建时区UTC+8:00
>>> now = datetime.now()
>>> now
datetime.datetime(2015, 5, 18, 17, 2, 10, 871012)
>>> dt = now.replace(tzinfo=tz_utc_8) # 强制设置为UTC+8:00
>>> dt
datetime.datetime(2015, 5, 18, 17, 2, 10, 871012,
 tzinfo=datetime.timezone(datetime.timedelta(0, 28800)))

#时区转换
# 拿到UTC时间，并强制设置时区为UTC+0:00:
>>> utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
>>> print(utc_dt)
2015-05-18 09:05:12.377316+00:00
# astimezone()将转换时区为北京时间:
>>> bj_dt = utc_dt.astimezone(timezone(timedelta(hours=8)))
>>> print(bj_dt)
2015-05-18 17:05:12.377316+08:00
# astimezone()将转换时区为东京时间:
>>> tokyo_dt = utc_dt.astimezone(timezone(timedelta(hours=9)))
>>> print(tokyo_dt)
2015-05-18 18:05:12.377316+09:00
# astimezone()将bj_dt转换时区为东京时间:
>>> tokyo_dt2 = bj_dt.astimezone(timezone(timedelta(hours=9)))
>>> print(tokyo_dt2)
2015-05-18 18:05:12.377316+09:00

#datetime表示的时间需要时区信息才能确定一个特定的时间，否则只能视为本地时间。
#如果要存储datetime，最佳方法是将其转换为timestamp再存储，因为timestamp的值与时区完全无关。


#collections
#namedtuple
>>> from collections import namedtuple
>>> Point = namedtuple('Point', ['x', 'y'])
>>> p = Point(1, 2)
>>> p.x
1
>>> p.y
2
>>> isinstance(p, Point)
True
>>> isinstance(p, tuple)
True
# namedtuple('名称', [属性list]):
Circle = namedtuple('Circle', ['x', 'y', 'r'])

#deque
#append() pop() appendleft() popleft()

#defaultdict 引用的key不存在时抛出默认值
defaultdict(lambda:'N/A')

#OrderedDict 保持key的顺序,按插入顺序排列
od=OrderedDict([('a',1),('b',2),('c',3)])

#Counter 计数器
from collections import Counter
c=Counter()
for ch in 'programming':
	c[ch]=c[ch]+1
>>>c
Counter(['g':2,'m':2,'r':2,'a':1...])


#base64  通过查表的编码方法，适用于小段内容的编码
#3字节的二进制数据编码为4字节的文本数据
#将3个字节=24bit，划为4组，每组6个bit
#如果二进制数据不是3的倍数，在编码末尾加 =
>>>base64.b64encode(b'i\xb7\x1d\xfb\xef\xff')
b'abcd++//'
>>>base64.urlsafe_b64encode(b'i\xb7\x1d\xfb\xef\xff')
b'abcd--__' #+和/变成-和_

'abcd' -> 'YWJjZA==' #标准Base64
'abcd' -> 'YWJjZA'
 #自动去掉=，解码时加上=使Base64字符串长度变成4的倍数


#struct
>>>import struct
>>>struct.pack('>I',10240099)
b'\x00\x9c@c'
# > 表示字节顺序是big-endian，即网络序，I表示4字节无符号整数
>>>struct.unpack('>IH',b'\xf0\xf0\xf0\xf0\x80\x80')
(4042322160,32896)
# >IH 后面bytes依次变为I:4字节无符号整数和H：2字节无符号整数


#hashlib  摘要算法
# MD5
import hashlib
md5 = hashlib.md5()
md5.update('how to use md5 in python hashlib?'.encode('utf-8'))
print(md5.hexdigest())
#如果数据量很大可分块多次调用update()
d5.update('how to use md5 in'.encode('utf-8'))
d5.update('python hashlib?'.encode('utf-8'))
print(md5.hexdigest()) #结果是128 bit，通常用32位16进制字符串表示

# SHA1
import hashlib
md5 = hashlib.sha1()
d5.update('how to use md5 in'.encode('utf-8'))
d5.update('python hashlib?'.encode('utf-8'))
print(sha1.hexdigest()) #结果是160 bit，通常用40位16进制字符串表示

#比SHA1更安全的算法是SHA256和SHA512，但越安全越慢且摘要长度长

#加盐
def calc_md5(password):
	return get_md5(password + 'the-Salt')


#itertools 返回值是Iterator
>>>import itertools
>>>natuals=itertools.count(1)
>>>for n in natuals:
... print(n)
1
2
3
...
#count()创造一个无限的迭代器，Ctrl+C退出

cycle() #把传入的一个序列无线重复下去
repeat('A',3) #把一个元素无线重复下去,可限定重复次数

#takewhile() 根据条件判断截取一个有限序列
>>>natuals = itertools.count(1)
>>>ns = itertools.takewhile(lambda x:x<=10,natuals)
>>>list(ns)
[1,2,3,4,5,6,7,8,9,10]

#chain() 把一组迭代对象串联形成更大的迭代器
>>>for  c in itertools.chain('ABC','XYZ'):
>>>print(c)
# 迭代效果：'A''B''C''X''Y''Z'

#groupby() 把迭代器中相邻的重复元素挑出来放在一起
>>>for key,group in itertools.groupby('AAABBBCCAAA'):
	print(key,list(group))
A['A','A','A']
B['B','B','B']
C['C','C']
A['A','A','A']

>>>for key,group in itertools.groupby('AaaBBbcCAAa',lambda c:c.upper()):
	print(key,list(group))
A['A','a','a']
B['B','B','b']
C['c','C']
A['A','A','a']


#XML
#DOM占用内存大，解析慢，可遍历树的节点 
#SAX流模式，边读边解析，占用内存小，解析快，需要自己处理事件


#HTMLParser

#urllib


#PIL
from PIL import Image, ImageFilter
# 打开一个jpg图像文件，注意是当前路径:
im = Image.open('test.jpg')
# 获得图像尺寸:
w, h = im.size
print('Original image size: %sx%s' % (w, h))
# 缩放到50%:
im.thumbnail((w//2, h//2))
print('Resize image to: %sx%s' % (w//2, h//2))
# 把缩放后的图像用jpeg格式保存:
im.save('thumbnail.jpg', 'jpeg')
# 应用模糊滤镜:
im2 = im.filter(ImageFilter.BLUR)
im2.save('blur.jpg', 'jpeg')

#随机生成字母验证码
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
# 随机字母:
def rndChar():
    return chr(random.randint(65, 90))
# 随机颜色1:
def rndColor():
    return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))
# 随机颜色2:
def rndColor2():
    return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))
# 240 x 60:
width = 60 * 4
height = 60
image = Image.new('RGB', (width, height), (255, 255, 255))
# 创建Font对象:
font = ImageFont.truetype('C:/Windows/Fonts/Arial.ttf', 36)
# 创建Draw对象:
draw = ImageDraw.Draw(image)
# 填充每个像素:
for x in range(width):
    for y in range(height):
        draw.point((x, y), fill=rndColor())
# 输出文字:
for t in range(4):
    draw.text((60 * t + 10, 10), rndChar(), font=font, fill=rndColor2())
# 模糊:
image = image.filter(ImageFilter.BLUR)
image.save('code.jpg', 'jpeg')


#virtualenv 为一个应用创建一套“隔离”的Python运行环境


#图形界面
from tkinter import * #导入Tkinter包的所有内容
import tkinter.messagebox as messagebox #文本框
#Frame派生一个Application类，这是所有Widget的父容器
class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack() 
        self.createWidgets()
    def createWidgets(self):
        self.nameInput = Entry(self)
        self.nameInput.pack()
        self.alertButton = Button(self, text='Hello', command=self.hello)
        self.alertButton.pack() #pack()方法把Widget加入到父容器中，并实现布局
    def hello(self):
        name = self.nameInput.get() or 'world'
        messagebox.showinfo('Message', 'Hello, %s' % name)
#实例化Application，并启动消息循环
app = Application()
# 设置窗口标题:
app.master.title('Hello World')
# 主消息循环:
app.mainloop()






























