# -*- coding: utf-8 -*-
# FileName       : schema_parser.py
# Create Time    : 2024/6/26 09:43:28
# Create By      : liubo
"""
schema_parser.py 使用说明:
    用于将json的数据转换为swagger的schema属性

    示例
    respJson = {
      "xnmId": "local-xnm-system-id-1", #运管系统ID（这里属于扩展字段，目前是将字段放入title中）
      "level": "1",         #运管系统级别
      "stationInfos": [     #运管下的站点信息
        {
          "stationId": "test-stationid-1" #站点ID
        }
      ]
    }
    demoSchema = jsonToSchema(respJson)

    在某个view中使用
    @extend_schema(tags=["xx模块"], summary="业务", responses={200: demoSchema})
"""
import json
import re

import django.conf


def jsonToSchema(respJson):
        try:
            checkJs = ""
            ll = respJson.splitlines()
            for it in ll:
                line = it
                sharpIdx = line.find("#")
                if sharpIdx != -1:

                    lineSchema = line[sharpIdx+1:]
                    line = line[:sharpIdx]
                    kvs = line.split(":")

                    pattern = r'\'(.*?)\'|\"(.*?)\"'
                    result = re.findall(pattern, line)
                    content = [item[0] if item[0] else item[1] for item in result]
                    key = content[0]

                    if kvs[0].find(key) == -1:
                        raise Exception(f"未找到key, k={kvs[0]}, c={content}")

                    kvs[0] = kvs[0].replace(key, f'{key}__{lineSchema}')
                    line = ":".join(kvs)
                checkJs += (line + "\n")
            try:
                dd = json.loads(checkJs)
            except Exception as e:
                print("异常的json: ")
                print(checkJs)
                raise Exception(e, "json.loads执行失败，请检查json格式是否错误")
            schema = jsonSchemaObj(dd)
            #print(json.dumps(schema, indent=2, ensure_ascii=False))
            return schema
        except Exception as e:
            if django.conf.settings.DEBUG:
                raise e
            else:
                print(e)


def jsonSchemaObj(obj, title=None)->dict:
    schema = {}
    if title:
        schema["title"] = title
    if isinstance(obj, list):
        schema["type"] = "array"
        schema["items"] = jsonSchemaObj(obj[0])
        return schema
    if isinstance(obj, int) or isinstance(obj, float):
        schema["type"] = "number"
        schema["example"] = obj
        return schema
    elif isinstance(obj, str):
        schema["type"] = "string"
        schema["example"] = obj
        return schema
    schema["type"] = "object"
    props = {}
    schema["properties"] = props
    requiredKeys = []
    for k, v in obj.items():
        ks = k.split("__")
        key = k
        title = None
        if len(ks) >= 2:
            key = ks[0]
            # ks[1] 是额外信息存放方案，比如后续可以扩展非必要选项
            title = ks[1]
        requiredKeys.append(key)

        if isinstance(v, int) or isinstance(obj, float):
            props[key] = {
                "type": "number",
                "example": v,
            }
            if title:
                props[key]["title"] = title
        elif isinstance(v, str):
            props[key] = {
                "type": "string",
                "example": v,
            }
            if title:
                props[key]["title"] = title
        elif isinstance(v, list):
            props[key] = jsonSchemaObj(v, title=title)
        elif isinstance(v, object):
            props[key] = jsonSchemaObj(v, title=title)

    schema["required"] = requiredKeys
    return schema
