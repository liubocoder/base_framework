# -*- coding: utf-8 -*-
# FileName       : pagination.py
# Create Time    : 2024/8/1 15:08:12
# Create By      : liubo
"""
pagination.py 使用说明:

"""

from rest_framework import pagination
from rest_framework.response import Response

from app.pkg.django.response import CommonResponseContent, CommonResponseStatusCode


class LocalTablePagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = "pageSize"

    page_query_description = '分页数据：页码1-n，默认1'
    page_size_query_description = '分页数据：每页的大小，默认10'

    def get_paginated_response_schema(self, schema):
        """
        重写分页swagger scema
        """
        return {
            'type': 'object',
            'required': ['code', 'data'],
            'properties': {
                'code': {
                    'type': 'integer',
                    'example': 0,
                    'title': "业务响应码 0成功 1失败"
                },
                'data': {
                    'type': 'object',
                    'required': ['recordTotal', 'pageSize', 'page', 'results'],
                    'properties': {
                        'recordTotal': {
                            'type': 'integer',
                            'example': 1,
                            'title': "数据总条数"
                        },
                        'pageSize': {
                            'type': 'integer',
                            'example': 10,
                            'title': "分页大小"
                        },
                        'page': {
                            'type': 'integer',
                            'example': 1,
                            'title': "当前页码"
                        },
                        'records': schema
                    }
                }
            }
        }

    def get_paginated_response(self, data):
        """
        重写分页数据返回结果
        """
        return Response(CommonResponseContent(code=CommonResponseStatusCode.SUCCESS, data={
            "recordTotal": self.page.paginator.count,
            "pageSize": self.page_size,
            "page": self.page.number,
            "records": data
        }).to_dict())