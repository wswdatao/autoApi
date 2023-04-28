# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
------------------------------------------
    Description :
    File Name : request_enums
    Author : Dade
    Create Time : 2023/3/28 11:10
------------------------------------------
    Change Activity:
        Modifier: 
        Modify time: 2023/3/28 11:10
------------------------------------------
"""

from enum import Enum


class Method(Enum):

    GET = 'get'
    POST = 'post'
    POST_FILE = 'post_file'
