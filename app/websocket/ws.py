# -*- coding: utf-8 -*-
# FileName       : ws.py
# Create Time    : 2024-08-19 15:21:27
# Created By     : liubo
"""
ws.py 使用说明:

"""

from channels.generic.websocket import AsyncJsonWebsocketConsumer

from app.settings import logger

class WsConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        # 可以判断session，合法连接才允许接入
        logger.debug(f"ws con: {self.scope}")
        if False:
            self.close()
            return
        await super().connect()

    async def disconnect(self, code):
        logger.debug("ws discon")

    async def receive_json(self, content, **kwargs):
        logger.debug(f"ws rcv: {content}")