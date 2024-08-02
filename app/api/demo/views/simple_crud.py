# -*- coding: utf-8 -*-
# FileName       : simple_crud.py
# Create Time    : 2024/8/1 14:52:07
# Create By      : liubo
"""
simple_crud.py 使用说明:

"""

from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from app.api.demo.models import MyDemoData
from app.api.demo.serializers.serializer import MyDemoDataRequestSerializer, MyDemoDataSerializer
from app.pkg.django.base_filter_backends import ListFilterBackends, QFieldParamType, QField
from app.pkg.django.base_view_handler import HandleExcGenericAPIView
from app.pkg.django.response import CommonResponseSerializer, CommonResponseContent, CommonResponseStatusCode
from app.settings import logger

class MyDataListFilter(ListFilterBackends):
    name = QField(paramType=QFieldParamType.STR, description="名称")
    factory = QField(paramType=QFieldParamType.INT, description="厂家")

    class Meta:
        order_by = ('-ctime', )

class SimpleCrudViewSet(HandleExcGenericAPIView, ViewSet, viewsets.GenericViewSet,
                        mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.ListModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin):
    permission_classes = []
    authentication_classes = []
    http_method_names = ['get', 'post', 'put', 'delete']
    lookup_field = "did"
    filter_backends = [MyDataListFilter]

    def get_queryset(self):
        # 这里可以做其他的过滤
        return MyDemoData.objects.all()

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return MyDemoDataSerializer
        if self.action == 'create' or self.action == 'update':
            return MyDemoDataRequestSerializer
        return CommonResponseSerializer

    @extend_schema(
        tags=["示例-CRUD"],
        summary="功能类1【创建】",
        description="示例代码",
        request=MyDemoDataRequestSerializer,
        responses={200: CommonResponseSerializer}
    )
    def create(self, request, *args, **kwargs):
        logger.debug("demo create")
        serial = MyDemoDataRequestSerializer(data=request.data)
        if serial.check_invalid():
            return serial.invalid_err_response()
        # 携带其他参数，例如用户认证信息等
        serial.save(mykey="otherdata")
        ret = CommonResponseContent()
        ret.code = CommonResponseStatusCode.SUCCESS
        return Response(ret.to_dict(), status.HTTP_200_OK)

    @extend_schema(
        tags=["示例-CRUD"],
        summary="功能类1【更新】",
        description="示例代码",
        request=MyDemoDataRequestSerializer,
        responses={200: CommonResponseSerializer},
        parameters=[
            OpenApiParameter(name='did', description='数据id', type=str, location=OpenApiParameter.PATH),
        ]
    )
    def update(self, request, *args, **kwargs):
        logger.debug("demo update")
        serial = MyDemoDataRequestSerializer(instance=self.get_object(), data=request.data)
        if serial.check_invalid():
            return serial.invalid_err_response()
        serial.save()
        ret = CommonResponseContent()
        ret.code = CommonResponseStatusCode.SUCCESS
        return Response(ret.to_dict(), status.HTTP_200_OK)

    @extend_schema(
        tags=["示例-CRUD"],
        summary="功能类1【详情】",
        description="示例代码",
        parameters=[
            OpenApiParameter(name='did', description='数据id', type=str, location=OpenApiParameter.PATH),
        ]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        tags=["示例-CRUD"],
        summary="功能类1【列表】",
        description="示例代码",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        tags=["示例-CRUD"],
        summary="功能类1【删除】",
        description="示例代码",
        parameters=[
            OpenApiParameter(name='did', description='数据id', type=str, location=OpenApiParameter.PATH),
        ],
        responses={204: CommonResponseSerializer}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)




