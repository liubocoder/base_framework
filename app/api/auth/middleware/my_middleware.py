# -*- coding: utf-8 -*-
# FileName       : my_middleware.py
# Create Time    : 2024-08-19 14:05:47
# Created By     : liubo
"""
my_middleware.py 使用说明:

"""
from django.utils.deprecation import MiddlewareMixin

from app.settings import logger

class MyMiddleware(MiddlewareMixin):
    def process_request(self, request):
        logger.debug(f"custom middleware: request={request}")
