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

from app.api.demo.tasks import demo_app_task
from app.pkg.django.response import CommonResponseSerializer, CommonResponseContent, CommonResponseStatusCode
from app.settings import logger


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
        logger.debug("demo create")
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
        logger.debug(rdConn.ttl(k1))
        logger.debug(rdConn.get(k1))
        ret = CommonResponseContent()
        ret.code = CommonResponseStatusCode.SUCCESS
        return Response(ret.to_dict(), status.HTTP_200_OK)

    @extend_schema(
        tags=["示例-Celery操作"],
        summary="Celery测试",
        description="Celery测试",
    )
    @action(detail=False, methods=['get'], url_path='celery-func')
    def celery_func(self, request, *args, **kwargs):
        ret = CommonResponseContent()
        ret.code = CommonResponseStatusCode.SUCCESS
        logger.debug("celery_func")
        from celery.result import AsyncResult

        # celery的异步
        t_res: AsyncResult =demo_app_task.delay(1, 2)
        logger.debug(f"task_id={t_res.task_id}, status={t_res.status}")
        return Response(ret.to_dict(), status.HTTP_200_OK)
