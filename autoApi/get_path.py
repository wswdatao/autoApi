# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
------------------------------------------
    Description :   获取当前项目地址
    File Name : get_path
    Author : Dade
    Create Time : 2023/2/13 17:24
------------------------------------------
    Change Activity:
        Modifier: 
        Modify time: 2023/2/13 17:24
------------------------------------------
"""

import os


def get_path():
    return os.path.split(__file__)[0]
