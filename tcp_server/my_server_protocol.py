# -*- coding: utf-8 -*-
# FileName       : my_server_protocol.py
# Create Time    : 2024-08-19 15:52:00
# Created By     : liubo
"""
my_server_protocol.py 使用说明:

"""
import asyncio
import threading
import uuid

from twisted.internet import defer
from twisted.internet.protocol import Protocol, connectionDone
from twisted.python import failure

from tcp_server.my_comsumer import MySyncConsumer

def init_new_thread_worker():
    def thread_loop_task(loop):
        asyncio.set_event_loop(loop)
        loop.run_forever()

    loop = asyncio.new_event_loop()
    th = threading.Thread(target=thread_loop_task, args=(loop,))
    th.daemon = True
    th.start()
    return loop

loop = init_new_thread_worker()

class MyServerProtocol(Protocol):

    def __init__(self):
        self.application_queue = None

    def connectionMade(self):
        clnt = self.transport.getPeer().host
        print(f"TCP 新客户端连接：{clnt}")
        self.application_deferred = defer.maybeDeferred(
            self.createApplication,
            self,
            {"mytcp": "0.1-snapshort"}
        )
        self.application_deferred.addCallback(self.applicationCreateWorked)
        self.application_deferred.addErrback(self.applicationCreateFailed)

    def connectionLost(self, reason: failure.Failure = connectionDone) -> None:
        print("TCP 断开连接")
        if self.application_queue:
            self.application_queue.put_nowait({"type": "disconnect"})

    def dataReceived(self, data: bytes) -> None:
        dataStr = data.decode()
        print(f"TCP 接收数据：{dataStr}")
        print(self.application_queue)
        self.application_queue.put_nowait({"type": "on_message", "data": dataStr})

    async def send(self, msg):
        print(f"TCP 发送数据：{msg}")
        self.transport.write(str.encode(msg))

    def createApplication(self, protocol, scope):
        input_queue = asyncio.Queue()
        scope.setdefault("mytcp", {"version": "0.1"})
        application_instance = MySyncConsumer.as_asgi()(
            scope, input_queue.get, self.send
        )

        application_instance = asyncio.run_coroutine_threadsafe(application_instance, loop)
        print(f"create app: {application_instance}")
        return input_queue

    def applicationCreateWorked(self, application_queue):
        self.application_queue = application_queue
        application_queue.put_nowait({"type": "connect", "group_name": f"group-{uuid.uuid4()}"})
        print("application created")

    def applicationCreateFailed(self, failure):
        print(f"application failed: {failure}")
        return failure