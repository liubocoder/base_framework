# -*- coding: utf-8 -*-
# FileName       : my_comsumer.py
# Create Time    : 2024-08-19 15:51:42
# Created By     : liubo
"""
my_comsumer.py 使用说明:

"""

from channels.consumer import AsyncConsumer

class MySyncConsumer(AsyncConsumer):
    # 自定义别名 这里使用默认
    #channel_layer_alias = "mylayer"

    def __init__(self):
        self.group_name = None

    async def on_message(self, data):
        print(f"on_message: scope={self.scope}, chName={self.channel_name}, rcv={data}")
        await self.send(f"consumer send called, rcv={data}")

    async def connect(self, data):
        self.group_name = data["group_name"]
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        print(f"connected: {self.group_name}")

    async def disconnect(self, data):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        print(f"disconnected: {self.group_name}")

    async def inner_handler(self, *args, **kwargs):
        print(f"inner_handler: {self.scope}, args={args}, kwargs={kwargs}")