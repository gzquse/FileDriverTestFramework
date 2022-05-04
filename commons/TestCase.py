# -*- coding:utf-8 -*-
"""
测试用例
"""
import requests
import json
import re
import traceback


class TestCase:
    def __init__(self, line, configs):
        # 构造函数初始化时 载入各种初始化变量
        self.case_id = line[0]
        self.case_name = line[1]
        self.Asert = "Fail"
        self.line = line
        self.url = configs['host_addr'] + line[3]
        self.method = line[4]
        self.params = eval(line[5]) if line[5].strip() else ""
        self.is_login = True if line[6] == "是" else False
        self.asert_type = line[7]
        self.expect = line[8]
        self.login_url = configs['host_addr'] + configs['login_url']
        self.logout_url = configs['host_addr'] + configs['logout_url']
        self.login_param = eval(configs['login_params'])
        self.cookies = None
        self.dba = configs['dba']
        print(">>>测试用例({:.0f})[{}]...".format(float(self.case_id), self.case_name), end='...')

    def setup(self):
        # 前处理方法
        # 如果需要登录，完成登录并获得cookies
        if self.is_login:
            res = requests.post(self.login_url, data=self.login_param)
            if res.status_code == 200:
                self.cookies = res.cookies
            #     print("登陆成功.")
            # else:
            #     print("登陆失败.")

    def do_test(self):
        """
        测试主方法
        完成测试用例的执行
        :return:
        """
        try:
            self.setup()

            # 根据调用方式是get/post,请求参数params,是否需要登录
            # 来配置参数 采用关键字可变参数来传输
            _kwargs = {
                "url": self.url
            }
            if self.is_login:
                # 如果是需要登录才能访问的请求
                # 在参数中加入cookies
                _kwargs['cookies'] = self.cookies

            if self.method == "get":
                # get请求配置参数params 并调用get方法得到response
                if self.params:
                    _kwargs['params'] = self.params
                response = requests.get(**_kwargs)
            else:
                # post请求配置form-data 并调用post方法得到response
                if self.params:
                    _kwargs['data'] = self.params
                response = requests.post(**_kwargs)

            # 断言开始
            # 根据配置的断言方式不同，完成断言，最终要self.Asert有一个结果，Pass表示测试通过，其他表示失败，并传递失败内容
            if self.asert_type.startswith("响应码"):  # 直接以响应码断言
                if response.status_code == int(self.expect):
                    self.Asert = "Pass"
                else:
                    self.Asert = "Fail: status_code = %d" % response.status_code
            elif self.asert_type.startswith("响应内容"):  # 根据响应内容断言，这的前提是响应内容为json格式
                if response.status_code == 200:
                    res = json.loads(response.text)
                    if eval(self.expect, res):
                        self.Asert = "Pass"
                    else:
                        self.Asert = self.expect + " 未成立. " + response.content.decode("gbk")
                else:
                    self.Asert = "测试失败,status_code=[%d]" % response.status_code
            elif self.asert_type.startswith("自定义"):  # 自定义方法 断言
                # 使用反射 实例化对象 并执行方法调用，
                rr = re.match(r"^(.*)\.(\w+)$", self.expect)
                if rr.group():
                    # 包名和类名 根据类名可以实例化对象
                    class_path = rr.group(1)
                    # 方法名 执行对应方法完成断言
                    method_name = rr.group(2)

                    # 反射出对象 初始化时传入3个基础参数
                    asert_object = createObject('asserts.'+class_path, self.url, self.params, self.dba)

                    # 调用方法并传入response参数
                    self.Asert = doMethod(asert_object, method_name, response)

        except Exception as e:
            traceback.print_exc()
            self.Asert = str(e)
        finally:
            self.teardown()

        return self.Asert

    def teardown(self):
        # 结束处理中，注销登录，节约系统资源
        if self.is_login:
            try:
                requests.post(self.logout_url, cookies=self.cookies)
                # print("注销登录.")
            except Exception as e:
                traceback.print_exc()
                print("注销登录异常:", e)

        print(self.Asert)


def createObject(name_path, *args, **kwargs):
    r = re.match(r"^(.*)\.(\w+)$", name_path)
    if r.group():
        module_name = r.group(1)
        class_name = r.group(2)
        module = __import__(module_name, fromlist=True)
        class_obj = getattr(module, class_name)
        o = class_obj(*args, **kwargs)
        return o
    else:
        raise ValueError("无法实例化 {}".format(name_path))


def doMethod(obj, method_name, *args, **kwargs):
    if hasattr(obj, method_name):
        method = getattr(obj, method_name)
        return method(*args, **kwargs)
    else:
        raise ValueError("没有这个方法:{}".format(method_name))

