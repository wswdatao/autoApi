# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
------------------------------------------
    Description :   封装连接和操作 mysql、mongo 数据库的工具类
    File Name : database
    Author : Dade
    Create Time : 2023/2/13 17:38
------------------------------------------
    Change Activity:
        Modifier: 
        Modify time: 2023/2/13 17:38
------------------------------------------
"""

import pymongo
import pymysql
from common.logger import logger


class ConnectMysql:

    def __init__(self, database, account, password, host, port):
        """
            实例化方法，根据传入的 mysql连接信息+库名建立数据库连接，生成游标
        :param database:    数据库名
        :param account:     用户名
        :param password:    用户密码
        :param host:        host地址
        :param port:        端口号
        """
        self.connect = pymysql.connect(             # 建立数据库连接
            database=database, user=account, password=password, host=host, port=int(port)
        )
        self.cursor = self.connect.cursor()         # 生成游标实例
        logger.debug(f"连接mysql数据库成功...")

    def find(self, sql):
        """
            根据传入的 sql语句进行查询，并返回结果
        :param sql:         需要执行的 sql语句
        :return:            返回查询结果（元祖）
        """
        self.cursor.execute(sql)
        infos = self.cursor.fetchall()
        # self.connect.close()
        return infos

    def execute(self, sql):
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            logger.success(f'执行Mysql语句成功，本次执行语句为【{sql}】.')
        except Exception as e:
            self.connect.rollback()
            logger.error(f'执行Mysql语句【{sql}】失败，错误日志为【{e}】，数据已回滚...')
            # self.connect.close()

    def session_close(self):
        """
            业务实现中可能存在循环，每次处理时关闭和校验数据库连接会很麻烦
            因此单独封装出来，在完成所有操作后执行再关闭数据库连接的操作
        :return:
        """
        self.connect.close()
        logger.debug(f"已关闭mysql数据库连接...")


class ConnectMongo:

    def __init__(self, url, database, user, password):
        """
            根据传入的 mongo连接信息+库名建立数据库连接
        :param url:         mongo连接 url
        :param database:    数据库名
        """
        self.db = pymongo.MongoClient(url)[database]
        self.db.authenticate(name=user, password=password)
        logger.debug(f"连接MongoDB数据库成功!")

    def delete_many(self, table, field, keyword):
        """
            mongo 批量删除数据，传入表名、匹配字段和关键字，删除所有匹配到的数据
        :param table:       表名
        :param field:       匹配字段
        :param keyword:     关键字
        :return:
        """
        # collections = self.db.list_collection_names()                   # 获取所有表名
        self.db[table].delete_many({field: {'$regex': keyword}})        # 批量删除 匹配到的数据
        logger.success(f'正在清除mongo表【{table}】的数据，匹配字段为【{field}】，匹配内容为【{keyword}】.')

    def find_one(self, table, condition):
        """
            传入表名、查询条件  例如 {"_id": "this is test Id"}  find_one为精确查找
            相较于find会返回一个集合 find_one更适合获取封装使用 查询准确的数据并返回
        :param table:       表名
        :param condition:   条件
        :return:            查询结果
        """
        result = self.db[table].find_one(condition)
        logger.debug(f"正在查询数据，表名为【{table}】， 查询条件为【{condition}】.")
        return result

    def insert(self, table, info):
        """
            暂未调试，传入表名、插入数据  例如 {"_id": "this is test Id"}
        :param table:       表名
        :param info:        数据
        :return:            执行结果
        """
        self.db[table].insert_one(dict(info))
        logger.success(f"已向表{table}插入数据，本次插入数据为【{info}】.")
