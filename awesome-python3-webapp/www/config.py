#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Configuration
'''

__author__ = 'Coreene Wong'

import config_default #导入默认配置

# 这个类主要可以使dict对象，以object.key 形式来替代  object[key]来取值
class Dict(dict): 
    '''
    Simple dict but support access as x.y style.
    '''
    def __init__(self, names=(), values=(), **kw):
        super(Dict, self).__init__(**kw) 
        for k, v in zip(names, values): 
            self[k] = v

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

def merge(defaults, override): # 融合默认配置和自定义配置
    r = {}
    for k, v in defaults.items():
        if k in override:
            if isinstance(v, dict):
                r[k] = merge(v, override[k])
            else:
                r[k] = override[k]
        else:
            r[k] = v
    return r

# 把配置文件转换为Dict类实例
def toDict(d):
    D = Dict()
    #假如值本身就是一个dict，那就把这个值交给toDict处理，然后再存入Dict
    for k, v in d.items():
        D[k] = toDict(v) if isinstance(v, dict) else v
    return D
configs = config_default.configs

try:
    import config_override
    # 这里把自定义配置文件里的配置项覆盖了默认配置里的配置项，
    # 如果自定义配置里没有定义，默认配置定义了，则还是沿用默认配置
    configs = merge(configs, config_override.configs)
except ImportError:
    pass

configs = toDict(configs)