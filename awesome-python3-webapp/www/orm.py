#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Coreene Wong'

import asyncio, logging

import aiomysql

# 记录操作日志
def log(sql, args=()):
    logging.info('SQL: %s' % sql)

#创建连接池，(应用服务器和数据库) 每个HTTP请求都可以从连接池中直接获取数据库连接。
#不必频繁地打开和关闭数据库连接
async def create_pool(loop, **kw):
    logging.info('create database connection pool...')
    global __pool  #声明全局变量
    # 调用一个子协程来创建全局连接池，create_pool返回一个pool实例对象
    __pool = await aiomysql.create_pool(
        # 连接的基本属性设置
    	# kw应该就是create_pool函数的参数**kw，也就是关键字参数
        host=kw.get('host', 'localhost'), # 数据库服务器位置，本地
        port=kw.get('port', 3306), # MySQL端口号
        user=kw['user'],# 登录用户名
        password=kw['password'], # 登录密码
        db=kw['db'],# 数据库名
        charset=kw.get('charset', 'utf8'),# 设置连接使用的编码格式utf-8
        autocommit=kw.get('autocommit', True),# 是否自动提交，默认false
        maxsize=kw.get('maxsize', 10),# 最大连接池大小，默认10
        minsize=kw.get('minsize', 1), # 最小连接池大小，默认1
        loop=loop # 设置消息循环
    )

#将执行sql的代码封装进select函数，调用的时候只要传入sql，和sql需要的一些参数值就好
#select从表中选取数据，结果被存储在一个结果表中（称为结果集）
async def select(sql, args, size=None): 
    # sql：sql语句， 这个sql中的values的内容使用占位符%s表示
    # args：填入sql的参数,list类型，如['20111101','xue']
    # size:取多少行记录
    log(sql, args) 
    global __pool # 从连接池中获取一个连接
    async with __pool.get() as conn: # with...as...的作用就是try...exception...
        async with conn.cursor(aiomysql.DictCursor) as cur:
        # 打开一个DictCursor，以dict形式返回结果的游标
        # cur = conn.cursor()获取对应的操作游标,才能进行数据库的操作
            await cur.execute(sql.replace('?', '%s'), args or ())
            # sql.replace的作用是把sql中的字符串占位符？换成python的占位符%s，
            # 使用带参数的sql，而不是自己拼接sql字符串(纯sql语句)，这样可以防止SQL注入攻击
            # args是执行sql语句时通过占位符插入的一些参数，()表示一个空的tuple
            if size: # 如果size不为空，则取一定量的结果集
                rs = await cur.fetchmany(size)
            else:
                rs = await cur.fetchall()
        logging.info('rows returned: %s' % len(rs))
        return rs #返回查询结果

#操作数据库
async def execute(sql, args, autocommit=True):
    log(sql)
    async with __pool.get() as conn:
        if not autocommit:
            await conn.begin()
        try:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(sql.replace('?', '%s'), args)  #写入数据
                affected = cur.rowcount #返回执行的sql 影响的行数
            if not autocommit:
                await conn.commit() #commit():提交当前事务
        except BaseException as e:
            if not autocommit:
                await conn.rollback() #rollback():取消当前事务
            raise
        return affected

# 该方法用来将其占位符拼接起来成'?,?,?'的形式，num表示为参数的个数
def create_args_string(num):
    L = []
    for n in range(num):
        L.append('?')
    return ', '.join(L)

# 父域 定义字段基类
class Field(object):

    def __init__(self, name, column_type, primary_key, default):
        self.name = name               #字段名
        self.column_type = column_type #字段列类型 
        self.primary_key = primary_key #主键
        self.default = default         #默认值
    #为了在命令行按照'<%s, %s:%s>'这个格式输出字段的相关信息

    def __str__(self):
        return '<%s, %s:%s>' % (self.__class__.__name__, self.column_type,self.name)

# 字符串域。映射varchar
class StringField(Field):

    def __init__(self, name=None, primary_key=False, default=None, ddl='varchar(100)'):
    #ddl是数据定义语言("data definition languages")，默认值是'varchar(100)'，意思是可变字符串，长度为100
    #和char相对应，char是固定长度，字符串长度不够会自动补齐，varchar则是多长就是多长，但最长不能超过规定长度
        super().__init__(name, ddl, primary_key, default) #super()调用父类方法

# 布尔域，映射boolean
class BooleanField(Field):

    def __init__(self, name=None, default=False):
        super().__init__(name, 'boolean', False, default)

# 整型域，映射Integer
class IntegerField(Field):

    def __init__(self, name=None, primary_key=False, default=0):
        super().__init__(name, 'bigint', primary_key, default)

# 浮点数域
class FloatField(Field):

    def __init__(self, name=None, primary_key=False, default=0.0):
        super().__init__(name, 'real', primary_key, default)

# 文本域
class TextField(Field):

    def __init__(self, name=None, default=None):
        super().__init__(name, 'text', False, default)

# 将具体的子类如User的映射信息读取出来
class ModelMetaclass(type): #详见元类

    def __new__(cls, name, bases, attrs): 
        # cls: 当前准备创建的类对象,相当于self
        # name: 类名,比如User继承自Model,当使用该元类创建User类时,name=User
        # bases: 父类的元组
        # attrs: Model子类的属性和方法的字典,比如User有__table__,id,等,就作为attrs的keys
        # 排除Model类本身：
        if name=='Model':
            return type.__new__(cls, name, bases, attrs) #元类对Model不操作
        tableName = attrs.get('__table__', None) or name 
        # 获取table名称，若没有定义__table__属性,将类名作为表名
        logging.info('found model: %s (table: %s)' % (name, tableName))
        # 获取所有的Field和主键名:        
        mappings = dict() # 用字典来存储类属性与数据库表的列的映射关系
        fields = []       # 用于保存除主键以外的属性
        primaryKey = None # 用于保存主键
        # attrs是User类的属性集合，是一个dict，需要通过items函数转换为[(k1,v1),(k2,v2)]这种形式，才能用for k, v in来循环
        # k是属性名，v是定义域。如name=StringField(ddl="varchar50"),k=name,v=StringField(ddl="varchar50")
        for k, v in attrs.items():
            if isinstance(v, Field):
                logging.info('  found mapping: %s ==> %s' % (k, v))
                mappings[k] = v   
                # 找到主键:
                if v.primary_key:    
                    if primaryKey:   # 主键已存在，报错，不可能俩主键
                        raise StandardError('Duplicate primary key for field: %s' % k) 
                    primaryKey = k # 主键赋值
                else:
                    fields.append(k) # 不是主键的属性名储存到非主键字段名的list中
        # 没找到主键报错
        if not primaryKey: 
            raise StandardError('Primary key not found.')
        # 从类属性中删除已经加入了映射字典的键，以免重名：
        for k in mappings.keys():
            attrs.pop(k)   
        # 将非主键的属性变形,放入escaped_fields中,方便增删改查语句的书写
        # fields中的值都是字符串，下面这个匿名函数的作用是在字符串两边加上``生成一个新的字符串，为了后面生成sql语句做准备
        escaped_fields = list(map(lambda f: '`%s`' % f, fields))
        attrs['__mappings__'] = mappings # 保存属性和列的映射关系
        attrs['__table__'] = tableName
        attrs['__primary_key__'] = primaryKey # 主键属性名
        attrs['__fields__'] = fields # 除主键外的属性名
        attrs['__select__'] = 'select `%s`, %s from `%s`' % (primaryKey, ', '.join(escaped_fields), tableName)
        attrs['__insert__'] = 'insert into `%s` (%s, `%s`) values (%s)' % (tableName, ', '.join(escaped_fields), primaryKey, create_args_string(len(escaped_fields) + 1))
        attrs['__update__'] = 'update `%s` set %s where `%s`=?' % (tableName, ', '.join(map(lambda f: '`%s`=?' % (mappings.get(f).name or f), fields)), primaryKey)
        attrs['__delete__'] = 'delete from `%s` where `%s`=?' % (tableName, primaryKey)
        return type.__new__(cls, name, bases, attrs) 
        #将操作后的参数传入自己(元类会自动将你通常传给‘type’的参数作为自己的参数传入)

#到这儿可以总结一下元类到底干了些什么，还是以User类为例
#首先、元类找出User类在数据库中对应的表名，对User类的自有属性逐条进行分析，找出主键和非主键，同时把这些属性全部存入mappings这个dict
#然后、删除User类的全部属性，因为实际操作数据库的时候用不到这些属性
#最后、把操作数据库需要用到的属性添加进去，这包括所有字段和字段类型的对应关系，类对应的表名、主键名、非主键名，还有四句sql语句
#这些属性才是操作数据库正真需要用到的属性，但仅仅只有这些属性还是不够，因为没有方法
#而Model类就提供了操作数据库要用到的方法


# 所有ORM映射的基类，继承自dict，通过ModelMetaclass元类来构造类
class Model(dict, metaclass=ModelMetaclass): #抽象类
   
    # 初始化函数,调用其父类(dict)的方法，把传入的关键字参数**kw存入自身的dict中
    def __init__(self, **kw):
        super(Model, self).__init__(**kw) 

    # 增加__getattr__方法,使获取属性更方便,即可通过"a.b"的形式       
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)

    # 增加__setattr__方法,使设置属性更方便,可通过"a.b=c"的形式
    def __setattr__(self, key, value):
        self[key] = value

    # 通过键取值,若值不存在,返回None
    def getValue(self, key):
        return getattr(self, key, None)   # 如果没有与key相对应的属性值则返回None
    
    # 通过键取值,若值不存在,则返回默认值
    # 这招很妙！
    def getValueOrDefault(self, key):
        value = getattr(self, key, None)
        if value is None:
            field = self.__mappings__[key]  # field是一个定义域!比如FloatField
            if field.default is not None:
                # id的StringField.default=next_id,因此调用该函数生成独立id。实现自增
                # FloatFiled.default=time.time数,因此调用time.time函数返回当前时间。当前时间做id
                # 普通属性的StringField默认为None,因此还是返回None
                value = field.default() if callable(field.default) else field.default
                # 当前实例找不到想要的属性值时，就要到__mappings__属性中去找了
                logging.debug('using default value for %s: %s' % (key, str(value)))
                # 通过default取到值之后再将其作为当前值
                setattr(self, key, value)
        return value

 

    # classmethod，装饰器，定义该方法为类方法，必备参数为cls(类似于self);staticmethod,可以不传任何参数;其他的方法，必备参数self
    @classmethod #这个装饰器是类方法的意思，这样就可以不创建实例直接调用类的方法
    async def findAll(cls, where=None, args=None, **kw):
        # cls表示当前类或类的对象可调用该方法，where表示sql中的where，args记录下所有的需要用占位符'?'的参数
        # **kw是一个tuple，里面有多个dict键值对，如{'name',Mary} 多为筛选条件
        ' find objects by where clause. ' # 通过条件来查询对象，一个对象对应数据库表中的一行
        sql = [cls.__select__]
        # 我们定义的默认的select语句并不包括where子句
        # 因此若指定有where,需要在select语句中追加关键字
        if where: 
            sql.append('where')
            sql.append(where)
        if args is None:
            args = []
        orderBy = kw.get('orderBy', None)  # 从**kw中取得orderBy的值，没有就默认为None
        if orderBy:
            sql.append('order by')
            sql.append(orderBy)
        limit = kw.get('limit', None)    
        if limit is not None:
            sql.append('limit')      
            # sql中limit有两种用法：
            if isinstance(limit, int): # 如果是一个整型数，直接在sql语句的limit字段后添加占位符'?'
                sql.append('?')
                args.append(limit)
            elif isinstance(limit, tuple) and len(limit) == 2:
            #如果limit为一个两个值的tuple，则前一个值代表索引，后一个值代表从这个索引开始要取的结果数
                sql.append('?, ?')
                args.extend(limit) # 用extend是为了把tuple的小括号去掉，因为args传参的时候不能包含tuple
            else:
                raise ValueError('Invalid limit value: %s' % str(limit))
        # ''.join(list/tuple/dict)   "|".join(['a','b','c']) -> 'a|b|c'  
        rs = await select(' '.join(sql), args) # 转list为str.
        return [cls(**r) for r in rs] # cls(**r)调用本类的__init__(方法)

    # 查找某列
    @classmethod
    async def findNumber(cls, selectField, where=None, args=None):
        ' find number by select and where. ' 
        sql = ['select %s _num_ from `%s`' % (selectField, cls.__table__)]
        if where:
            sql.append('where')
            sql.append(where)
        rs = await select(' '.join(sql), args, 1)
        if len(rs) == 0:
            return None
        return rs[0]['_num_']

    # 按主键查找
    @classmethod
    async def find(cls, pk):
        ' find object by primary key. '
        rs = await select('%s where `%s`=?' % (cls.__select__, cls.__primary_key__), [pk], 1)
        if len(rs) == 0:
            return None
        # 注意,我们在select函数中,打开的是DictCursor,它会以dict的形式返回结果
        return cls(**rs[0])

    # save、update、remove这三个方法需要管理员权限才能操作，所以不定义为类方法，需要创建实例之后才能调用
    async def save(self):
        # 我们在定义__insert__时,将主键放在了末尾.因为属性与值要一一对应,因此通过append的方式将主键加在最后
        # 使用getValueOrDefault方法,可以调用time.time这样的函数来获取值
        args = list(map(self.getValueOrDefault, self.__fields__))
        # 把实例的非关键字属性值全都查出来然后存入args这个list
        args.append(self.getValueOrDefault(self.__primary_key__)) # 把主键找出来加到args这个list的最后
        rows = await execute(self.__insert__, args) # 执行sql语句后返回影响的结果行数
        print('返回行数：',rows)
        if rows != 1: # 一个实例只能插入一行数据，所以返回的影响行数一定为1,如果不为1那就肯定错了
            logging.warn('failed to insert record: affected rows: %s' % rows)

    async def update(self):
        # 像time.time,next_id之类的函数在插入的时候已经调用过了,没有其他需要实时更新的值,因此调用getValue
        args = list(map(self.getValue, self.__fields__))
        args.append(self.getValue(self.__primary_key__))
        rows = await execute(self.__update__, args)
        print('更新成功！')
        if rows != 1:
            logging.warn('failed to update by primary key: affected rows: %s' % rows)

    async def remove(self):
        args = [self.getValue(self.__primary_key__)] # 取得主键作为参数
        rows = await execute(self.__delete__, args)
        print('删除成功！')
        if rows != 1:
            logging.warn('failed to remove by primary key: affected rows: %s' % rows)
