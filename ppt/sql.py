# -*- coding:utf-8 -*-
# @FileName  :sql.py
# @Time      :2022/5/18 下午4:48
# @Author    :tungwerl
import os
import sqlite3

db = '/mnt/hgfs/ShareFile/UrlManage.db'


class DB_OP():
    def __init__(self, db_name):
        if os.path.isfile(db_name) is True:
            self.conn = sqlite3.connect(db_name)
            self.csr = self.conn.cursor()
            print("数据库", db_name, "连接成功!")
        else:
            print('数据库不存在，请检查路径是否正确')

    def db_close(self):
        """
        关闭游标和连接
        """
        print('数据库游标和连接已关闭')
        self.conn.commit()
        self.conn.close()

    def addRecord(self, table_name: str, listing: str, value, sql):
        """
        先判断表里是否存在该数据，如果不存在就插入，存在则跳过
        :param table_name: 表名（字符串格式）
        :param listing: 判断是否重复的列名（字符串格式）
        :param value: 判断是否重复的值
        :return:
        """
        self.csr.execute(f'select * from {table_name} WHERE {listing} = "{value}"')
        result = self.csr.fetchone()
        if result is None:
            # self.csr.execute(f"insert into {table_name} ( {listing} ) values ('{value}')")
            self.csr.execute(sql)
            self.conn.commit()
            print("成功插入一条数据")
        else:
            print('数据已经存在，跳过！')

    def getRecord(self, table_name):
        """
        取出第一条数据，如果没有数据，返回0
        :return: 返回第一条数据，没有返回0
        """
        self.csr.execute(f'select * from {table_name} limit 1')
        result = self.csr.fetchone()
        if result is not None:
            print(result)
            return result
        else:
            return None

    def delRecord(self, table_name, listing, value):
        """
        删除指定数据
        :param table_name: 表名
        :param listing:   列名
        :param value: 要删除的值
        """
        sql = f"DELETE FROM {table_name} WHERE {listing} = '{value}'"
        self.csr.execute(sql)
        self.conn.commit()
        print(f"{value} 删除成功!")


# a = DB_OP(db)
# a.addRecord('new','url',f'www.baidu.com')
# a = DB_OP(db)
# a.getRecord('new')
# a = DB_OP(db)
# a.delRecord('new','url',f'www.baidu.com')
