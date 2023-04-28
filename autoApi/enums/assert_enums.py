# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
------------------------------------------
    Description :
    File Name : assert_enums
    Author : Dade
    Create Time : 2023/2/17 15:21
------------------------------------------
    Change Activity:
        Modifier: 
        Modify time: 2023/2/17 15:21
------------------------------------------
"""

from enum import Enum


class Assert(Enum):

    SQL = 'SQL'
    RESPONSE = 'response'
    Equal = '=='
    NotEqual = '!='
    Include = 'in'
