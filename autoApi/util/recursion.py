# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
------------------------------------------
    Description :
    File Name : recursion
    Author : Dade
    Create Time : 2023/3/10 16:02
------------------------------------------
    Change Activity:
        Modifier: 
        Modify time: 2023/3/10 16:02
------------------------------------------
"""

import time
import jsonpath
from common.logger import logger
from enums.method_enums import Method
from enums.dependency_enums import Dependence


def run(res, headers, current_case):
    """
        根据传入的用例数据组织请求信息，发起请求后返回接口返回值
        额外扩展：加入是否执行定时任务的逻辑判断
    :param res:             requests实例
    :param headers:         请求头
    :param current_case:    执行用例参数
    :return:                执行接口返回值
    """
    url = current_case["host"]+current_case["url"]
    method = current_case['method'].lower()
    data = current_case['data']

    logger.debug(f"run方法，构建请求参数，正在执行测试用例...")
    try:
        do = getattr(res, method)
        if method.upper() == Method.POST_FILE.name:
            file = current_case['file_path']
            result = do(url, data, headers, file)
        else:
            result = do(url, data, headers)
        try:
            do_task = current_case['execute_task']
            if do_task:
                task_rule = current_case['task_rule']
                get_result_from_task(task_rule)
        except Exception as e:
            logger.error(f"执行定时任务出错，可能是用例未带上相关参数，错误原因为【{e}】")
        return result
    except AttributeError as e:
        logger.error(f"执行用例时出错，请求方式不包含【{method}】")
        raise RuntimeError(f"执行用例时出错，请求方式不包含【{method}】，{e}")


def get_value_from_response(path, result):
    """
        从接口返回值中获取指定path的值
    :param path:        jsonpath地址
    :param result:      接口返回值
    :return:            提取到的值
    """
    logger.debug(f"get_value_from_response，即将从响应结果【{result}】中提取【{path}】依赖值...")
    value = jsonpath.jsonpath(result, path)[0]
    return value


def get_value_from_sql(cursor, sql):
    """
        需要传入两个数据库连接游标，根据具体语句判断使用哪一个
    :param cursor:      游标，需要传入mysql、mongo两个游标
    :param sql:         sql语句
    :return:            sql查询结果
    """
    logger.debug(f"get_value_from_sql，暂未使用，未编写逻辑...")
    return ''


def get_result_from_task(info):
    """
        适用于需要执行xxl-job定时任务的用例，目前暂定方案为执行后等待6秒后校验任务执行结果
        后续确认python如何调用xxljob执行任务后再考虑实现
    :param info:
    :return:
    """
    # 以上为定时任务执行区
    time.sleep(6)


def recursion(res, headers, case_id, case_list, cursor=None):
    """

    :param res:         requests实例
    :param headers:     请求头
    :param case_id:     用例id
    :param case_list:   用例池
    :param cursor:      数据库游标，暂不启用默认为空
    :return:            最终接口的返回值
    """
    current_case = case_list[case_id]
    # 用例存在依赖用例时，递归调用run_case函数依次处理
    if current_case['dependency_case']:
        dependency_case_id = current_case['dependency_case']['dependency_id']
        dependency_data = current_case['dependency_case']['dependency_data']
        dependency_result = recursion(res, headers, dependency_case_id, case_list)
        # 获取依赖参数，替换到当前用例中
        if dependency_data:
            logger.debug(f"依赖用例存在依赖参数，即将进行参数替换...")
            for data in dependency_data:
                if data['dependency_type'] == Dependence.RESPONSE.value:
                    response_data = get_value_from_response(data['jsonpath'], dependency_result)
                    current_case['data'][data['replace_key']] = response_data
                elif data['dependency_type'] == Dependence.SQL.value and cursor is not None:
                    sql_data = get_value_from_sql(cursor, data['sql'])
                    current_case['data'][data['replace_key']] = sql_data
                else:                       # 目前只支持SQL、response两种类型
                    logger.error(f"处理依赖参数时出错，依赖类型暂不支持【{data['dependency_type']}】...")
                    raise RuntimeError(f"处理依赖参数时出错，依赖类型暂不支持【{data['dependency_type']}】...")
            current_result = run(res, headers, current_case)        # 依赖均替换完成后执行用例
            return current_result
        else:           # 用例不存在依赖参数，直接执行
            current_result = run(res, headers, current_case)
            return current_result
    else:               # 当前用例没有依赖用例，直接执行
        current_result = run(res, headers, current_case)
        return current_result
