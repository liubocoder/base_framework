# -*- coding: utf-8 -*-
# FileName       : some_work1_set.py
# Create Time    : 2024-01-16 10:14:04
# Created By     : liubo
"""
some_work1_set.py 使用说明:
    测试一些业务
"""
from django_redis import get_redis_connection
from drf_spectacular.utils import extend_schema
from redis import Redis
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

import logging

from app.pkg.django.response import CommonResponseSerializer, CommonResponseContent, CommonResponseStatusCode


class SomeWork1Set(ViewSet, viewsets.GenericViewSet, mixins.CreateModelMixin):
    permission_classes = []
    authentication_classes = []
    http_method_names = ['get', 'post']

    @extend_schema(
        tags=["示例-CRUD"],
        summary="功能类1【创建】",
        description="示例代码",
        responses=CommonResponseSerializer,
    )
    def create(self, request, *args, **kwargs):
        logging.debug("demo create")
        ret = CommonResponseContent()
        ret.code = CommonResponseStatusCode.SUCCESS
        return Response(ret.to_dict(), status.HTTP_200_OK)

    @extend_schema(
        tags=["示例-Redis操作"],
        summary="Redis测试",
        description="Redis测试",
    )
    @action(detail=False, methods=['get'], url_path='redis-func')
    def redis_func(self, request, *args, **kwargs):
        rdConn: Redis = get_redis_connection()
        k1 = "foo1"
        rdConn.set(k1, "value1", ex=10)
        logging.debug(rdConn.ttl(k1))
        logging.debug(rdConn.get(k1))
        ret = CommonResponseContent()
        ret.code = CommonResponseStatusCode.SUCCESS
        return Response(ret.to_dict(), status.HTTP_200_OK)
