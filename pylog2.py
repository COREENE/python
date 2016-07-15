#笔记2之函数式编程

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






