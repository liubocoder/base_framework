# -*- coding: utf-8 -*-
# FileName       : urls.py
# Create Time    : 2024-01-16 10:11:27
# Created By     : liubo
"""
urls.py 使用说明:
    基础路由路径管理
"""
from django.urls import path, include, re_path
from rest_framework import routers

from app.api.demo.views.simple_crud import SimpleCrudViewSet
from app.api.demo.views.some_work1_set import SomeWork1Set
from app.api.demo.views.simple_router import SimpleRouterViewSet

demo_router = routers.DefaultRouter()
demo_router.register("some-work1", SomeWork1Set, basename="some_work1_set")
demo_router.register("simple-crud", SimpleCrudViewSet, basename="simple_crud")
demo_router.register("simple-router", SimpleRouterViewSet, basename="simple_router")

urlpatterns = [
    # 上古写法，不再使用
    # url()

    # 注意如下写的方式优先级的考虑，未处理冲突问题，实际项目根据需求调整
    path("demo/", include(demo_router.urls)),
    path("demo/<str:did>/", SimpleRouterViewSet.as_view({"get": "url3"})),
    path("demo/<str:did>/<str:name>/", SimpleRouterViewSet.as_view({"get": "url4"})),

    re_path(r'^demo/abc/fac/(?P<factory>[0-9])/$', SimpleRouterViewSet.as_view({"get": "url5"})),
]

