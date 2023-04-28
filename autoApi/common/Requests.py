# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
------------------------------------------
    Description :
    File Name : Requests
    Author : Dade
    Create Time : 2023/2/13 17:50
------------------------------------------
    Change Activity:
        Modifier: 
        Modify time: 2023/2/13 17:50
------------------------------------------
"""

import json
import time
import requests
from common.logger import logger


class Requests:

    def __init__(self):
        self.res = requests

    def get(self, *params):
        content = self.res.get(url=params[0], params=params[1], headers=params[2]).json()
        logger.info(f'正在发起GET请求，请求地址：【{params[0]}】，请求参数：{params[1]}，请求头：{params[2]}')
        return content

    def post(self, *params):
        content = self.res.post(url=params[0], data=json.dumps(params[1]), headers=params[2]).json()
        logger.info(f'正在发起POST请求，请求地址：【{params[0]}】，请求参数：{params[1]}，请求头：{params[2]}')
        return content

    def post_params(self, *params):
        """
            扩展方法，支持部分旧接口走的post，但实际传参方式与Get请求相同的场景
        :param params:
        :return:
        """
        content = self.res.post(url=params[0], params=params[1], headers=params[2]).json()
        logger.info(f'正在发起POST请求，请求地址：【{params[0]}】，请求参数：{params[1]}，请求头：{params[2]}')
        return content

    def post_file(self, *params):
        """
            扩展方法，支持上传文件场景，上传接口只需要校验token，isForever替换时全部替换大写了，需要调整回来
        :param params:
        :return:
        """
        headers = {}
        file = {"file": open(params[3], 'rb')}
        headers["Authorization"] = params[2]["Authorization"]
        if params[1].get("isForever"):
            params[1]["isForever"] = 'false'
        content = self.res.post(url=params[0], data=params[1], files=file, headers=headers).json()
        logger.info(f'正在发起POST_FILE请求，请求地址：【{params[0]}】，请求参数：{params[1]}，'
                    f'上传文件为：【{file}】')
        return content

    def post_export(self, *params):
        """
            扩展方法，支持导出接口，导出后暂停10秒，避免可能导出记录还未新增+未完成时直接查询导致的失败
        :param params:
        :return:
        """
        content = self.res.post(url=params[0], data=json.dumps(params[1]), headers=params[2]).json()
        logger.info(f'正在发起POST_EXPORT请求，请求地址：【{params[0]}】，请求参数：{params[1]}，请求头：{params[2]}')
        time.sleep(10)
        return content
