# -*- coding: utf-8 -*-
# FileName       : jwt.py
# Create Time    : 2024-08-19 14:14:38
# Created By     : liubo
"""
jwt.py 使用说明:

"""
from django.contrib.sessions.backends.cache import SessionStore
from rest_framework.authentication import BaseAuthentication

from app.api.auth.user import User
from app.settings import logger

class JwtAuthentication(BaseAuthentication):

    def authenticate(self, request):
        """
        自定义认证，返回：用户对象+认证信息（字典）
        """
        logger.debug(f"my auth: {request}")
        ss: SessionStore = request.session
        logger.debug(f"my session: {ss.items()}")
        # request 从中获取token，自定义session
        return User("zs", "dd"), {"mysession": "aa"}
