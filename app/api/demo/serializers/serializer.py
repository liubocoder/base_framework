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

class MyDemoDataSerializer(serializers.ModelSerializer):
    myJson = serializers.SerializerMethodField(label="json数据")

    @extend_schema_field(OpenApiTypes.ANY)
    def get_myJson(self, obj):
        td = obj.myTextData
        if td:
            return json.loads(td)
        return {}

    class Meta:
        model = MyDemoData
        #fields = '__all__'
        exclude = ('myTextData', )