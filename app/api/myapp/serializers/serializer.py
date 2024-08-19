# -*- coding: utf-8 -*-
# FileName       : serializer.py
# Create Time    : 2024/8/1 15:18:11
# Create By      : liubo
"""
serializer.py 使用说明:

"""

from rest_framework import serializers

from app.api.myapp.models import Book
from app.pkg.django.base_request_serializer import BaseRequestSerializerMixin


class MyBookSerializer(serializers.ModelSerializer, BaseRequestSerializerMixin):
    class Meta:
        model = Book
        fields = '__all__'