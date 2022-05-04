# -*- coding:utf-8 -*-
"""
需求查询列表断言类
"""
import json
from commons.SuperAsert import SuperAsert


class asserts(SuperAsert):
    """需求列表功能断言类"""

    def asert_1(self, response):
        if response.status_code == 200:
            # print(response.text)
            res = json.loads(response.text)
            if res['code'] == 0:
                # 通过数据库验证结果
                orderCount = self.dba.dbQueryOne("select count(*) from order_info where status='0'")
                if res['count'] == orderCount[0]:
                    # print("测试成功， count=%d" % res['count'])
                    return "Pass"
            else:
                return "测试失败: %s" % res['msg']
        else:
            return "测试失败,status_code=[%d]" % response.status_code

    def asert_2(self, response):
        if response.status_code == 200:
            res = json.loads(response.text)
            if res['code'] == 0:
                # 通过数据库验证结果
                orderCount = self.dba.dbQueryOne("select count(*) from order_info where status='0' and dep='001'")
                if res['count'] == orderCount[0]:
                    # print("测试成功， count=%d" % res['count'])
                    return "Pass"
            else:
                return "测试失败: %s" % res['msg']
        else:
            return "测试失败,status_code=[%d]" % response.status_code

    def asert_3(self, response):
        if response.status_code == 200:
            res = json.loads(response.text)
            if res['code'] == 0:
                # 通过数据库验证结果
                orderCount = self.dba.dbQueryOne("select count(*) from order_info where status='0' and type='new'")
                if res['count'] == orderCount[0]:
                    # print("测试成功， count=%d" % res['count'])
                    return "Pass"
            else:
                return "测试失败: %s" % res['msg']
        else:
            return "测试失败,status_code=[%d]" % response.status_code

    def asert_4(self, response):
        if response.status_code == 200:
            res = json.loads(response.text)
            if res['code'] == 0:
                # 通过数据库验证结果
                orderCount = self.dba.dbQueryOne("select count(*) from order_info where status='0' and date='2020-09-08'")
                if res['count'] == orderCount[0]:
                    # print("测试成功， count=%d" % res['count'])
                    return "Pass"
            else:
                return "测试失败: %s" % res['msg']
        else:
            return "测试失败,status_code=[%d]" % response.status_code

    def asert_5(self, response):
        if response.status_code == 200:
            res = json.loads(response.text)
            if res['code'] == 0:
                # 通过数据库验证结果
                orderCount = self.dba.dbQueryOne(
                    "select count(*) from order_info where status='0' and dep='001' and type='new' and date='2020-09-08'")
                if res['count'] == orderCount[0]:
                    # print("测试成功， count=%d" % res['count'])
                    return "Pass"
            else:
                return "测试失败: %s" % res['msg']
        else:
            return "测试失败,status_code=[%d]" % response.status_code
