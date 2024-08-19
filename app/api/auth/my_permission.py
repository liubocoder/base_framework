# -*- coding: utf-8 -*-
# FileName       : my_permission.py
# Create Time    : 2024-08-19 14:10:22
# Created By     : liubo
"""
my_permission.py 使用说明:

"""
from rest_framework.permissions import BasePermission

from app.settings import logger

class MyPermission(BasePermission):
    def has_permission(self, request, view):
        # 认证过后进入权限判断
        # 自定义权限 结合用户等其他情况
        logger.debug(f"my permission: {view}")
        if hasattr(view, "action"):
            if view.action == "nopermission":
                return False
        return super().has_permission(request, view)