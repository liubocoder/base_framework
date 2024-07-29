# -*- coding: utf-8 -*-
# FileName       : handler.py
# Create Time    : 2024/7/23 11:15:04
# Create By      : liubo
"""
handler.py 使用说明:

"""

import logging
import os.path
from loguru import logger

from app.settings import LOGGING_FILE_MAX_AGE, LOGGING_FILE_MAX_SIZE, LOG_FORMAT


class InterceptTimedRotatingFileHandler(logging.Handler):
    """
    自定义反射时间回滚日志记录器
    缺少命名空间
    """
    def __init__(self, filename, encoding="utf-8", delay=False):
        super(InterceptTimedRotatingFileHandler, self).__init__()
        #print("bind filename: ", filename)
        filename = os.path.abspath(filename)
        # 需要本地用不同的文件名做为不同日志的筛选器
        self.logger_ = logger.bind(sime=filename)
        self.logger_.remove()
        self.filename = filename
        self.logger_.add(
            filename,
            retention="%s days" % (LOGGING_FILE_MAX_AGE),
            encoding=encoding,
            rotation="%s MB" % (LOGGING_FILE_MAX_SIZE),
            compression="zip",
            delay=delay,
            format=LOG_FORMAT,
            enqueue=True,
        )

    def emit(self, record):
        try:
            level = self.logger_.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        # 把当前帧的栈深度回到发生异常的堆栈深度，不然就是当前帧发生异常而无法回溯
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        self.logger_.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


