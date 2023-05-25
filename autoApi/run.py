# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
------------------------------------------
    Description :
    File Name : run
    Author : Dade
    Create Time : 2023/2/13 17:30
------------------------------------------
    Change Activity:
        Modifier: 
        Modify time: 2023/2/13 17:30
------------------------------------------
"""

import os
import pytest

if __name__ == '__main__':
    pytest.main()
    # os.system(r"copy environment.properties report\tmp\environment.properties")   # 这部分是在windows执行后查看报告
    # os.system(r"copy report\result\history report\tmp\history")     # 用于生成allure趋势信息
    # os.system(r"allure generate -o .\report\result --clean .\report\tmp")
    # os.system(r"allure open .\report\result")     # 通过allure浏览报告  linux环境执行时注释掉
