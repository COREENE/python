#python学习笔记1之python基础，函数，高级特性，函数式编程
#难点：装饰器


#!/user/bin/env python3
# -*- coding: utf-8 -*-

#输入输出
print('hello,world')
print('one','two','three') #逗号相当于空格
print('one''two''three')
print('one'+'two'+'three') #这两条等同
print(300)
print('100+200=',100+200) #逗号省略会报错
print('please enter your name')
name=input() #input()输入函数，返回类型为str
print('hello,',name)



#数据类型和变量
print('I\'m \"OK\"!') #转义字符\
#\n换行;  \t制表; \\符号'\';
print('\\\t\\')
print(r'\\\t\\')
#r''表示''内部字符串默认不转义
print('''line1
line2
line3''')
#'''...'''格式表示多行内容,保留'''...'''内格式

print(True) #布尔值True,False,not;python大小写敏感
#空值None，不能理解为0，0是有意义的
a="ABC" #变量a指向数据对象--字符串"ABC"
PI=3.14159265359 #常用全部大写的变量名表示常量
print(10/3) #3.3333333333 精确除法
print(10//3) #3 除法结果取整
print(10%3) #1 取余数



#字符串和编码
ord('A') #65 获取字符的整数表示
chr(65) #A 把编码转换成对应字符
'ABC'.encode('ascii') #b'ABC' 
'中文'.encode('utf-8') #b'\xe4\xb8\xad\xe6\x96\x87'
#str通过encode()方法编码成指定bytes
b'ABC'.decode('ascii') #'ABC'
b'\xe4\xb8\xad\xe6\x96\x87'.decode('utf-8') #'中文'
#bytes通过decode()方法变成str
len('ABC') #'3' 计算str字符数ord('A') 
len(b'ABC') #'3' 计算bytes字节数

#格式化
print ('Hi,%s you have $%d.' % ('Michael',1000000))
# %d整数； %f浮点数； %s字符串；%x十六进制整数
print('%2d-%02d'%(3,1)) #'3-01' 补零
print('%.2f'%3.1415926) #'3.14' 指定整数与小数的位数
print('growth rate:%d %%'%7) #%%表示一个%



#使用list和tuple
classmates=['Michael','Bob','Tracy'] #list
len(classmates) #list长度，空list长度为0
classmates[0] #0,1,2 ; -1,-2,-3
classmates.append('Adam') #末尾追加元素
print(classmates)
classmates[1]='Sarah' #替换元素
L=['Apple',123,True]
s=['python','java',['asp','php'],'scheme'] 
#len(s)==4 ,'php'可写成s[2][1]
t=('Michael','Bob','Tracy') #tuple初始化后不能修改
t0=() #定义空tuple
t1=(5,) #只有1个元素的tuple
t2=(5) #定义5这个数
t3=('a','b',['A','B']) #'可变的'tuple
t3[0] #'b'



#条件判断
age =20
if age>=6:
	print('teenager')
elif age>=18:
	print('adult')
else:
	print('kid')
#'teenager' 
#某判断是True，执行对应语句忽略剩下的elif和else

s=input('birth:') #输出提示词
birth=int(s)
if birth <2000:
	print('00前')
else:
	print('00后')
#int()函数把str转换成整数


#for循环
names=['Michael','Bob','Tracy']
for name in names:
	print (name)
#for x in...把每个元素代入变量x，执行缩进块的语句
list(range(5))
#range(5)生成从0开始小于5的整数序列，list()转化成list
sum=0
for x in range(101):
	sum = sum + x
print (sum)

#while循环
sum=0
n=99
while n>0:
	sum=sum+n
	n=n-2
print (sum)
#Ctrl+C退出程序
#Ctrl+Z


#dict和set
d={'Michael':95,'Bob':75,'Tracy':85}
print(d['Michael'])#95
d['Adam']=67
print(d['Adam'])#67
d['Adam']=90
print(d['Adam'])#90 
#多次对一个key放入value，后面的值会把前面的值冲掉
'Thomas' in d #False #通过in判断key是否存在
d.get('Thomas') #如果key不存在，返回None,交互命令行不显示结果
d.get('Thomas',-1) #-1 #如果key不存在，返回指定的value
d.pop('Bob') #删除key和对应value
d = {'Michael': 95, 'Bob': 75, 'Tracy': 85} 
s=d.get('%s'%input('请输入要查询的姓名：'),'查无此人！')
print(s)
#dict内部存放顺序和key放入的顺序没有关系
#dict的key是不可变对象，list不能作为key

#set 数学意义上的无序和无重复元素的集合
s1=set([1,2,3])
print(s1) #{1,2,3} 
#创建一个set，需要提供一个list作为输入集合
s2=set([2,2,3,3,4,4]) 
print(s1) #{1,2,3} 重复元素在set中自动过滤
s2.add(5) #添加元素
s2.remove(5) #删除元素
s1&s2 #{2,3}
s1|s2 #{1,2,3,4}
#and 跟 & 不同. or 跟 | 不同
#set和dict原理一样，不可以放入可变对象


#不可变对象
#不可变类型(immutable)包含str,int,tuple；
#可变类型(mutable)包含list，dict

ts = zip(['A', 'B', 'C'], [1, 2, 3])
for t in ts:
	print(t)
#('A', 1)('B', 2)('C', 3)


#调用函数
def my_abs(x):
	if not isinstance(x,(int,float)):
		raise TypeError('bad operand type')
	#数据类型检查
	if x>=0:
		return x
	else :
		return -x
#如果没有return语句，返回结果为None

from abstest import my_abs

def nop():
	pass   #pass占位符

import math
def move(x,y,step,angle=0):
	nx=x+step*math.cos(angle)
	ny=y+step*math.sin(angle)
	return nx,ny
#返回多值是返回一个tuple

#作业
def qudratic():
	a=float(input('a='))
	b=float(input('b='))
	c=float(input('c='))
	d=b**2-4*a*c  #**为次方
	if a==0:
		return -c/b
	elif d>0:
		x1=(-b+math.sqrt(d))/(2*a)
		x2=(-b-math.sqrt(d))/(2*a)
		return x1,x2
	elif d==0:
		x0=(-b)/(2*a)
	else:
		return('no result') #return
print(qudratic())



#函数的参数 
#默认参数
def add_end(L=[]) #错误。L指向对象[]，是可变对象
#默认参数必须指向不变对象

#定义函数必须确定输入的参数
def calc(numbers): 
	pass
>>> calc([1, 2, 3]) #不确定的参数作为一个list或tuple传入
#可变参赛：*args 传入的参数个数是可变的
def calc(*numbers) ： #参数前加*变成可变参数
	pass 
>>> calc(1, 2, 3) >>> calc(1, 3, 5, 7) #可变参数
#可变参赛在函数调用时自动组装为一个tuple
>>> nums=[1,2,3]
>>> calc(*nums)   #list或tuple前加*，元素作为可变参数换入

#关键字参数 **kw
def person(name, **kw):
    print('name:', name, 'other:', kw)
>>> person('Bob',  city='Beijing')
name: Bob other: {'city': 'Beijing'}
 #关键字参数kw，在函数内部自动组装为一个dict
>>> extra = {'city': 'Beijing', 'job': 'Engineer'}
>>> person('Jack', **extra)
name: Jack other: {'city': 'Beijing', 'job': 'Engineer'}
#kw获得的dict是extra的一份拷贝
 
#命名关键字参数 * ：限制调用者可以传入的参数名，可提供默认值
def person(name, age, *, city, job):
    print(name, age, city, job)
# *后面的参数被视为命名关键字参数，缺少*则视为位置参数
>>> person('Jack', 24, city='Beijing', job='Engineer')
Jack 24 Beijing Engineer #正确
>>> person('Jack', 24, 'Beijing', 'Engineer')#错误
#必须传入参数名(不传入参数名则视为位置参数)
def person(name, age, *args, city, job):
    print(name, age, args, city, job)
#如果函数定义中已经有了一个可变参数，
#后面跟着的命名关键字参数就不再需要一个特殊分隔符*了
def person(name, age, *, city='Beijing', job):
    print(name, age, city, job)
>>> person('Jack', 24, job='Engineer')
Jack 24 Beijing Engineer
#命名关键字参数可以有缺省值，从而简化调用

#参数组合
#顺序：必选参数 默认参数 可变参数 命名关键字参数 关键字参数
def f1(a, b, c=0, *args, **kw):
    print('a =', a, 'b =', b, 'c =', c, 'args =', args, 'kw =', kw)
def f2(a, b, c=0, *, d, **kw):
    print('a =', a, 'b =', b, 'c =', c, 'd =', d, 'kw =', kw)
>>> args = (1, 2, 3, 4)
>>> kw = {'d': 99, 'x': '#'}
>>> f1(*args, **kw)
a = 1 b = 2 c = 3 args = (4,) kw = {'d': 99, 'x': '#'}
>>> args = (1, 2, 3)
>>> kw = {'d': 88, 'x': '#'}
>>> f2(*args, **kw)
a = 1 b = 2 c = 3 d = 88 kw = {'x': '#'}
#通过一个tuple和dict调用函数
#任意函数都可以通过类似func(*args, **kw)形式调用
#*args, **kw都是把tuple和dict里元素解压出来后一个萝卜一个坑



#递归函数  注意防止栈溢出
def fact(n):
    if n==1:
        return 1
    return n * fact(n - 1)
#引入乘法表达式，不是尾递归。
def fact(n):
	return fact_iter(n,1)
def fact_iter(num,product):
	if num=1:
		return product
	return fact_iter(num-1,num*product)
#num-1和mun*produ在函数调用前被计算
#尾递归：函数返回是调用本身，且return语句不能包含表达式
#尾递归调用时如果做了优化栈不会增长因此不会溢出
#Python标准的解释器没有针对尾递归做优化，存在栈溢出的问题
def  move(n,a,b,c):
	if n==1:
		print(a,'-->',c)
	else:
		move(n-1,a,c,b) #n－1个盘子从a移动到b上。a-->b
		print(a,'-->',c) #然后把最后一个盘子移动到c上。a-->c
		move(n-1,b,a,c) #然后把n－1个盘子从b移动到c上。b-->c
n=input('enter the number:')
move(int(n),'A','B','C')
#汉诺塔 A借助B移动到C



#切片
#L[x:y:z] 从x开始（包括x），y结束（不包括），间隔z
L = ['A', 'B', 'C','D','E']
L[0:3] #['A','B','C]
L[:3]  #['A','B','C]
L[-2:] #['D','E']
L[-2:-1]  #['D']
L[:10:2]  #前10个数，每两个取一个
L[::5]    #所有数，每5个取一个
L[:]      #复制list
(0,1,2,3,4,5)[:3] #(0,1,2)
'ABCDEFG'[::2] #'ACEG'
'ABCDEFG'[:1:-1] #GFEDC  
'ABCDEFG'[5:1:-1] #FEDC
'ABCDEFG'[5::-1] #FEDCBA
L2=L    #等同，指向同一list，内存保存的地址是同一个
L3=L[:] #copy，数值复制，对象不同，内存保存地址不同
In [1]: list1 = list('abcdefhijk')
In [2]: list1
Out[2]: ['a', 'b', 'c', 'd', 'e', 'f', 'h', 'i', 'j', 'k']
In [3]: list1[2:6] = [1,2]
In [4]: list1
Out[4]: ['a', 'b', 1, 2, 'h', 'i', 'j', 'k']



#迭代
d = {'a': 1, 'b': 2, 'c': 3}
for key in d #迭代key
for value in d.values() #迭代value
for k,v in d.items() #迭代key和value
for ch in 'ABC' #字符串也可迭代

#迭代索引和元素本身 
for i, value in enumerate(['A', 'B', 'C'])
#0 A 1 B 2 C #从0开始索引
for i, value in enumerate(['A', 'B', 'C'],1)
#1 A 2 B 3 C #从1开始索引
#enumerate函数可以把一个list变成索引-元素对

#判断对象是否可迭代
from collections import Iterable
isinstance('abc', Iterable) # str是否可迭代

for x, y in [(1, 1), (2, 4), (3, 9)] #引用两个变量

#题目
In[1]:
alist = [0, True, 1.5, 'list']
atuple = (0, 1,1.2, False, 'tuple')
aset = {0, 1.1, True, 'set'}
for first, *middle, last in (alist, atuple, aset):
    print('first=',first)
    print('middle=',middle)
    print('last=',last)
Out[1]:
first=0
middle=[True,1.5]
last=list
first=0
middle=[1,1.2,False]
last=tuple
first=0    #dict
middle=['set',1.1]
last=True  #第三组是乱序的
#python可以通过逗号解压一个序列



#列表生成式List Comprehensions
[x*x for x in range(1,11)]
[1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
#if判断
[x * x for x in range(1, 11) if x % 2 == 0]
[4, 16, 36, 64, 100]
#两层循环
[m + n for m in 'ABC' for n in 'XYZ']
['AX', 'AY', 'AZ', 'BX', 'BY', 'BZ', 'CX', 'CY', 'CZ']
#同时使用多个变量
d = {'x': 'A', 'y': 'B', 'z': 'C' }
[k + '=' + v for k, v in d.items()]
['y=B', 'x=A', 'z=C']



#generator 保存的是算法，一边循环一边计算
#生成器
g=(x*x for x in range(10)) 
next(g)  #逐个打印
for n in g:
	print(n)  #打印
#带yield的gennerator function
#斐波拉契数列（Fibonacci）
def fib(max):
    n, a, b = 0, 0, 1
    while n < max:
        yield b #普通函数这里为print(b)
        a, b = b, a + b
        n = n + 1
    return 'done'
#函数定义中包括yield关键字，则为generator
g=fib(6)
next(g)
#generator和函数的执行流程不一样
#顺序执行，遇到return语句或者最后一行函数语句就返回
#变成generator的函数调用next()的时候执行，遇到yield语句返回
#再次执行时从上次返回的yield语句处继续执行
for n in fib(6):
	print(n)
#遇到return语句或执行到最后一行函数语句，结束generator的指令
#for 循环调用generator时，拿不到return返回值
#返回值包含在StopIteration的value中
g=fib(6)
while True:
    try:
   	    x = next(g)
    	print('g:', x)
    except StopIteration as e:
        print('Generator return value:', e.value)
	    break

#普通函数调用直接返回结果
#generator函数的“调用”实际返回一个generator对象

#杨辉三角
def triangles():
    a,N=0,[1]
    while True:
        yield N
        N=[1]+[N[i]+N[i+1] for i in range(a)]+[1]
        a=a+1
n = 0
for t in triangles():
    print(t)
    n = n + 1
    if n == 10:
        break



#迭代器Iterator
#可迭代对象Iterable:可以直接作用于for循环的对象
#可迭代对象：list,tupl,dict,set,str; generator
#迭代器Iterator:可以被next()函数不断调用并返回下一值的对象
#迭代器Iterator 无法预先得知长度
#生成器是Iterator对象，list,tupl,dict,set,str不是
from collections import Iterable
isinstance([],Iterable) #判断对象是否是Iterable对象
isinstance(x for x in range(1,10) #判断是否Iterator对象
iter([]) #iter()把Iterable变成Iterator
#Python的for循环本质上就是通过不断调用next()函数实现的





#函数式编程

#高阶函数：一个函数接受另一个函数作为参数
#map
def f(x):
 	return x*x
r=map(f,[1,2,3,4,5])
#map()接受两个参数：函数和Iterable，
#将传入函数依次作用到序列每个元素，并把结果作为新的Iterator返回
#做题错了的：被传入记得return！否则结果为None
In[1]:print(r)
Out[1]:<map object at ...>  
In[2]:list(r) 
Out[2]:[1, 4, 9, 16, 25]
#r是Iterator是惰性序列，通过list()把整个n序列计算出来并返回list

#reduce
reduce(f, [x1, x2, x3, x4]) = f(f(f(x1, x2), x3), x4)
#函数必须接受两个参数
#字符串转化为整数
from functools import reduce
def char2num(s):
    return {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, 
    '6': 6, '7': 7, '8': 8, '9': 9}[s]
def str2int(s):
    return reduce(lambda x, y: x * 10 + y, map(char2num, s))

#filter 根据返回值决定保留还是丢弃元素
list(filter()) #获得结果并返回list
#过滤回数
def is_palindrome(n):
	return str(n)[::]==str(n)[::-1]
print(list(filter(is_palindrome,range(1,1000))))

#sorted
sorted([36, 5, -12, 9, -21], key=abs, reverse=True)
#key指定的函数作用于list的每个元素。映射函数




#返回函数
def lazy_sum(*args):
    def sum():
        ax = 0
        for n in args:
            ax = ax + n
        return ax
    return sum
f=lazy_sum(1,3,5,7,9)
In[1]:f    #(指向函数f)调用lazy_sum时，返回求和函数
Out[1]:<function lazy_sum.<locals>.sum at 0x101c6ed90>
In[2]:f()  #调用函数f时，计算求和结果
Out[2]:25
#返回的函数没有立刻执行，直到调用了f()才执行
#调用lazy_sum()时，每次调用返回新的函数
#闭包Closure 相关参数和变量都保存在返回的函数中
def count():
    fs = []
    for i in range(1, 4):
        def f():
             return i*i
        fs.append(f)
    return fs
f1, f2, f3 = count()
#count函数运行完后，fs=[f,f,f]
#f1, f2, f3 = count()相当于f1=f,f2=f,f3=f
#python赋值方式：a,b,c=[1,2,3]，a,b,c=(1,2,3)，a,b,c=1,2,3
In[1]:f1
Out[1]:<function count.<locals>.f at 0x001856F0>
In[2]:f1()
Out[2]:9
In[3]:f2()
Out[3]:9
In[4]:f3()
Out[4]:9
#fs.append(f)的f只是指针，不是函数，所以不执行
#返回函数引用了变量i，但并非立刻执行。3个函数都返回时i变成3
#闭包：返回函数不要引用任何循环变量或后续会发生变化的变量
def count():
    def f(j):
        def g():
            return j*j
        return g
    fs = []
    for i in range(1, 4):
        fs.append(f(i))
    # f(i)立刻被执行，因此i的当前值被传入f()
    return fs
In[1]:f1()
Out[1]:1
In[2]:f2()
Out[2]:4
In[3]:f3()
Out[3]:9
#闭包的返回值是函数而不是函数计算后的返回值(函数指向函数调用)
def count():
    def f(j):
        return j*j
    fs = []
    for i in range(1, 4):
        fs.append(f(i))
    return fs  #这不是闭包
#return的list是元素是整数的list而不是元素是函数引用地址的list
#等同于：
def count():
	return[i*i for i in rang(1,4)]

#上面例子的lambda写法：
def count():
    return [lambda: i*i for i in range(1, 4)]
f1, f2, f3 = count()
print(f1()) # 9
print(f2()) # 9
print(f3()) # 9

def count2():
    # 用i=i来绑定循环变量的传值
    return [lambda i=i: i*i for i in range(1, 4)]
    #i是默认值，for循环在调用函数前调用并生成默认值，
g1, g2, g3 = count2()
print(g1()) # 1
print(g2()) # 4
print(g3()) # 9




#匿名函数
lambda x:x*x #冒号前面的x表示函数参数，冒号后面相当于返回值
#等同于：
def f(x):
	return x*x 

f=lambda x:x*x #匿名函数赋值给对象
In[1]:f #指向函数
Out[1]:<function <lambda> at 0x101c6ef28>
In[2]:f(5)  #利用变量调用函数
Out[2]:25

f=lambda:[x%2==0 for x in range(10)]
In[1]:print(f())
Out[1]:[True,False,...]  #返回list类型



#装饰器Decorator 代码运行期间动态增加功能
#接受一个函数作为参数并返回一个函数
import functools  #导入functools模块
def log(func):   #两层嵌套
    @functools.wraps(func) #原始函数性质复制
    def wrapper(*args, **kw):
        print('call %s():' % func.__name__)
        return func(*args, **kw)
    return wrapper
@log   #相当于执行now=log(now)
def now():  
    print('2015-3-25')
In[1]:now()
Out[1]:call now():
   ....2015-3-25

import functools
def log(text):   #三层嵌套
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            print('%s %s():' % (text, func.__name__))
            return func(*args, **kw)
        return wrapper
    return decorator
@log('execute') #now = log('execute')(now)
def now():
    print('2015-3-25')
In[1]:now()
Out[1]:execute now():
   ....2015-3-25

#
from collections import Iterable
import functools

#同时支持两种情况
def log(text):
    def decorator(func=text):       #默认参数为函数名???
        @functools.wraps(func)
        def wrapper(*args, **kw):
            if isinstance(text, Iterable): 
                print(r'@log(%s)' % text)
                for item in text:
                    print(item)
            else:
                print('@log')
            func(*args, **kw)
            return 
        return wrapper
    if isinstance(text, Iterable):
        return decorator
    else:
        return decorator(text)   
    #以@log 装饰时，少了一次调用，所以返回decorator(text)



#偏函数Partial function
#设置默认参数，仍能改变其值
import functools
int2=functools.partial(int,base=2) 
#偏函数可以接收函数对象，*args,**kw三个参数
int2('10010') #相当于
kw={'base':2}
int('10010',**kw)
max2 = functools.partial(max, 10)
max2(5, 6, 7) #相当于
args = (10, 5, 6, 7)
max(*args)



