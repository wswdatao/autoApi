# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
------------------------------------------
    Description :
    File Name : get_config
    Author : Dade
    Create Time : 2023/2/13 18:09
------------------------------------------
    Change Activity:
        Modifier: 
        Modify time: 2023/2/13 18:09
------------------------------------------
"""

import configparser
from get_path import get_path
from get_platform import get_platform


class GetConfig:

    def __init__(self):
        self.way = get_platform()
        self.config = configparser.ConfigParser()
        self.default_dir = get_path() + f'{self.way}config{self.way}'       # 指定配置文件路径

    def get_config_sections(self, file_name):
        """
            根据传入的配置文件名，获取配置文件内所有section，以列表形式返回
        :param file_name: config文件名
        :return: 所有的 section列表
        """
        self.config.read(self.default_dir + file_name, encoding='GBK')      # 读取指定config文件
        sections = [i for i in self.config if i != 'DEFAULT']
        return sections

    def get_options(self, file_name, section):
        """
            根据指定的配置文件名和 section，获取 section下的options信息，以字典形式返回
        :param file_name: config文件名
        :param section: 指定 section名
        :return: 所有的 options字典
        """
        infos = {}
        self.config.read(self.default_dir + file_name, encoding='GBK')      # 读取指定config文件
        for key in self.config.options(section):
            infos[key] = self.config[section][key]
        return infos


if __name__ == '__main__':
    config = GetConfig()
    print(config.get_options('config', 'DATABASE_MONGO'))
    print(config.get_options('config', 'ENV'))
