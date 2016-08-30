#python 学习笔记4之正则表达式


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

