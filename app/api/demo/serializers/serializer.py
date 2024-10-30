# -*- coding: utf-8 -*-
# FileName       : serializer.py
# Create Time    : 2024/8/1 15:18:11
# Create By      : liubo
"""
serializer.py 使用说明:

"""
import json

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from app.api.demo.models import MyDemoData
from app.pkg.django.base_request_serializer import BaseRequestSerializerMixin
from app.pkg.schema_parser import jsonToSchema


class MyDemoChildData(serializers.Serializer):
    data1 = serializers.CharField(required=False, allow_blank=True, allow_null=True, default="")
    data2 = serializers.CharField(required=False, allow_null=True, allow_blank=True, default="")

    class Meta:
        fields = "__all__"

class MyDemoDataRequestSerializer(serializers.Serializer, BaseRequestSerializerMixin):
    name = serializers.CharField(max_length=64, label="名称")
    factory = serializers.IntegerField(min_value=1, max_value=10, label="厂家")
    myJson = MyDemoChildData(label="json数据", required=True)

    def update(self, instance, validated_data):
        setattr(instance, "name", validated_data["name"])
        setattr(instance, "factory", validated_data["factory"])
        setattr(instance, "myTextData", json.dumps(validated_data["myJson"]))
        instance.save()
        return instance

    def create(self, validated_data):
        mdd = MyDemoData(name=validated_data["name"], factory=validated_data["factory"],
                   myTextData=json.dumps(validated_data["myJson"]))
        mdd.save()
        return mdd

    class Meta:
        fields = "__all__"


class MyJsonField(serializers.DictField):
    _spectacular_annotation = None
    def __init__(self, **kwargs):
        js = kwargs.pop("jsonSchema", None)
        if js:
            self._spectacular_annotation = {"field": jsonToSchema(js)}
        super().__init__(**kwargs)

    def to_representation(self, value):
        return json.loads(value) if value else None

class MyMethodField(serializers.SerializerMethodField):
    _spectacular_annotation = None

    def __init__(self, **kwargs):
        js = kwargs.pop("jsonSchema", None)
        if js:
            self._spectacular_annotation = {"field": jsonToSchema(js)}
        super().__init__(**kwargs)

class MyDemoDataSerializer(serializers.ModelSerializer):
    field1 = """
        {
            "a": 1,  #测试数据
            "aa": [1,2,3], #测试数组
            "obj": {
                "b": "dddd" # 测试对象
            },
            "objArr": [ #测试对象数组
                {
                    "c": "ccccc" # 测试数据
                }
            ]
        }
        """
    myTextData = MyJsonField(label="测试json", jsonSchema=field1)
    myMethod = MyMethodField(label="测试method", jsonSchema=field1)

    def get_myMethod(self, obj):
        return {
            "aa": 11
        }

    class Meta:
        model = MyDemoData
        fields = '__all__'
        #exclude = ('myTextData', )