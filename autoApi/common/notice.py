# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
------------------------------------------
    Description :
    File Name : notice
    Author : Dade
    Create Time : 2023/2/15 11:01
------------------------------------------
    Change Activity:
        Modifier: 
        Modify time: 2023/3/24 17:34
------------------------------------------
"""

import json
import time
import requests
from get_path import get_path
from get_platform import get_platform


class Notice:

    def __init__(self):
        self.linkman = ''                                                       # 钉钉群艾特的手机号，可传入列表艾特多个
        self.say = 'https://v1.hitokoto.cn/?c=i&encode=text'                    # 一言api-sc
        self.jenkins = ''                                                       # jenkins域名
        self.url = 'https://oapi.dingtalk.com/robot/send?access_token='         # ding机器人域名
        self.headers = {"Content-Type": "application/json;charset=UTF-8"}
        self.access_token = '机器人access_token'

    def report_notice(self, total, success, url=None):
        """
            根据传参，调取钉钉机器人通知接口，markdown格式
        :param res:         requests实例
        :param total:       执行用例数
        :param success:     执行成功率
        :param url:         allure报告地址
        :return:
        """
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        saying = requests.get(self.say).text
        from util.read_yaml import ReadYAML
        way = get_platform()
        file_path = get_path() + way + "cache" + way
        name = "cache_Cases"
        case_num = len(ReadYAML().safe_load(file_path, name))
        message = {
                     "msgtype": "markdown",
                     "markdown": {
                         "title": "CMS接口自动化执行结果通知",
                         "text": f">{saying}\n> \n"
                                 f"#### 测试用例总数：{case_num} \n"
                                 f"#### 实际用例执行数：{total} \n"
                                 f"#### 实际执行通过率：{success}% \n"
                                 f"#### 执行时间：{now} \n"
                                 f"#### 在线报告地址：[【点我跳转】]({url}) \n"
                                 f"###### @{self.linkman} \n"
                     },
                     "at": {
                         "atMobiles": [
                              f"{self.linkman}",
                         ],
                         "isAtAll": False
                      }
                 }
        requests.post(url=self.url + self.access_token, data=json.dumps(message), headers=self.headers)

    def build_notice(self, res, service, params, num):
        """
            auto_builder 自动部署环境失败通知
        :param res:             requests实例
        :param service:         服务名
        :param params:          构建参数
        :param num:             构件编号
        :return:
        """
        saying = res.get(self.say).text   # 随机格言api
        console = f'{self.jenkins}/{service}/{num}/console'
        message = {
                     "msgtype": "markdown",
                     "markdown": {
                         "title": "auto_builder 服务部署失败消息通知",
                         "text": f">{saying}\n> \n"
                                 f"#### 失败服务：{service} \n"
                                 f"#### 构建参数：{params} \n"
                                 f"#### 构建日志：[【点我跳转】]({console}) \n"
                                 f"###### @{self.linkman} \n"
                     },
                     "at": {
                         "atMobiles": [
                              f"{self.linkman}",
                         ],
                         "isAtAll": False
                      }
                 }
        res.post(url=self.url + self.access_token, data=json.dumps(message), headers=self.headers)

    def update_notice(self, services):
        """
            Jenkins 服务更新通知，自动部署是检测到新增job在钉钉进行提示
        :param services:        服务名列表
        :return:
        """
        saying = requests.get(self.say).text   # 随机格言api
        message = {
                     "msgtype": "markdown",
                     "markdown": {
                         "title": "auto_builder 环境部署消息通知",
                         "text": f">{saying}\n> \n"
                                 f"#### newJob：{services} \n"
                                 f"#### **请及时将以上服务维护到脚本中！** \n"
                                 f"###### @{self.linkman} \n"
                     },
                     "at": {
                         "atMobiles": [
                              f"{self.linkman}",
                         ],
                         "isAtAll": False
                      }
                 }
        requests.post(url=self.url + self.access_token, data=json.dumps(message), headers=self.headers)


if __name__ == '__main__':
    import requests
    ding = Notice()
    ding.report_notice(requests, 77, 'https://www.baidu.com')
