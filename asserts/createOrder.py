# -*- coding:utf-8 -*-
"""
需求申请断言类
"""
import json

from commons.SuperAsert import SuperAsert


class asserts(SuperAsert):
    """需求申请功能断言类"""
    def normal(self, response):
        if response.status_code == 200:
            # print(response.text)
            res = json.loads(response.text)
            if res['code'] == 0:
                # 通过数据库验证结果
                order = self.dba.dbQuery("select * from order_info where id=%s" % res['order_id'], self.dbconn)
                if len(order) == 1:
                    # 测试完成后，尽量还原测试现场，将测试数据清除
                    self.dba.dbExecute("delete from order_info where id=%s" % res['order_id'], self.dbconn)
                    return "Pass"
            else:
                return "测试失败: %s" % res['msg']
        else:
            return "测试失败,status_code=[%d]" % response.status_code

