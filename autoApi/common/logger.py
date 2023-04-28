# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
------------------------------------------
    Description :
    File Name : logger
    Author : Dade
    Create Time : 2023/2/13 17:42
------------------------------------------
    Change Activity:
        Modifier: 
        Modify time: 2023/3/14 16:42
------------------------------------------
"""

import os
import time
import logging
from get_path import get_path
from loguru import logger


class IntegrationAllure(logging.Handler):

    def emit(self, record) -> None:
        logging.getLogger(record.name).handle(record)


logger.add(
            os.path.join(get_path(), 'log', time.strftime('%Y_%m_%d_') + 'cms.log'),
            level='INFO',
            rotation='5 MB',
            enqueue=True,
            encoding="utf-8",
        )                                                                           # 配置loguru的基础配置
logger.add(IntegrationAllure(), format="{time:YYYY-MM-DD HH:mm:ss} | {message}")    # 引入logging的handle将日志集成到allure
