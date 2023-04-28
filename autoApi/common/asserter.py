# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
------------------------------------------
    Description :
    File Name : assertion
    Author : Dade
    Create Time : 2023/2/15 10:59
------------------------------------------
    Change Activity:
        Modifier: 
        Modify time: 2023/2/15 10:59
------------------------------------------
"""


class Asserter:

    @staticmethod
    def eq(expect, actual):
        try:
            assert expect == actual
        except Exception:
            raise AssertionError(f'相等断言异常，预期结果为【{expect}】，实际结果为【{actual}】，两者并不相等...')

    @staticmethod
    def ne(expect, actual):
        try:
            assert expect != actual
        except Exception:
            raise AssertionError(f'不等断言异常，预期结果为【{expect}】，实际结果为【{actual}】，两者相等...')

    @staticmethod
    def include(expect, actual):
        try:
            assert actual in expect
        except Exception:
            raise AssertionError(f'包含断言异常，预期结果为【{expect}】，实际结果为【{actual}】，实际结果不包含在预期结果内...')
