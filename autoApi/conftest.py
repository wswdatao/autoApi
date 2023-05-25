# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
------------------------------------------
    Description :
    File Name : conftest
    Author : Dade
    Create Time : 2023/2/15 11:42
------------------------------------------
    Change Activity:
        Modifier: 
        Modify time: 2023/2/15 11:42
------------------------------------------
"""

import json
import time
import allure
import pytest
import jsonpath
from common.logger import logger
from common.Requests import Requests
from common.get_config import GetConfig
from common.database import ConnectMongo
from common.database import ConnectMysql
from util.read_yaml import ReadYAML
from common.notice import Notice


@pytest.fixture(scope='session', autouse=True)
def build(get_config, cursor):
    logger.debug('************************************************************************')
    logger.debug('**************************** 正在启动测试框架 ****************************')
    logger.debug('************************************************************************')
    mongo_tables = get_config.get_options('config', 'TABLE_MONGO')
    mysql_tables = get_config.get_options('config', 'TABLE_MYSQL')
    mongo, mysql = cursor
    yield mongo, mysql, mongo_tables, mysql_tables
    logger.debug('************************************************************************')
    logger.debug('**************************** 正在清理测试数据 ****************************')
    logger.debug('************************************************************************')
    for mongo_table in mongo_tables:
        clear_info = mongo_tables[mongo_table].split(',')
        if len(clear_info) == 3:
            mongo.delete_many(clear_info[0], clear_info[1], clear_info[2])
        else:
            logger.error(f"config文件中配置的mongo表【{mongo_table}】清理信息错误...")
    for mysql_table in mysql_tables:
        mysql.execute(mysql_tables[mysql_table])
    logger.debug('************************************************************************')
    logger.debug('**************************** 测试框架运行完毕 ****************************')
    logger.debug('************************************************************************')


@pytest.fixture(scope='session')
def get_config():
    """
        在conftest文件中进行前置实例化，生成获取配置文件的工具方法实例
    :return: 方法实例
    """
    config = GetConfig()
    return config


@pytest.fixture(scope='session')
def cursor(get_config):
    """
        在conftest文件中进行前置实例化，生成获取配置文件的工具方法实例
    :return: 方法实例
    """
    mongo_infos = get_config.get_options('config', 'DATABASE_MONGO')
    mysql_infos = get_config.get_options('config', 'DATABASE_MYSQL')
    func_mongo = ConnectMongo(
        mongo_infos['url'], mongo_infos['database'], mongo_infos['user'], mongo_infos['password'])
    func_mysql = ConnectMysql(
        mysql_infos['database'], mysql_infos['account'], mysql_infos['password'],
        mysql_infos['host'], mysql_infos['port'])
    return func_mongo, func_mysql


@pytest.fixture(scope='session')
def read_yaml():
    """
        在conftest文件中进行前置实例化，读取用例方法
    :return: 方法实例
    """
    read = ReadYAML()
    return read


@pytest.fixture(scope='session')
def res():
    res = Requests()
    return res


@pytest.fixture(scope='session', autouse=True)
def cache_cases(read_yaml):
    """
        读取所有接口测试用例，处理完毕后写入用例池，再返回
    :param read_yaml:
    :return:
    """
    cases = read_yaml.save_cache_cases()
    return cases


@pytest.fixture(params=ReadYAML().load_cases())
def test_cases(request):
    return request.param


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """
        hook函数，执行完毕后统计执行用例数和成功率，并进行钉钉通知
    :param terminalreporter:    固定写法
    :param exitstatus:          固定写法
    :param config:              固定写法
    :return:
    """
    total = terminalreporter._numcollected
    passed = len(terminalreporter.stats.get('passed', []))
    success_rate = round((passed / total) * 100, 2)
    Notice().report_notice(total, success_rate)         # 报告在线地址暂未启用


@allure.feature("CMS_获取登录token参数")
@allure.description("定义前置fixture，返回各项case运行需要的token")
@allure.severity("critical")
@pytest.fixture(scope='session')
def get_token(get_config, res):
    """
        接口测试用例运行前置方法，获取登录所需要的token，组装成header
    :param get_config:  获取配置文件的工具方法实例
    :return:            requests实例、域名、headers（带token）
    """
    config = get_config
    login = config.get_options('config', 'LOGIN')
    host = config.get_options('config', 'ENV')['host']
    # ##############################  以上初始化数据  ##############################
    login_url = host + login['url']
    headers = json.loads(login['headers'])
    data = {"userName": login['user'], "userPwd": login['password'], "loginDeviceType": login['device']}
    try:
        token_id = jsonpath.jsonpath(res.post(login_url, data, headers), '$..tokenId')[0]
        headers['Authorization'] = token_id
        logger.info(f'接口自动化前置-获取token参数方法运行成功，本次登录tokenID为【{token_id}】.')
        return res, headers
    except Exception as e:
        logger.error(f'获取token参数失败，错误日志为{e}.')
        raise RuntimeError(f'{login["url"]}接口请求失败，请确认登录服务是否已启动...')
