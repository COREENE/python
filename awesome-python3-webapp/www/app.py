#!/usr/bin/env python3
#-*- coding: utf-8 -*-

__author__= 'Coreene Wong'

'''
async web applicatiion.
'''

import logging; logging.basicConfig(level=logging.INFO) #打印日志
import asyncio, os, json, time
from datetime import datetime
from aiohttp import web

def index(request):
	return web.Response(body=b'<h1>Awesome</h1>')

@asyncio.coroutine
def init(loop):
	app = web.Application(loop=loop) #创建web服务器实例 
	#loop: event loop used for processing HTTP requests
	app.router.add_route('GET','/',index) #为route路径注册处理函数
	srv = yield from loop.create_server(app.make_handler(),'127.0.0.1',9000)
	return srv

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()

