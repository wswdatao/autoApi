# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
------------------------------------------
    Description :
    File Name : process_param
    Author : Dade
    Create Time : 2023/2/13 18:06
------------------------------------------
    Change Activity:
        Modifier: 
        Modify time: 2023/2/13 18:06
------------------------------------------
"""

import re
import json
import time
import random
from faker import Faker
from get_path import get_path
from get_platform import get_platform
from common.logger import logger


class Build:

    """
        该类存放用例文件中需要替换的参数方法
    """

    def __init__(self):
        pass

    @property
    def host(self):
        from common.get_config import GetConfig
        config = GetConfig()
        env = config.get_options('config', 'ENV')['host']
        return env

    @property
    def path(self):
        now_path = get_path()
        way = get_platform()
        if way == '\\':
            path = now_path.replace("\\", way + way) + way + way + 'data' + way + way + 'upload' + way
        else:
            path = now_path + way + 'data' + way + 'upload' + way
        return path

    @property
    def get_time(self):
        now = time.strftime('%Y-%m-%d:%H:%M:%S')
        return now

    @property
    def now_day(self):
        day = time.strftime('%Y%m%d')
        return day

    @property
    def random_type(self):
        type_li = [0, 1, 2, 3]
        decorate_type = random.choice(type_li)
        return decorate_type

    @property
    def user_id(self):
        return '1105'

    @property
    def user_name(self):
        return 'autoTest'

    @classmethod
    def time_process(cls, now):
        temp = time.localtime(int(now))
        now = time.strftime('%Y-%m-%d:%H:%M:%S', temp)
        return now


def regular(infos):
    """
        参数替换方法，将字典转成json字符串后进行参数替换，替换后再次转成字典返回
    :param infos:
    :return:
    """
    rule = '\\${(.*?)}'
    infos = json.dumps(infos, ensure_ascii=False)
    try:
        while re.findall(rule, infos):
            key = re.search(rule, infos).group(1)
            # 如果参数中不会出现以下字符导致读取报错 可以去掉异常处理 return也可以换成json.loads(info)
            try:
                infos = re.sub(rule, f"{getattr(Build(), key)}", infos, 1)
                infos = infos.replace("false", 'False')
                infos = infos.replace("null", 'None')
                infos = infos.replace("true", 'True')
            except Exception:
                infos = infos.replace("${%s}" % key, f"{getattr(Build(), key)}")
                infos = infos.replace("false", 'False')
                infos = infos.replace("null", 'None')
                infos = infos.replace("true", 'True')
        return eval(infos)
    except AttributeError:
        logger.error(f"未找到对应的替换数据, 请检查数据【{infos}】是否正确.")
        raise RuntimeError(f"未找到对应的替换数据, 请检查数据【{infos}】是否正确.")


if __name__ == '__main__':
    build = Build()
    print(build.path)
    print(build.random_type)
