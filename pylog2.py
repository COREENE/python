#python 学习笔记2之模块，面向对象编程，面向对象高级编程，错误调试和测试
#难点：metaclass元类

#模块
#目录组织模块——包Package
#__init__.py本身就是一个模块，而它的模块名就是包名mycompany

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' a test module '#模块的文档注释

__author__ = 'Michael Liao' #作者

import sys #导入sys模块

def test():
    args = sys.argv
    if len(args)==1:
            print('Hello, world!')
    elif len(args)==2:
        print('Hello, %s!' % args[1])
    else:
        print('Too many arguments!')

if __name__=='__main__': #if测试，判断是否是直接运行该.py文件
    test()
    #如果 import 一个模块，__name__的值通常为模块文件名
    #直接运行模块,__name__的值是一个特别缺省"__main__"
    #可以让一个模块通过命令行运行时执行一些额外的代码

#作用域
#正常的函数和变量名是公开的（public），可以被直接引用
#__xxx__：特殊变量，可以被直接引用，但是有特殊用途
#_xxx和__xxx：非公开的（private）函数或变量，不应该被直接引用

#安装第三方模块 
pip install Pillow #通过包管理工具pip安装Pillow



#面向对象编程Object Oriented Programming
#类Class和实例Instance“
class Student(object):  #object是父类
    def __init__(self, name, score): #self指向创建实例本身
        self.name = name
        self.score = score  #初始化实例属性
#__init__就是C++中的构造函数，self就是指向对象首地址的this指针
    def print_score(self): #定义方法，第一个参数是self
        print(self.name, self.score)
#方法是与实例绑定的函数，可以直接访问实例的数据        
bart = Student('Bart Simpson', 59) #调用时不用传递self
lisa = Student('Lisa Simpson', 87)
bart.print_score() #不用传递self，其他参数正常传入
lisa.print_score()
lisa.age=8 #python允许对实例变量绑定任何数据

#访问限制
self.__name = name
# __xxx :私有变量，外部不能直接访问, 被解释成了_Student__name
self._name = name
# _xxx :外部可以访问的私有变量，但是最好不要直接访问

#继承和多态
class Animal(object):
	def run(self):
		print('Animal is running...')
#基类、父类或超类（Base class、Super class）
class Dog(Animal):  
    def run(self):  #子类的run()覆盖父类的run()
        print('Dog is running...')
#子类（Subclass）
#动态语言的鸭子类型特点决定了继承不像静态语言那样是必须的
		
#获取对象信息
In[1]:type(123) 
Out[1]:<class'int'>
#type返回对应class类型
In[2]:type((x for x in range(10)))==types.GeneratorType
Out[2]:True
#使用types模块中定义的常量判断对象是否是函数
a = Animal()
In[3]:isinstance(a, Animal)
Out[3]:True
#isinstance()判断class的类型
In[4]:isinstance('a', str)
Out[4]:True
#isinstance()判断基本类型
In[5]:isinstance([1, 2, 3], (list, tuple))
Out[5]:True
#isinstance()判断一个变量是否是某些类型中的一种
In[6]:dir('ABC')
#dir()获得一个对象的所有属性和方法
 'ABC'.__len__()  #__xxx__的属性和方法在Python有特殊用途
len('ABC')  #两者等价 返回长度
'ABC'.lower()  #普通属性和方法

#操作对象状态
hasattr(obj, 'x') # 有属性'x'吗？
setattr(obj, 'y', 19) # 设置一个属性'y'
getattr(obj, 'y') # 获取属性'y'
getattr(obj, 'z', 404) 
# 获取属性'z'，如果不存在，返回默认值404
fn = getattr(obj, 'power') # 获取属性'power'并赋值到变量fn
fn # fn指向obj.power
fn() # 调用fn()与调用obj.power()是一样的
#只有在不知道对象信息的时候，我们才会去获取对象信息

#实例属性和类属性
class Student(object):
	name = 'Student'   #定义类属性
s=Student() # 创建实例s
In[1]:print(s.name)
Out[1]:Student #实例并没有name属性，继续查找class的name属性
In[2]:print(Student.name)
Out[2]:Student
In[3]:s.name='Michael' # 给实例绑定name属性
In[4]:print(s.name)
Out[4]:Michael # 实例属性优先级比类属性高，屏蔽类的name属性
In[5]:print(Student.name)
Out[5]:Student
In[6]:del s.name  #删除实例的name属性
In[7]:print(s.name)
Out[7]:Student




#面向对象高级编程
#Python是一门动态语言，可以在运行过程中，修改对象的属性和增删方法
#任何类的实例对象包含一个__dict__, Python通过这个dict将任意属性绑定到对象上
#实例的dict只保持实例的变量，对于类的属性是不保存的，类的属性包括变量和函数
#定义了slots后，slots中定义的变量变成了类的描述符，而不再有dict
#slots的作用是阻止在实例化类时为实例分配dict,只有slots里的名称才可以绑定
!???#？ __slots__ = ('__dict__')	时限制作用失效

#绑定
class Student(object):
    pass
s=Student()
s.name = 'Michael' # 动态给实例绑定一个属性
print(s.name)  #Michael
def set_age(self, age): # 定义一个函数作为实例方法
	self.age = age #也要加self！
from types import MethodType
s.set_age = MethodType(set_age, s) # 给实例绑定一个方法
s.set_age(25) # 调用实例方法
s.age #测试结果 25
#class绑定方法
def set_score(self,score):
	self.score=score
Student.set_score=set_score  #给class绑定方法
#动态绑定允许我们在程序运行的过程中动态给class加上功能


#使用__slots__ 限制实例属性 (节省内存)
class Student(object):
	__slots__=('name','age') #用tuple定义允许绑定的属性名称
#任何试图创建一个其名不在__slots__中的实例属性将导致AttributeError异常
#__slots__定义的属性j仅对当前类实例起作用，对继承的子类不起作用


#一个例题的混乱结果
def set_city(self, city):
    self.city=city  #定义一个方法添加属性
Student.set_city = MethodType(set_city, Student) #方法名属性名都可不被包括
#MethodType对类绑定，在Stu内存中创建一个link指向外部的方法
#创建Sut实例是link被复制，所有实例和类指向同一个方法
#MethodType只能用以实例，强行用于类后，作为类似于全局变量的存在影响在该类下的所有实例
Student.set_city = set_city#方法名和添加的属性名必须被slots包括
a.set_city = MethodType(set_city, a)#方法名和添加的属性名必须被slots包括

Student.set_city=MethodType(set_city, Student)
#方法的self指向类，而不是实例。所有实例共享一个内存，相互影响
Student.set_city=set_city 
#相当于把方法写进类属性。可以有效的指定到不同的实例
#两者是不同层面的
#总结，MethodType用于绑定实例，不能绑定类


#使用@property
class Student(object):

    @property  #把一个getter方法变成属性
    def score(self):  
        return self._score #注意不能和函数名self.score一样否则递归

    @score.setter  #@property本身又创建了另一个装饰器@score.setter
    def score(self, value):  #把一个setter方法变成属性赋值
        if not isinstance(value, int):
            raise ValueError('score must be an integer!')
        if value < 0 or value > 100:
            raise ValueError('score must between 0 ~ 100!')
        self._score = value
s = Student()
s.score = 60 # OK,实际转化为s.set_score(60)
s.score # OK,实际转化为s.get_score()
s._score = 50 #OK,直接修改,不经过setter设置.但私有变量最好不要这样
s._core #OK,直接读取


#多重继承 MixIn 有了slots就不要继承
#有共同方法时，优先级时继承的首个父类方法
#python自带的网络服务TCPServer and UDPServer
#python自带的多进程、多线程模型ForkingMixIn and ThreadingMixIn
#通过组合，我们就可以创造出合适的服务来。


#定制类 __xxx__
#__str__:打印实例
class Student(object):
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return 'Student object (name=%s)' % self.name
    __repr__ = __str__ #直接显示变量调用__repr__()

#__iter__:
#如果一个类想被用于for...in循环,就必须实现一个__iter__()方法,返回一个迭代对象
#然后Python的for循环不断调用该迭代对象的__next__()方法拿到循环的下一个值
class Fib(object): #斐波那契数列
    def __init__(self):
        self.a, self.b = 0, 1 # 初始化两个计数器a，b
    def __iter__(self):
        return self # 实例本身就是迭代对象，故返回自己
    def __next__(self):
        self.a, self.b = self.b, self.a + self.b # 计算下一个值
        if self.a > 100000: # 退出循环的条件
            raise StopIteration();
        return self.a # 返回下一个值
for n in Fib():
	print(n) #1 1 2 3 5...46368 75025

#__getitem__ 
class Fib(object):
    def __getitem__(self, n):
        if isinstance(n, int): # n是索引
            a, b = 1, 1
            for x in range(n): # 循环n次
                a, b = b, a + b
            return a
        if isinstance(n, slice): # n是切片
            start = n.start
            stop = n.stop
            if start is None:
                start = 0
            a, b = 1, 1
            L = []
            for x in range(stop):
                if x >= start:
                    L.append(a)
                a, b = b, a + b
            return L
f = Fib()
f[0] #1
f[0:5] #[1, 1, 2, 3, 5]
__getitem__() #按照下标取出元素，切片
__setitem__() #把对象视作list或dict来对集合赋值
__delitem__() #用于删除某个元素

#__getattr__ 作用:可以针对完全动态的情况作调用
class Student(object):
	def __init__(self):
		self.name = 'Michael'
	def __getattr__(self, attr):
		if attr=='score':
			return 99       #返回属性
		if attr=='age':
			return lambda: 25 #返回函数
		raise AttributeError('has no attribute \'%s\'' % attr)
    #在没有找到属性的情况下，调用__getattr__
s = Student()
print(s.name)
print(s.score) #调用__getattr__(self, 'score')
print(s.age()) #调用__getattr__(self, 's.age()')


#__call__ 替代instance.method()调用实例方法
class Student(object):
    def __init__(self, name):
        self.name = name
    def __call__(self):
        print('My name is %s.' % self.name)
s = Student('Michael')
s() # self参数不要传入
My name is Michael.
#对象和函数没有根本区别
callable #判断一个对象是否是“可调用”对象
callable(Student()) #True
callable(max) #True

class Chain(object):
    name='michael'
    def __init__(self, path=''):
        self._path = path

    def __getattr__(self, path):
        if path == 'user':
            return Chain('%s/%s' % (self._path, self.name))
        return Chain('%s/%s' % (self._path, path))

    def __str__(self):
        return self._path

    __repr__ = __str__

print(Chain().users.user.repos)  #return：/users/michael/repos


#使用枚举类
from enum import Enum
Month = Enum('Month', ('Jan', 'Feb', 'Mar', 'Apr', 'May', 
	'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))
#获得Month类型的枚举类
#Enum-Month-Jan的逻辑关系可以看作是： 父类 - 子类 - 实例
for name, member in Month.__members__.items():
	print(name, '=>', member, ',', member.value)
#Jan => Month.Jan ,1  ...Dec => Month.Dec ,12

from enum import Enum, unique
@unique    #@unique检查保证没有重复值
class Weekday(Enum):
    Sun = 0 # Sun的value被设定为0
    Mon = 1
    Tue = 2
    Wed = 3
    Thu = 4
    Fri = 5
    Sat = 6
#既可以用成员名称引用枚举常量，又可以直接根据value的值获得枚举常量。
#Enum可以把一组相关常量定义在一个class中，class不可变，成员可以直接比较


#使用元类
type() #可以返回一个对象的类型，又可以动态创建出新的类型
#写一个hello.py 模块：
class Hello(object):
    def hello(self, name='world'):
        print('Hello, %s.' % name)
h = Hello()
print(type(Hello)) #<class 'type'>
print(type(h)) #<class 'hello.Hello'>

def fn(self, name='world'): # 先定义函数
    print('Hello, %s.' % name)
Hello = type('Hello', (object,), dict(hello=fn)) # 创建Hello class
h = Hello()
h.hello() #Hello,world.
print(type(Hello)) #<class 'type'>
print(type(h)) #<class '__main__.Hello'>
#要创建一个class对象，type()函数依次传入3个参数：
#1.class的名称；
#2.继承的父类集合(Python支持多重继承，如果只有一个父类，tuple的单元素写法)；
#3.class的方法名称与函数绑定，这里我们把函数fn绑定到方法名hello上

#metclass 元类 #metaclass的类名总是以Metaclass结尾
#先定义metaclass，就可以创建类，最后创建实例
#可以把类看成是metaclass创建出来的“实例”
class ListMetaclass(type): # metaclass是类的模板，所以必须从`type`类型派生：
    def __new__(cls, name, bases, attrs):
        attrs['add'] = lambda self, value: self.append(value)
        return type.__new__(cls, name, bases, attrs)
#__new__()方法接收到的参数依次是：
#1.当前准备创建的类的对象；2.类的名字；3.类继承的父类集合；4.类的方法集合。        
class MyList(list, metaclass=ListMetaclass):
    pass
#使用ListMetaclass来定制类，传入关键字参数metaclass
#指示Python解释器在创建MyList时，要通过ListMetaclass.__new__()来创建
L = MyList()
L.add(1)
In[1]:L
Out[1]:[1]



#错误、调试和测试
#except捕获错误
try:
    print('try...')
    r = 10 / 0  #此处发生错误，跳转至except语句块
    print('result:', r)
except ValueError as e: #异常类型;异常对象(ValueError的Instance)
    print('ValueError:', e)
except ZeroDivisionError as e:
    print('ZeroDivisionError:', e)
else: #当没有错误发生时，自动执行else语句
    print('no error!')
finally:  #一定被执行
    print('finally...')
print('END')  #有错误发生时不执行
#except不但捕获该类型的错误，还把其子类也“一网打尽”
#try...except捕获错误可以跨越多层调用

#logging 记录错误
import logging
def foo(s):
    return 10 / int(s)
def bar(s):
    return foo(s) * 2
def main():
    try:
        bar('0')
    except Exception as e:
        logging.exception(e)
main()
print('END')
#程序打印完错误信息后会继续执行，并正常退出

#raise抛出错误 抛出错误后接下来的语句不会执行
class FooError(ValueError): #定义一个错误的class
    pass
def foo(s):
    n = int(s)
    if n==0:
        raise FooError('invalid value: %s' % s)
    return 10 / n
#xcept中raise一个Error，还可以把一种类型的错误转化成另一种类型    
try:
    10 / 0
except ZeroDivisionError:
    raise ValueError('input error!')

#调试
#assert
def foo(s):
    n = int(s)
    assert n != 0, 'n is zero!'
    return 10 / n
#assert断言 如果断言失败，assert语句本身就会抛出AssertionError
#启动Python解释器时可以用-O参数来关闭assert #python -O err.py

#logging
import logging
logging.basicConfig(level=logging.INFO) #配置
s = '0'
n = int(s)
logging.info('n = %d' % n)
print(10 / n)
#可指定记录信息的级别，有DEBUG，INFO，WARNING，ERROR

#pdb 启动：python3 -m pdb err.py
#pdb.set_tcace()
import pdb
s = '0'
n = int(s)
pdb.set_trace() # 运行到这里会自动暂停
print(10 / n)
#break 或 b 设置断点       ;continue 或 c 继续执行程序 
#list 或 l 查看当前行的代码段      ;step 或 s 进入函数 
#return 或 r 执行代码直到从当前函数返回 
#exit 或 q 中止并退出      ;next 或 n 执行下一行 
#p 变量名 打印变量的值     ;help 帮助


#单元测试
#mydict.py
class Dict(dict):
    def __init__(self, **kw):
        super().__init__(**kw) #super()调用父类方法
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)
    def __setattr__(self, key, value):
        self[key] = value
#mydict_test.py
import unittest  #unittest测试模块
from mydict import Dict
class TestDict(unittest.TestCase): #(unittest封测的标准类)
#测试方法以test开头，否则测试的时候不会被执行
    def test_init(self): #测验Dict()中key-valve是否匹配
        d = Dict(a=1, b='test') 
        self.assertEqual(d.a, 1) #断言值结果与1相等
        self.assertEqual(d.b, 'test')
        self.assertTrue(isinstance(d, dict))#检验Dict()是否是dict类型
    def test_key(self):  #检测d['key']赋值
        d = Dict()
        d['key'] = 'value'
        self.assertEqual(d.key, 'value')
    def test_attr(self): #检验属性赋值
        d = Dict()
        d.key = 'value'
        self.assertTrue('key' in d)
        self.assertEqual(d['key'], 'value') #相互调用
    def test_keyerror(self):   #抛出key法输入未存在key的错误
        d = Dict()
        with self.assertRaises(KeyError): #断言期待抛出指定类型的Error
            value = d['empty'] #通过d['empty']访问不存在的key时，抛出KeyError
    def test_attrerror(self):   #抛出属性赋值法输入未存在key的错误
        d = Dict()
        with self.assertRaises(AttributeError):
            value = d.empty #通过d.empty访问不存在的key时，抛出AttributeError
	def setUp(self): #连接数据库
		print('setUp...')   
    def tearDown(self): #关闭数据库
        print('tearDown...')   
#运行单元测试 
#方式1
if __name__ == '__main__':
    unittest.main()  #在mydict_test.py的最后加上两行代码
python mydict_test.py #命令行直接运行
#方式2  在命令行通过参数-m unittest直接运行单元测试（推荐做法）
python -m unittest mydict_test
 

#文档测试 doctest
#test.py  注意：>>> 后面有空格！
def abs(n):
 '''
    Function to get absolute value of number.
    Example:
    >>> abs(1)
    1 
    >>> abs(-1)
    1
    >>> abs(0)
    0
    '''
    return n if n >= 0 else (-n)
if __name__=='__main__':
    import doctest
    doctest.testmod()
#交互环境运行 如果python test.py -v 显示具体步骤
>>> d2['empty']
Traceback (most recent call last):
    ...  #省略
KeyError: 'empty'