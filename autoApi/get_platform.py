# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
------------------------------------------
    Description :   获取当前运行终端应该使用的路径符
    File Name : platform
    Author : Dade
    Create Time : 2023/2/13 18:11
------------------------------------------
    Change Activity:
        Modifier: 
        Modify time: 2023/2/13 18:11
------------------------------------------
"""

import platform


def get_platform():
    terminal = platform.system()
    path = "\\" if terminal == 'Windows' else '/'
    return path


if __name__ == '__main__':
    print(get_platform())
