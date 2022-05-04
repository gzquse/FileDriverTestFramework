# -*- coding:utf-8 -*-
"""
  所有断言方法的父类
  定义成员变量
"""


class SuperAsert:
    def __init__(self, url, params, dba):
        self.url = url
        self.params = params
        self.dba = dba
