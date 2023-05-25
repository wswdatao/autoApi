# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
------------------------------------------
    Description :
    File Name : read_yaml
    Author : Dade
    Create Time : 2023/2/13 17:54
------------------------------------------
    Change Activity:
        Modifier: 
        Modify time: 2023/2/13 17:54
------------------------------------------
"""

import os
import yaml
from get_path import get_path
from get_platform import get_platform
from util.process_param import regular


class ReadYAML:

    def __init__(self):
        self.yaml = yaml
        self.way = get_platform()
        self.path = get_path() + f'{self.way}data{self.way}cases_library{self.way}'

    def get_all_files(self):
        """
            获取所有yaml用例文件并返回
        :return:            文件列表
        """

        all_dir = os.listdir(self.path)
        files = []
        for file in all_dir:
            try:
                temp_path = [file + self.way + i for i in os.listdir(self.path+file)]
                files = [*files, *temp_path]
            except NotADirectoryError:
                continue
        files_path = [i for i in files if '.yaml' in i]
        # files_path += [i for i in files if '调试时指定文件.yaml' in i]
        return files_path

    def load_cases(self):
        """
            获取所有状态为True的用例，添加到执行用例列表中返回
        :return:            执行用例列表
        """
        files = self.get_all_files()
        cases = []
        for name in files:
            temp = regular(self.safe_load(self.path, name))
            for case in temp:
                temp_status = temp[case]["case_status"]
                if temp_status:
                    cases.append(temp[case])
        return cases

    def safe_load(self, path, file_name):
        """
            传入需要读取的yaml文件名，返回读取文件内容
        :param path:        文件地址
        :param file_name:   文件名
        :return:            文件内容
        """
        yaml_file = path + file_name
        with open(yaml_file, encoding='GBK') as f:
            content = self.yaml.safe_load(f)
        return content

    def save_cache_cases(self):
        """
            缓存用例池数据，将读取的用例数据写入到用例池文件中，后续通过递归组装用例场景
        :return:
        """
        cases = {}
        files = self.get_all_files()
        for name in files:
            temp = regular(self.safe_load(self.path, name))
            cases = {**cases, **temp}
        path, name = get_path(), f'{self.way}cache{self.way}cache_cases'
        with open(path + name, 'w') as f:
            self.yaml.dump(cases, stream=f, default_flow_style=False, encoding='GBK', allow_unicode=True)
        cache_cases = self.safe_load(path, f'{self.way}cache{self.way}cache_cases')
        return cache_cases

    def write_yaml(self, content, path):
        """
            快速生成yaml格式的用例文件，可直接复制贴到用例集中调整(注意-eq 需要手动调整为列表形式)
            暂未使用 预留
        :param content:     接口入参
        :param path:        生成的文件名
        """
        default = {
                    "case_name": {
                        "allure": {
                            "feature": "",
                            "severity": "blocker",
                            "story": "",
                            "title": ""
                        },
                        "case_id": "",
                        "case_status": False,
                        "host": "${host}",
                        "url": "",
                        "method": "POST",
                        "file_path": "${path}具体路径",
                        "data": "",
                        "dependency_status": False,
                        "dependency_case": {
                            "dependency_id": "word_manage_02",
                            "dependency_data": [
                                {
                                    "dependency_type": "response",
                                    "jsonpath": "$.data.list[(@.length-1)].id",
                                    "replace_key": "typeId",
                                    "sql": ""
                                }
                            ]
                        },
                        "assert": {
                            "jsonpath": "$.message",
                            "type": "==",
                            "value": "请求成功",
                            "assert_type": "response"
                        },
                        "sql":  ""
                    }
        }
        default["case_name"]['data'] = content
        yaml_path = self.path + path
        with open(yaml_path, 'a') as f:
            return self.yaml.dump(default, stream=f, default_flow_style=False, encoding='GBK', allow_unicode=True)


if __name__ == '__main__':
    rd = ReadYAML()
   # print(rd.load_cases())
    # rd.save_cache_cases()
