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


class WebsocketJwtAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        """
        参数为asgi的标准
        """
        # 处理ws的session
        session = scope.get("session")
        logger.debug(f"asgi session: {session}")
        # 注意处理数据库的问题 同步异步转换 @database_sync_to_async
        return await self.inner(scope, receive, send)


