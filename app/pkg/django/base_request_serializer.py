# -*- coding: utf-8 -*-
# FileName       : base_request_serializer.py
# Create Time    : 2024/8/1 15:01:00
# Create By      : liubo
"""
base_request_serializer.py 使用说明:
    BaseRequestSerializerMixin 参数序列化的mixin，用于统一在参数校验失败的返回情况
    BatchDelSerializer 批量删除的序列化类
"""
from app.settings import logger
from rest_framework import status
from rest_framework.response import Response

from django.conf import settings

from app.pkg.django.response import CommonResponseContent


class BaseRequestSerializerMixin:
    """
    使用方式
    1. 业务Serializer类 继承 BaseRequestSerializerMixin
    2. 实例化Serializer后，调用check_invalid
    3. check_invalid返回True，直接返回invalid_err_response
    """
    checked_status = None
    def check_invalid(self) -> bool:
        """
        检查数据是否无效
        """
        self.checked_status = self.is_valid()
        return self.checked_status is False

    def invalid_err_response(self, message="参数错误"):
        ret = CommonResponseContent()
        ret.message = message
        rd = ret.to_dict()
        if self.checked_status is None:
            rd["errors"] = "check_invalid函数未调用"
        elif self.checked_status is False:
            logger.error(self.errors)
            if settings.DEBUG:
                rd["errors"] = self.errors
        else:
            rd["errors"] = "参数有效，检查代码逻辑"
        return Response(rd, status.HTTP_400_BAD_REQUEST)

