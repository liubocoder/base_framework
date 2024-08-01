# -*- coding: utf-8 -*-
# FileName       : simple_router.py
# Create Time    : 2024/8/1 16:00:42
# Create By      : liubo
"""
simple_router.py 使用说明:

"""
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action

from app.api.demo.models import MyDemoData
from app.api.demo.serializers.serializer import MyDemoDataRequestSerializer, MyDemoDataSerializer
from app.pkg.django.base_filter_backends import ListFilterBackends, QFieldParamType, QField
from app.pkg.django.base_schema import CommonResponseSchema
from app.pkg.django.base_view_handler import HandleExcGenericAPIView
from app.pkg.django.response import CommonResponseSerializer, CommonResponseContent, CommonResponseStatusCode
from app.settings import logger

class SimpleRouterViewSet(HandleExcGenericAPIView, ViewSet, viewsets.GenericViewSet):

    permission_classes = []
    authentication_classes = []
    http_method_names = ['get']

    @extend_schema(tags=["示例-路由"], summary="单path", responses=CommonResponseSchema)
    @action(detail=False, methods=['get'], url_path=r'single/(?P<did>.+)')
    def url1(self, request, *args, **kwargs):
        ret = CommonResponseContent()
        rd = kwargs.copy()
        rd["action"] = self.action
        ret.data = rd
        logger.debug(kwargs)
        return Response(ret.to_dict())

    @extend_schema(tags=["示例-路由"], summary="中间path", responses=CommonResponseSchema)
    @action(detail=False, methods=['get'], url_path=r'(?P<did>.+)/midd')
    def url2(self, request, *args, **kwargs):
        ret = CommonResponseContent()
        rd = kwargs.copy()
        rd["action"] = self.action
        ret.data = rd
        logger.debug(kwargs)
        return Response(ret.to_dict())

    @extend_schema(tags=["示例-路由"], summary="path指定", responses=CommonResponseSchema)
    def url3(self, request, *args, **kwargs):
        ret = CommonResponseContent()
        rd = kwargs.copy()
        rd["action"] = self.action
        ret.data = rd
        logger.debug(kwargs)
        return Response(ret.to_dict())

    @extend_schema(tags=["示例-路由"], summary="多path参数指定", responses=CommonResponseSchema)
    def url4(self, request, *args, **kwargs):
        ret = CommonResponseContent()
        rd = kwargs.copy()
        rd["action"] = self.action
        ret.data = rd
        logger.debug(kwargs)
        return Response(ret.to_dict())

    @extend_schema(tags=["示例-路由"], summary="re_path", responses=CommonResponseSchema)
    def url5(self, request, *args, **kwargs):
        ret = CommonResponseContent()
        rd = kwargs.copy()
        rd["action"] = self.action
        ret.data = rd
        logger.debug(kwargs)
        return Response(ret.to_dict())