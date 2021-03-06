#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Coreene Wong'

import orm
import asyncio
import sys
from models import User, Blog, Comment

@asyncio.coroutine
def test(loop):
    yield from orm.create_pool(loop=loop, user='www-data', password='www-data', db='awesome')
    u = User(name='test78',email='test77@test.com',passwd='test',image='about:blank')
    yield from u.save()

loop = asyncio.get_event_loop()
loop.run_until_complete(test(loop))
loop.close()     
if loop.is_closed(): #在loop.close()这句代码后，程序还会循环运行
    sys.exit(0)