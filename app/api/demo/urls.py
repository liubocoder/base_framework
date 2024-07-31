# -*- coding: utf-8 -*-
# FileName       : urls.py
# Create Time    : 2024-01-16 10:11:27
# Created By     : liubo
"""
urls.py 使用说明:
    路由路径管理
"""
from django.urls import path, include
from rest_framework import routers

from app.api.demo.views.some_work1_set import SomeWork1Set

demo_router = routers.DefaultRouter()
demo_router.register("some-work1", SomeWork1Set, basename="some_work1_set")


urlpatterns = [
    path("demo/", include(demo_router.urls)),
]
