# -*- coding: utf-8 -*-
# FileName       : handler.py
# Create Time    : 2024/7/23 11:15:04
# Create By      : liubo
"""
handler.py 使用说明:

"""

import logging
from loguru import logger

class InterceptTimedRotatingFileHandler(logging.Handler):
    """
    自定义反射时间回滚日志记录器
    缺少命名空间
    """
    def __init__(self):
        super(InterceptTimedRotatingFileHandler, self).__init__()

    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        # 把当前帧的栈深度回到发生异常的堆栈深度，不然就是当前帧发生异常而无法回溯
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


