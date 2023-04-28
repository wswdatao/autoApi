# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
------------------------------------------
    Description :   接口用例文件，有且只有一个，场景、模块等根据yaml文件定义
    File Name : test_basic
    Author : Dade
    Create Time : 2023/2/13 17:33
------------------------------------------
    Change Activity:
        Modifier: 
        Modify time: 2023/2/13 17:33
------------------------------------------
"""

import time
import pytest
import allure
import jsonpath
from common.logger import logger
from enums.assert_enums import Assert
from common.asserter import Asserter
from util.recursion import recursion
from util.recursion import get_value_from_sql
from util.recursion import get_value_from_response


@allure.epic('CMS接口测试用例')
class TestDemo:

    def test_run(self, test_cases, cache_cases, get_token, cursor):
        """
            统一的用例执行方法，单接口用例单独执行，场景用例根据依赖递归执行
        :param test_cases:      测试用例
        :param cache_cases:     用例池数据
        :param get_token:       requests实例、请求头
        :param cursor:          数据库连接(0-mongo, 1-mysql)，暂未使用
        :return:
        """
        with allure.step(f'前置操作执行完毕（fixture加载、登录后台、获取Authorization令牌）'):
            res, headers = get_token
        with allure.step(f'①动态生成allure报告数据...'):
            # ######################## 动态allure报告 ##########################
            allure_infos = test_cases['allure']
            allure.dynamic.story(allure_infos['story'])
            allure.dynamic.title(allure_infos['title'])
            allure.dynamic.feature(allure_infos['feature'])
            allure.dynamic.severity(allure_infos['severity'])
        with allure.step(f'②组装用例场景，构建参数发起请求...'):
            # ######################## 发起接口请求 ############################
            case_id = test_cases["case_id"]
            result = recursion(res, headers, case_id, cache_cases)
            logger.info(f"用例场景已执行结束，最终响应结果为{result}.")
        with allure.step(f'③执行用例成功后对返回值进行断言...'):
            # ######################## 执行结束断言 ############################
            assert_data = test_cases["assert"]
            if assert_data['assert_type'] == Assert.RESPONSE.value:
                actual = get_value_from_response(assert_data['jsonpath'], result)
                if assert_data['type'] == Assert.Equal.value:
                    Asserter.eq(assert_data['value'], actual)
                elif assert_data['type'] == Assert.NotEqual.value:
                    Asserter.ne(assert_data['value'], actual)
                elif assert_data['type'] == Assert.Include.value:
                    Asserter.include(assert_data['value'], actual)
                else:
                    logger.error(f"断言时出错，断言类型暂不支持【{assert_data['type']}】...")
                    raise RuntimeError(f"断言时出错，断言类型暂不支持【{assert_data['type']}】...")
            elif assert_data['assert_type'] == Assert.SQL.value and cursor is not None:
                # sql_data = get_value_from_sql(None, assert_data['sql'])
                logger.error(f"断言时出错，暂未启用数据库断言...")
                raise RuntimeError(f"断言时出错，暂未启用数据库断言...")
            else:  # 目前只支持SQL、response两种类型
                logger.error(f"处理依赖参数时出错，暂不支持【{assert_data['assert_type']}】类型...")
                raise RuntimeError(f"处理依赖参数时出错，暂不支持【{assert_data['assert_type']}】类型...")
