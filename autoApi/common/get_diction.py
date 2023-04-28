# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
------------------------------------------
    Description :
    File Name : get_diction
    Author : Dade
    Create Time : 2023/2/15 10:40
------------------------------------------
    Change Activity:
        Modifier: 
        Modify time: 2023/2/15 10:40
------------------------------------------
"""

from common.logger import logger


class GetDiction:

    def __init__(self):
        self.url = '/market/dictionaryData/'

    def get_diction(self, request, host, diction, headers):
        """
            封装获取各字典库的方法，需要获取的字典库在config 配置文件中配置
        :param request:     requests实例
        :param host:        域名
        :param diction:     字典分组Code
        :param headers:     请求头（token）
        :return:    返回列表类型的【站点+枚举值】元祖，方便随机获取
        """
        try:
            temp = {}
            url = host + self.url + diction
            resp = request.get(url, None, headers)
            assert resp.status_code == 200
            infos = resp.json()
            for i in infos['data']:
                temp[i['pname']] = i['pcode']
            return list(temp.items())
        except Exception as e:
            logger.error(f'获取字典库数据失败，错误日志为【{e}】.')
            raise RuntimeError(f'获取字典库数据失败，请确认字典分组code【{diction}】是否正确.')


if __name__ == '__main__':
    from common.Requests import Requests
    res = Requests()
    host = 'http://test-cms-ishare.iask.com.cn/cms'
    diction = 'site'
    headers = {
                "Content-Type": "application/json; charset=UTF-8",
                "Authorization": "NzI1XzVmOWNkNmQzODhmNDRjZjliYzY4NDA5M2M5ZjY1NGMz"
    }
    dic = GetDiction()
    print(dic.get_diction(res, host, diction, headers))
