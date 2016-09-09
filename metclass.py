metclass 元类

python中一切皆对象,它们要么是类的实例，要么是元类的实例，除了type,type实际上是它自己的元类.
str 是用来创建字符串对象的类
int 是用来创建证书对象的类
metclass(type) 是用来创建类的类 

type动态创建类 (type是python的内建元类)：
type(类名，父类的元祖(可为空)，包含属性的字典(名称和值))

#__metclass__属性
class Foo(object):
	__metclass__ = something... #添加__metclass__属性
[...]

'''创建过程：首先写下class Foo(object)，但是类对象Foo还没有在内存中创建。
python在类的定义(寻找顺序：类->父类 ->模块层次)中寻找__metclass__属性,如果找到了，python就会用它来创建类Foo，
如果没有找到，就会用内建的type来创建这个类'''


#自定义元类
'''元类：1)拦截类的创建;  2)修改类;  3)返回修改之后的类'''
'''元类的目的：创建类时能够自动改变类，创建符合当前上下文的类。(如API)
如：在模块级别设置 __metclass__ ，使模块内所有类的属性是大写形式。'''


例：
# 元类会自动将你通常传给‘type’的参数作为自己的参数传入
def upper_attr(future_class_name, future_class_parents, future_class_attr):
    # 返回一个类对象，将属性都转为大写形式
    # 选择所有不以'__'开头的属性
    attrs = ((name, value) for name, value in future_class_attr.items() if not name.startswith('__'))
    # 将它们转为大写形式
    uppercase_attr = dict((name.upper(), value) for name, value in attrs)
    
    # 通过'type'来做类对象的创建
    return type(future_class_name, future_class_parents, uppercase_attr)
 
__metaclass__ = upper_attr  #  这会作用到这个模块中的所有类
 
class Foo(object):
    # 我们也可以只在这里定义__metaclass__，这样就只会作用于这个类中
    bar = 'bip'

print hasattr(Foo, 'bar')
# 输出: False
print hasattr(Foo, 'BAR')
# 输出:True
f = Foo()
print f.BAR
# 输出:'bip'

例：
# 请记住，'type'实际上是一个类，就像'str'和'int'一样
# 所以，你可以从type继承
class UpperAttrMetaClass(type):
    # __new__ 是在__init__之前被调用的特殊方法
    # __new__ 是用来创建对象并返回之的方法
    # 而__init__只是用来将传入的参数初始化给对象
    # 你很少用到__new__，除非你希望能够控制对象的创建
    # 这里，创建的对象是类，我们希望能够自定义它，所以我们这里改写__new__
    # 如果你希望的话，你也可以在__init__中做些事情
    # 还有一些高级的用法会涉及到改写__call__特殊方法，但是我们这里不用
    def __new__(upperattr_metaclass, future_class_name, future_class_parents, future_class_attr):
        attrs = ((name, value) for name, value in future_class_attr.items() if not name.startswith('__'))
        uppercase_attr = dict((name.upper(), value) for name, value in attrs)
        return type(future_class_name, future_class_parents, uppercase_attr)

但是，这种方式其实不是OOP。我们直接调用了type，而且我们没有改写父类的__new__方法。
现在让我们这样去处理:

class UpperAttrMetaclass(type):
    def __new__(upperattr_metaclass, future_class_name, future_class_parents, future_class_attr):
        attrs = ((name, value) for name, value in future_class_attr.items() if not name.startswith('__'))
        uppercase_attr = dict((name.upper(), value) for name, value in attrs)
 
        # 复用type.__new__方法
        # 这就是基本的OOP编程，没什么魔法
        return type.__new__(upperattr_metaclass, future_class_name, future_class_parents, uppercase_attr)

使用super方法的话，我们还可以使它变得更清晰一些，这会缓解继承（是的，你可以拥有元类，从元类继承，从type继承）

class UpperAttrMetaclass(type):
    def __new__(cls, name, bases, dct): #通常写法是 cls, name, bases, dct
        attrs = ((name, value) for name, value in dct.items() if not name.startswith('__'))
        uppercase_attr = dict((name.upper(), value) for name, value in attrs)
        return super(UpperAttrMetaclass, cls).__new__(cls, name, bases, uppercase_attr)