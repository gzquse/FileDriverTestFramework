# -*- coding:utf-8 -*-
"""
主控函数调用测试文件并执行
# 需要安装如下库
1: pymysql==0.10.1
2: requests==2.26.0
3: xlrd==1.2.0
4: xlwt==1.3.0
"""
from commons.TestRunner import TestRunner

runner = TestRunner("TestFiles/演示测试文件.xlsx", "Sniper.ZH")
runner.do_runner()
