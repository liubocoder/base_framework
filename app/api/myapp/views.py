# Create your views here.


from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from app.api.myapp.models import Book
from app.api.myapp.serializers.serializer import MyBookSerializer
from app.pkg.django.base_filter_backends import ListFilterBackends, QFieldParamType, QField
from app.pkg.django.base_view_handler import HandleExcGenericAPIView
from app.pkg.django.response import CommonResponseSerializer, CommonResponseContent, CommonResponseStatusCode
from app.settings import logger


class MyDataListFilter(ListFilterBackends):
    name = QField(paramType=QFieldParamType.STR, description="名称")

    class Meta:
        order_by = ('-ctime',)


class MyAppViewSet(HandleExcGenericAPIView, ViewSet, viewsets.GenericViewSet,
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
        return Book.objects.all()

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return MyBookSerializer
        if self.action == 'create' or self.action == 'update':
            return MyBookSerializer
        return CommonResponseSerializer

    @extend_schema(
        tags=["MyApp-CRUD"],
        summary="功能类1【创建】",
        description="MyApp代码",
        request=MyBookSerializer,
        responses={200: CommonResponseSerializer}
    )
    def create(self, request, *args, **kwargs):
        logger.debug("myapp create")
        serial = MyBookSerializer(data=request.data)
        if serial.check_invalid():
            return serial.invalid_err_response()
        serial.save()
        ret = CommonResponseContent()
        ret.code = CommonResponseStatusCode.SUCCESS
        return Response(ret.to_dict(), status.HTTP_200_OK)

    @extend_schema(
        tags=["MyApp-CRUD"],
        summary="功能类1【更新】",
        description="MyApp代码",
        request=MyBookSerializer,
        responses={200: CommonResponseSerializer},
        parameters=[
            OpenApiParameter(name='id', description='数据id', type=int, location=OpenApiParameter.PATH),
        ]
    )
    def update(self, request, *args, **kwargs):
        logger.debug("myapp update")
        serial = MyBookSerializer(instance=self.get_object(), data=request.data)
        if serial.check_invalid():
            return serial.invalid_err_response()
        serial.save()
        ret = CommonResponseContent()
        ret.code = CommonResponseStatusCode.SUCCESS
        return Response(ret.to_dict(), status.HTTP_200_OK)

    @extend_schema(
        tags=["MyApp-CRUD"],
        summary="功能类1【详情】",
        description="MyApp代码",
        parameters=[
            OpenApiParameter(name='id', description='数据id', type=int, location=OpenApiParameter.PATH),
        ]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        tags=["MyApp-CRUD"],
        summary="功能类1【列表】",
        description="MyApp代码",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        tags=["MyApp-CRUD"],
        summary="功能类1【删除】",
        description="MyApp代码",
        parameters=[
            OpenApiParameter(name='id', description='数据id', type=int, location=OpenApiParameter.PATH),
        ],
        responses={204: CommonResponseSerializer}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
