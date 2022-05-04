# -*- coding:utf-8 -*-
"""
测试执行器
"""
import xlrd
from commons.TestSuite import TestSuite
import pymysql
import time
import datetime
import os
import xlwt
from commons.database import DataBaseApi
# 测试执行器
# 运行测试的发动机


class TestRunner:
    """
    测试执行器
    需要完成文件读取，并调度各个测试场景，生成testSuite执行测试
    """
    def __init__(self, _filePath, _tester):
        self.file_path = _filePath
        self.tester = _tester
        print("测试开始: {}".format(_filePath))

        self.book = xlrd.open_workbook(filename=_filePath)

        # 第1个sheet页为配置页，读取配置参数
        config_sheet = self.book.sheet_by_index(0)
        configs = {}
        for i in range(config_sheet.nrows)[1:]:
            line = config_sheet.row_values(i)
            if line[0] == "系统名称":
                configs['sys_name'] = line[1]
            elif line[0] == "版本":
                configs['version'] = line[1]
            elif line[0] == "应用地址":
                configs['host_addr'] = line[1]
            elif line[0] == "登陆URL":
                configs['login_url'] = line[1]
            elif line[0] == "登陆参数":
                configs['login_params'] = line[1]
            elif line[0] == "注销URL":
                configs['logout_url'] = line[1]
            elif line[0] == "数据库地址":
                conn = pymysql.connect(
                    line[1].split(":")[0],
                    line[1].split(":")[2],
                    line[1].split(":")[3],
                    line[1].split(":")[4],
                    int(line[1].split(":")[1])
                )
                configs['dba'] = DataBaseApi(conn)

        self.configs = configs

    def do_runner(self):
        runner_begin = time.time()
        total = 0
        pass_count = 0
        fail_count = 0
        test_suites = []
        # 读取后续sheet，每一个sheet是一个测试点 testSuite
        for sheet_name in self.book.sheet_names()[1:]:
            sheet = self.book.sheet_by_name(sheet_name)
            suite_res = TestSuite(sheet, self.configs).do_suite()
            total += suite_res['total']
            pass_count += suite_res['pass_count']
            fail_count += suite_res['fail_count']
            test_suites.append(suite_res)

        # 关闭数据库连接
        self.configs['dba'].close()
        runner_end = time.time()
        res = {
            "file_path": self.file_path,
            "tester": self.tester,
            "test_datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "exectime": round(runner_end - runner_begin, 3),
            "total": total,
            "pass_count": pass_count,
            "fail_count": fail_count,
            "test_suites": test_suites,
        }

        reportPath = 'TestReports'
        if not os.path.exists(reportPath):
            os.mkdir(reportPath)
        file_name = os.path.split(self.file_path)[1]
        reportFileName = reportPath+'/'+os.path.splitext(file_name)[0] + "_测试报告_" + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + os.path.splitext(file_name)[1]
        createReport(reportFileName, res)


def createReport(file_path, res):
    """生成测试报告"""
    print("测试报告:", file_path)
    # print(res)
    # 保存文件
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('测试报告')

    # 统一字体
    font = xlwt.Font()
    font.name = '微软雅黑'
    font.bold = False
    font.underline = False
    font.italic = False

    font_title = xlwt.Font()
    font_title.name = '微软雅黑'
    font_title.height = 18 * 20
    font_title.bold = False
    font_title.underline = False
    font_title.italic = False

    # 边框
    borders = xlwt.Borders()
    borders.left = xlwt.Borders.THIN
    borders.right = xlwt.Borders.THIN
    borders.top = xlwt.Borders.THIN
    borders.bottom = xlwt.Borders.THIN
    borders.left_colour = 0x40
    borders.right_colour = 0x40
    borders.top_colour = 0x40
    borders.bottom_colour = 0x40

    # 对齐方式
    alignment = xlwt.Alignment()
    alignment.horz = 0x02
    alignment.vert = 0x01

    # 背景色 表头
    pattern_tt = xlwt.Pattern()
    pattern_tt.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern_tt.pattern_fore_colour = 43

    pattern_suite = xlwt.Pattern()
    pattern_suite.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern_suite.pattern_fore_colour = 42

    # 普通单元格格式
    style = xlwt.XFStyle()
    style.borders = borders
    style.font = font

    # 标题单元格格式
    style_tt = xlwt.XFStyle()
    style_tt.borders = borders
    style_tt.font = font
    style_tt.pattern = pattern_tt

    # 标题2单元格格式
    style_tt2 = xlwt.XFStyle()
    style_tt2.borders = borders
    style_tt2.font = font
    style_tt2.pattern = pattern_suite

    # 标题格式
    style_title = xlwt.XFStyle()
    style_title.font = font_title
    style_title.alignment = alignment

    # 写入标题行
    worksheet.write_merge(1, 2, 0, 4, "测试报告", style_title)

    worksheet.write(3, 0, "测试用例文件", style_tt)
    worksheet.write_merge(3, 3, 1, 4, res['file_path'], style)
    worksheet.write(4, 0, "测试执行人", style_tt)
    worksheet.write_merge(4, 4, 1, 4, res['tester'], style)
    worksheet.write(5, 0, "开始时间", style_tt)
    worksheet.write_merge(5, 5, 1, 4, res['test_datetime'], style)
    worksheet.write(6, 0, "执行时间", style_tt)
    worksheet.write_merge(6, 6, 1, 4, str(res['exectime'])+"秒", style)
    worksheet.write(7, 0, "结果统计", style_tt)
    worksheet.write_merge(7, 7, 1, 4, "共执行用例({})个，通过({})个，未通过({})个。".format(res['total'], res['pass_count'], res['fail_count']), style)

    worksheet.write(8, 0, "测试点/测试用例", style_tt)
    worksheet.write(8, 1, "合计", style_tt)
    worksheet.write(8, 2, "通过", style_tt)
    worksheet.write(8, 3, "失败", style_tt)
    worksheet.write(8, 4, "执行时间(秒)", style_tt)
    line = 9
    for suite in res['test_suites']:
        worksheet.write(line, 0, suite['suite_name'], style_tt2)
        worksheet.write(line, 1, suite['total'], style_tt2)
        worksheet.write(line, 2, suite['pass_count'], style_tt2)
        worksheet.write(line, 3, suite['fail_count'], style_tt2)
        worksheet.write(line, 4, suite['suite_exectime'], style_tt2)
        line += 1

        for test_case in suite['test_cases']:
            worksheet.write(line, 0, "  " + test_case['name'], style)
            worksheet.write_merge(line, line, 1, 3, test_case['asert'], style)
            worksheet.write(line, 4, test_case['exectime'], style)
            line += 1

    worksheet.write(line, 0, "合计", style_tt2)
    worksheet.write(line, 1, res['total'], style_tt2)
    worksheet.write(line, 2, res['pass_count'], style_tt2)
    worksheet.write(line, 3, res['fail_count'], style_tt2)
    worksheet.write(line, 4, res['exectime'], style_tt2)
    line += 1

    worksheet.col(0).width = 40 * 256
    worksheet.col(1).width = 20 * 256
    worksheet.col(2).width = 20 * 256
    worksheet.col(3).width = 20 * 256
    worksheet.col(4).width = 12 * 256

    workbook.save(file_path)
