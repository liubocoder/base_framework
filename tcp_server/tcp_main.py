# -*- coding: utf-8 -*-
# FileName       : tcp_main.py
# Create Time    : 2024-08-19 15:44:40
# Created By     : liubo
"""
tcp_main.py 使用说明:
    用于测试使用asgi的接口规范实现tcp服务器
    仅用于学习使用，生产环境中可能直接使用python基础库实现tcp服务器可能性能更好一点。
    或者使用twisted的api，不使用Channel
"""
import os
from datetime import datetime

import django
from twisted.internet import reactor
from twisted.internet.protocol import ServerFactory

from tcp_server.my_server_protocol import MyServerProtocol

# 引入channel 使用django框架进行初始化
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()


def main():
    print(f"start-----{datetime.now()}")
    factory = ServerFactory()
    factory.protocol = MyServerProtocol

    reactor.listenTCP(6666, factory)
    reactor.run()

if __name__ == '__main__':
    main()