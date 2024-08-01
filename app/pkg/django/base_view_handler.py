# -*- coding: utf-8 -*-
# FileName       : base_view_handler.py
# Create Time    : 2024/8/1 15:04:33
# Create By      : liubo
"""
base_view_handler.py 使用说明:

"""
import django.http
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.conf import settings

from app.pkg.django.response import CommonResponseContent
from app.settings import logger


class HandleExcGenericAPIView(APIView):
    """
    参数说明在Swagger各个接口参数的Schema中

    请求参数：
    ```
    参考Swagger Parameters 或 Request body
    ```
    响应数据：
    ```
    参考Swagger Responses
    ```
    """
    def dispatch(self, request, *args, **kwargs):
        """
        override APIView.dispatch，捕获业务代码的异常
        """
        self.args = args
        self.kwargs = kwargs
        request = self.initialize_request(request, *args, **kwargs)
        self.request = request
        self.headers = self.default_response_headers  # deprecate?

        try:
            self.initial(request, *args, **kwargs)

            # Get the appropriate handler method
            if request.method.lower() in self.http_method_names:
                handler = getattr(self, request.method.lower(),
                                  self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed

            try:
                response = handler(request, *args, **kwargs)
            except Exception as e:
                response = self.handle_business_exc(e)

        except Exception as exc:
            response = self.handle_exception(exc)

        self.response = self.finalize_response(request, response, *args, **kwargs)
        return self.response
    def handle_business_exc(self, exc):
        """
        处理业务异常
        """
        sCode = status.HTTP_400_BAD_REQUEST
        if isinstance(exc, django.http.Http404):
            sCode = status.HTTP_404_NOT_FOUND
            logger.debug(f"资源未找到：{exc}")
        ret = CommonResponseContent()
        ret.message = "操作失败"
        rd = ret.to_dict()
        if settings.DEBUG:
            rd["errors"] = f"{exc}"
        # 已知的异常不打印异常内存，例如404错误一般是 update、retrieve、destroy未找到资源
        if sCode == status.HTTP_400_BAD_REQUEST:
            logger.exception(exc)
            logger.error(rd)
        return Response(rd, status=sCode)