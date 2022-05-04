# -*- coding:utf-8 -*-
"""
登陆主页
"""
from commons.SuperAsert import SuperAsert
# 主页面测试用例断言类

# 模块名、文件名、类名、方法名可以任意定义，与测试文件中 期望结果一致即可
# 约定1 所有断言类必须继承自SuperAsert父类
# 约定2 所有断言方法必须有一个参数response
# 约定3 所有断言方法必须有一个字符串的返回值，Pass代表断言测试成功，其他代表测试失败


class asserts(SuperAsert):
    def unlogin(self, response):
        if response.status_code == 200:
            if self.url != response.url:
                return "Pass"
            else:
                return "测试失败"
        else:
            return "测试失败,status_code=[%d]" % response.status_code

    def login(self, response):
        if response.status_code == 200:
            # print(response.url)
            # print(url)
            if self.url == response.url:
                return "Pass"
            else:
                return "测试失败"
        else:
            return "测试失败,status_code=[%d]" % response.status_code
