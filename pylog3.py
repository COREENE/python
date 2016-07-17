#python 学习笔记3之IO编程,线程和进程

#IO编程（同步模式）
#打开文件、读文件、关闭文件的典型方法
try:
    f = open('/path/to/file', 'r') #标示符'r'表示读
    print(f.read())
finally:  #保证无论是否出错都能正确关闭文件
    if f:
        f.close()
#推荐的简洁写法，不必显示的关闭文件描述符
with open('/path/to/file', 'r') as f:
    print(f.read())

read(size) #每次最多读取size个字节内容
readline() #每次读取一行内容
readlines() #一次读取所有内容并按行返回list
for line in f.readlines():
    print(line.strip()) # 把末尾的'\n'删掉

#file-like Object(open返回的对象):字节流、网络流、自定义流等
#StringIO就是在内存中创建的file-like Object，常用作临时缓冲

>>> f = open('/Users/michael/test.jpg', 'rb')
#读取二进制文件，比如图片、视频等等，用'rb'模式打开文件
>>> f = open('/Users/michael/gbk.txt', 'r', encoding='gbk')
#读取非UTF-8编码的文本文件，需要给open()函数传入encoding参数
>>> f = open('/Users/michael/gbk.txt', 'r', encoding='gbk', errors='ignore')
#errors参数，表示如果遇到编码错误后如何处理
f = open('/Users/michael/test.txt', 'w')
f.write('Hello, world!')
f.close() #忘记调用close()数据可能丢失
#写文件。传入标识符'w'或者'wb'表示写文本文件或写二进制文件
with open('/Users/michael/test.txt', 'w') as f:
    f.write('Hello, world!')
#with语句更保险
#要写入特定编码的文本文件，需给open()函数传入encoding参数
#要么用'r'要么用'w'，不要同时读写，代码会很乱
'r'    open for reading (default)
'w'    open for writing, truncating the file first
'x'    open for exclusive creation, failing if the file already exists
'a'    open for writing, appending to the end of the file if it exists
'b'    binary mode
't'    text mode (default)
'+'    open a disk file for updating (reading and writing)
'U'    universal newlines mode (deprecated)
with open('D:/test12.txt','a+') as f4:
    for line in f4.readlines():
        print(line.strip())
    f4.write('a new line2!')


#StringIO和BytesIO 在内存中读写
>>> from io import StringIO
>>> f = StringIO()
>>> f.write('hello')
5
>>> f.write(' ')
1
>>> f.write('world!')
6
>>> print(f.getvalue()) #getvalue()方法用于获得写入后的str
hello world!
#读取StringIO，可以用一个str初始化StringIO，然后像读文件一样读取
>>> from io import StringIO
>>> f = StringIO('Hello!\nHi!\nGoodbye!')
>>> while True:
...     s = f.readline()
...     if s == '':
...         break
...     print(s.strip())
...
Hello!
Hi!
Goodbye!

#使用BytesIO操作二进制数据
>>> from io import BytesIO
>>> f = BytesIO()
>>> f.write('中文'.encode('utf-8'))
6
>>> print(f.getvalue())
b'\xe4\xb8\xad\xe6\x96\x87'
#写入的不是str，而是经过UTF-8编码的bytes
#读取BytesIO.用一个bytes初始化BytesIO，然后，像读文件一样读取
>>> from io import BytesIO
>>> f = BytesIO(b'\xe4\xb8\xad\xe6\x96\x87')
>>> f.read()
b'\xe4\xb8\xad\xe6\x96\x87'

#f.read()是会从你设定(或者默认)的position开始读取数据
#f.getvalue()会返回当前存储的数据

#the stream position
d = StringIO('Hello World')#stream position为0（d.tell()获得）
d.readline()#返回'Hello World'。stream position移动到11
f = StringIO() #stream position为0
f.write('Hello World')#stream position移动到11
f.seek(0) #调整stream position到0
f.readline() #返回'Hello World'


#操作文件和目录
>>> import os
>>> os.name # 操作系统类型
>>> os.environ
>>> os.environ.get('PATH') #获取某个环境变量的值
>>> os.environ.get('x', 'default')

# 查看当前目录的绝对路径:
>>> os.path.abspath('.')
'/Users/michael'
# 在某个目录下创建一个新目录，首先把新目录的完整路径表示出来:
>>> os.path.join('/Users/michael', 'testdir')
'/Users/michael/testdir'
# 然后创建一个目录:
>>> os.mkdir('/Users/michael/testdir')
# 删掉一个目录:
>>> os.rmdir('/Users/michael/testdir')
#合并、拆分路径的函数不要求目录和文件要真实存在，只对字符串进行操作
>>> os.path.split('/Users/michael/testdir/file.txt')
('/Users/michael/testdir', 'file.txt')
# 对文件重命名:
>>> os.rename('test.txt', 'test.py')
# 删掉文件:
>>> os.remove('test.py')
#列出当前目录下的所有目录
>>> [x for x in os.listdir('.') if os.path.isdir(x)]
['.git','__pycache__']
#列出所有的.py文件
>>> [x for x in os.listdir('.') if os.path.isfile(x) and os.path.splitext(x)[1]=='.py']
['online.py','print.py','pylog1.py','pylog2.py','pylog3.py']


#序列化 picking 把变量从内存中变成可存储或传输的过程
#反序列化 unpickling 把变量内容从序列化的对象重新读到内存里
>>> import pickle
>>> d = dict(name='Bob', age=20, score=88)
>>> pickle.dumps(d) #pickle.dumps()方法把任意对象序列化成一个bytes
b'\x80\x03}q\x00(X\x03\x00...'#然后，就可以把这个bytes写入文件;
#另一种方法：pickle.dump()直接把对象序列化后写入一个file-like Object：
>>> f = open('dump.txt', 'wb') 
>>> pickle.dump(d, f) 
>>> f.close()
#把对象从磁盘读到内存：
>>> f = open('dump.txt', 'rb') 
>>> d = pickle.load(f) #从一个file-like Object中直接反序列化出对象
>>> f.close()
>>> d
{'age': 20, 'score': 88, 'name': 'Bob'}
#也可以先把内容读到一个bytes，然后用pickle.loads()方法反序列化出对象
#Pickle只能用于Python，并且可能不同版本的Python彼此都不兼容

#JSON 序列化标准格式
#把Python对象变成一个JSON：
>>> import json
>>> d = dict(name='Bob', age=20, score=88)
>>> json.dumps(d) #dumps()方法返回一个str，内容就是标准的JSON
'{"age": 20, "score": 88, "name": "Bob"}'
#dump()方法可以直接把JSON写入一个file-like Object
#把JSON反序列化为Python对象：
>>> json_str = '{"age": 20, "score": 88, "name": "Bob"}'
>>> json.loads(json_str) #把JSON的字符串反序列化
{'age': 20, 'score': 88, 'name': 'Bob'}
#load()从file-like Object中读取字符串并反序列化

#JSON进阶  传入更多的参数定制序列化或反序列化的规则
#把Student类实例序列化为JSON
import json
class Student(object):
    def __init__(self, name, age, score):
        self.name = name
        self.age = age
        self.score = score
s = Student('Bob', 20, 88)
def student2dict(std):  #Student的转换函数
    return {
        'name': std.name,
        'age': std.age,
        'score': std.score
    }
>>> print(json.dumps(s, default=student2dict))
{"age": 20, "name": "Bob", "score": 88}
#可选参数default就是把任意一个对象变成一个可序列为JSON的对象
#Student实例首先被student2dict()函数转换成dict，再被顺利序列化为JSON

#简化:把任意class的实例变为dict：
print(json.dumps(s, default=lambda obj: obj.__dict__))

#把JSON反序列化为一个Student对象实例
def dict2student(d):
    return Student(d['name'], d['age'], d['score'])
>>> json_str = '{"age": 20, "score": 88, "name": "Bob"}'
>>> print(json.loads(json_str, object_hook=dict2student))
<__main__.Student object at 0x10cd3c190>
#loads()转换出一个dict对象，传入的object_hook函数把dict转换为Student实例




#进程Process（任务）和线程Thread(进程的“子任务”)
#线程是最小的执行单元，而进程由至少一个线程组成

#fork() 父进程自动创建子进程,一个父进程可以fork出很多子进程
import os
print('Process (%s) start...' % os.getpid())#getppid()拿到父进程的ID
# Only works on Unix/Linux/Mac:
pid = os.fork() #fork()系统调用，
if pid == 0:  #子进程永远返回0，而父进程返回子进程的ID
    print('I am child process (%s) and my parent is %s.' % (os.getpid(), os.getppid()))
else:
    print('I (%s) just created a child process (%s).' % (os.getpid(), pid))
#有了fork调用，一个进程在接到新任务时就可以复制出一个子进程来处理新任务

#multiprocessing
from multiprocessing import Process #Process类来代表一个进程对象
import os
# 子进程要执行的代码
def run_proc(name):
    print('Run child process %s (%s)...' % (name, os.getpid()))
if __name__=='__main__':
    print('Parent process %s.' % os.getpid())
    p = Process(target=run_proc, args=('test',))
    print('Child process will start.')
    p.start()
    p.join() #join()方法可以等待子进程结束后再继续往下运行，通常用于进程间的同步

#Pool 批量创建子进程
from multiprocessing import Pool
import os, time, random
def long_time_task(name):
    print('Run task %s (%s)...' % (name, os.getpid()))
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    print('Task %s runs %0.2f seconds.' % (name, (end - start)))
if __name__=='__main__':
    print('Parent process %s.' % os.getpid())
    p = Pool(4)
    for i in range(5):
        p.apply_async(long_time_task, args=(i,))
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    print('All subprocesses done.')
#执行结果
Parent process 669.
Waiting for all subprocesses done...
Run task 0 (671)...
Run task 1 (672)...
Run task 2 (673)...
Run task 3 (674)...
Task 2 runs 0.14 seconds.
Run task 4 (673)...
Task 1 runs 0.27 seconds.
Task 3 runs 0.86 seconds.
Task 0 runs 1.41 seconds.
Task 4 runs 1.91 seconds.
All subprocesses done.
#对Pool对象调用join()方法会等待所有子进程执行完毕，
#调用join()之前必须先调用close()，调用close()之后不能继续添加新的Process
p = Pool(5) #修改Pool的大小，最多执行5个进程。Pool的默认大小是CPU的核数

#子进程














