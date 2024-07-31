# -*- coding: utf-8 -*-
# FileName       : response.py
# Create Time    : 2024/7/31 09:58:28
# Create By      : liubo
"""
response.py 使用说明:
    通用的响应结构
"""

import copy
import enum
from typing import Any

from rest_framework import serializers


class CommonResponseStatusCode:
    SUCCESS = 0
    FAILED = 1


class CommonResponseContent(object):
    def __init__(self, **kwargs):
        self.code: int = kwargs.get("code", CommonResponseStatusCode.FAILED)
        self.message: str = kwargs.get("message", None)
        self.data: Any = kwargs.get("data", None)

    def __str__(self):
        return str(self.to_dict())

    def to_dict(self):
        data_dict = vars(self).copy()
        if self.data is None:
            data_dict.pop("data", None)
        if self.message is None:
            data_dict.pop("message", None)
        return data_dict

class CommonResponseSerializer(serializers.Serializer):
    code = serializers.IntegerField(read_only=True, label="回应状态", help_text="回应状态码")
    message = serializers.CharField(read_only=True, label="错误消息", required=False)
    data = serializers.DictField(read_only=True, label="数据", required=False)

    def to_internal_value(self, data):
        return CommonResponseContent(**data)

    def to_representation(self, instance: CommonResponseContent):
        return instance.to_dict()

    def get_fields(self):
        declared_fields = copy.deepcopy(self._declared_fields)
        return declared_fields

    class Meta:
        fields = "__all__"