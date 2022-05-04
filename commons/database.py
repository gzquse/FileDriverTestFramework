# -*- coding:utf-8 -*-
"""
    完成数据库操作
"""


class DataBaseApi:
    def __init__(self, conn):
        self.conn = conn

    def dbQuery(self, sql):
        # 拿到游标
        cursor = self.conn.cursor()

        # 执行sql
        cursor.execute(sql)

        result = cursor.fetchall()

        cursor.close()
        return result

    def dbQueryOne(self, sql):
        # 拿到游标
        cursor = self.conn.cursor()

        # 执行sql
        cursor.execute(sql)

        result = cursor.fetchone()

        cursor.close()
        return result

    def dbExecute(self, sql):
        # 拿到游标
        cursor = self.conn.cursor()

        # 执行sql
        cursor.execute(sql)

        cursor.close()
        self.conn.commit()

    def close(self):
        self.conn.close()
