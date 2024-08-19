# -*- coding: utf-8 -*-
# FileName       : router.py
# Create Time    : 2024-08-19 10:20:49
# Created By     : liubo
"""
router.py 使用说明:

"""


class DbRouter(object):

    def db_for_read(self, model, **hints):
        ...

    def db_for_write(self, model, **hints):
        ...

    def allow_relation(self, obj1, obj2, **hints):
        ...

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        db 数据库名称
        app_label 应用简称
        """
        ...