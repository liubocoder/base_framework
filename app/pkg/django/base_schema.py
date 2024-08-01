# -*- coding: utf-8 -*-
# FileName       : base_schema.py
# Create Time    : 2024/8/1 15:03:06
# Create By      : liubo
"""
base_schema.py 使用说明:
    一些通用的schema定义
"""


###########################通用响应###############################

# 普通操作响应
CommonResponseSchema = {
    200: {
        'type': 'object',
        'required': ['code'],
        'properties': {
            'code': {
                'type': 'integer',
                'example': 0,
                'title': '业务响应码 0成功 1失败'
            },
            'data': {
                'type': 'object',
                'title': '数据字段，可能是对象也可能是数组',
            }
        }
    },
    400: {
        'type': 'object',
        'required': ['code', 'message'],
        'properties': {
            'code': {
                'type': 'integer',
                'example': 0,
                'title': '业务响应码 0成功 1失败'
            },
            'message': {
                'type': 'string',
                'example': '操作失败',
                'title': '错误消息'
            },
            'errors': {
                'type': 'string',
                'example': 'sql insert failed',
                'title': '内部异常，仅在debug模式运行时返回'
            }
        }
    }
}

# 含有404错误的接口响应，一般含有path参数的情况出现
CommonResponseNotfoundSchema = dict(CommonResponseSchema)
CommonResponseNotfoundSchema[404] = {
    'type': 'object',
    'required': ['code', 'message'],
    'properties': {
        'code': {
            'type': 'integer',
            'example': 0,
            'title': '业务响应码 0成功 1失败'
        },
        'message': {
            'type': 'string',
            'example': '操作失败',
            'title': '错误消息'
        },
        'errors': {
            'type': 'string',
            'example': 'sql search not found',
            'title': '内部异常，仅在debug模式运行时返回'
        }
    }
}
