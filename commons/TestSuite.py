# -*- coding:utf-8 -*-
"""
测试套件场景
"""
from commons.TestCase import TestCase
import re
import time
# 测试套件，可以暂时理解为对应一个sheet的全部测试用例


class TestSuite:
    # 测试套件，处理一个完整的测试点
    def __init__(self, sheet, configs):
        self.sheet = sheet
        self.configs = configs

        print("测试点 <{}> 初始化完毕...".format(sheet.name))

    def do_suite(self):
        suite_begin = time.time()
        total = 0
        pass_count = 0
        test_cases = []
        for i in range(self.sheet.nrows)[1:]:
            line = self.sheet.row_values(i)
            if isinstance(line[0], float) or re.match(r"^\d+$", line[0]):
                begin = time.time()
                asert = TestCase(line, self.configs).do_test()
                end = time.time()
                total += 1
                if asert == "Pass":
                    pass_count += 1
                test_cases.append({
                    "id": "{}".format(int(line[0])),
                    "name": line[1],
                    "exectime": round(end-begin, 3),
                    "asert": asert,
                })
            else:
                continue

        print("测试点 <{}> 共执行用例({})个, 测试通过({}), 测试未通过({})".format(self.sheet.name, total, pass_count, total - pass_count))
        # print(test_cases)
        suite_end = time.time()

        return {
            "suite_name": self.sheet.name,
            "suite_exectime": round(suite_end - suite_begin, 3),
            "test_cases": test_cases,
            "total": total,
            "pass_count": pass_count,
            "fail_count": total-pass_count,
        }
