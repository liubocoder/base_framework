# -*- coding: utf-8 -*-
# FileName       : router.py
# Create Time    : 2024-08-19 10:20:49
# Created By     : liubo
"""
router.py 使用说明:
    用于对不同业务进行数据库路由
    1. 可以实现分库
    2. 读写分离
    ...
"""


class DbRouter(object):

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'myapp':
            return 'libdb'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'myapp':
            return 'libdb'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        #TODO 这里示例项目仅简单处理
        if obj1._meta.app_label == obj2._meta.app_label:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        db 数据库名称
        app_label 应用简称
        """
        if db == 'libdb':
            return app_label == 'myapp'
        if app_label == 'myapp':
            # 如果App与db不匹配，则不允许迁移
            return False
        return None