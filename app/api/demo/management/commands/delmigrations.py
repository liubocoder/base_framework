# -*- coding: utf-8 -*-
# FileName       : clearumdb.py
# Create Time    : 2024/5/27 10:37:56
# Create By      : liubo
"""
delmigrations.py 使用说明:
用于删除00xx migration文件
"""
import os
import sys

from django.apps import apps
from django.core.management.base import BaseCommand
from django.conf import settings


# 前期数据结构名称可能不固定，有时候需要重建表，用脚本命令快速重建表
# 特别注意  这里会删除表，仅用于开发前期测试
# 特别注意  这里会删除表，仅用于开发前期测试
# 特别注意  这里会删除表，仅用于开发前期测试

class Command(BaseCommand):
    # 这种方式只能删除django_migrations表中数据，无法删除已创建的表
    help = "特别注意  这里会删除表，仅用于开发前期测试！！！ 用于删除表，重建表 "
    myAppName = []

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument("apps", nargs="+", type=str, help="app列表 例如：app.api.demo")

    def get_apps(self):
        for app in apps.get_app_configs():
            if not app.name.startswith("app.api."):
                #self.stdout.write(f"ingore app: {app.name}")
                continue
            appShortName = app.name.split('.')[-1]
            if settings.DATABASE_APPS_MAPPING.get(appShortName, "default") != "default":
                # 忽略非default数据库的表
                continue

            if self.myAppName[0] != "all":
                if appShortName not in self.myAppName:
                    continue

            path = os.path.join(
                settings.BASE_DIR, "web_api", app.name.replace(".", "/"), "migrations"
            )
            if not os.path.exists(path):
                os.makedirs(path, 0o777, True)
                with open(os.path.join(path, "__init__.py"), "w+") as file:
                    file.write("")
                    file.flush()
            yield app, path

    def execute_command(self, command: str):
        self.stdout.write(f"run command: {command}")
        os.system(f"{sys.executable} {command}")

    def handle(self, *args, **options):
        self.myAppName = options.get("apps")

        self.stdout.write(f"=====apps={self.myAppName}， 目标的应用包括：")
        for app, path in self.get_apps():
            self.stdout.write(f"{app.name} --- {path}")

            try:
                ld = os.listdir(path)
                for it in ld:
                    if it.startswith("00"):
                        iniPath = os.path.join(path, it)
                        os.remove(iniPath)
                        self.stdout.write(f"remove: {iniPath}")
            except Exception as e:
                self.stderr.write(e)

        self.stdout.write("==================")

        self.stdout.write(self.style.SUCCESS(f"successfully deleted"))
