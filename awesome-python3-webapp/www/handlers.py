#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao'

' url handlers '

import re, time, json, logging, hashlib, base64, asyncio

from coroweb import get, post # 导入装饰器,这样就能很方便的生成request handler

from models import User, Comment, Blog, next_id

# 此处所列所有的handler都会在app.py中通过add_routes自动注册到app.router上
# 因此,在此脚本尽情地书写request handler即可

# 对于首页的get请求的处理
@get('/')
async def index(request):
    users = await User.findAll()
    return {
        '__template__': 'test.html', 
        'users': users
        #'__template__'指定的模板文件是test.html，其他参数是传递给模板的数据
    }