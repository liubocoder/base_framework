# -*- coding: utf-8 -*-
# FileName       : showm.py
# Create Time    : 2024/5/28 09:21:52
# Create By      : liubo
"""
showm.py 使用说明:
    测试django框架的自定义命令
"""


import os

from django.apps import apps
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = "show migrations"

    def get_apps(self):
        for app in apps.get_app_configs():
            if not app.name.startswith("app.api"):
                continue
            ns = app.name.split(".")
            path = os.path.join(
                settings.BASE_DIR, *ns, "migrations"
            )
            if os.path.exists(path):
                yield app, path
            else:
                self.printInfo(f"app->{app.name}, migration not exist")

    def handle(self, *args, **options):
        self.printInfo("begin handle")
        iterF = self.get_apps()
        for app, p in iterF:
           self.printInfo(f"app->{app.name}, migrationsPath->{p}")
        self.printInfo("end handle")

    def printInfo(self, msg: str):
        self.stdout.write(msg)