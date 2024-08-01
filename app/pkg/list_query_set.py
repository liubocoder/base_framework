# -*- coding: utf-8 -*-
# FileName       : list_query_set.py
# Create Time    : 2024/6/27 17:10:55
# Create By      : liubo
"""
list_query_set.py 使用说明:
    用于从列表中搜索数据
    1. 支持筛选条件
        contains、==(或equal)、>(或gt)、>=(或gte)、<(或lt)、<=(或lte)
    2. 支持order
        目前只支持按一个数据排序

    conditions = {
        "name__contains": "张",
        "id__>=": 3,
    }
    ListQuerySet.create([
            {"id": 8, "name": "张四", "ot": True},
            {"id": 12, "name": "王二", "ot": False},
            {"id": 3, "name": "张三", "ot": True},
        ]).filter(**conditions).order_by("-id").all()

    结果：
    [{'id': 8, 'name': '张四', 'ot': True}, {'id': 3, 'name': '张三', 'ot': True}]
"""
import jmespath
from app.settings import logger

sOperator = ["==", ">", ">=", "<", "<="]
sOrmOperator = {
    "equal": "==",
    "gt": ">",
    "gte": ">=",
    "lt": "<",
    "lte": "<="
}

class ListQuerySet:
    def __init__(self, data: list):
        self.data = data
        self.orderKey = None
        self.conditions = None

    @classmethod
    def create(cls, data: list):
        return ListQuerySet(data)
    def filter(self, **kwargs):
        self.conditions = kwargs
        return self

    def order_by(self, *orderKey: str):
        # 只支持按一个数据排序
        self.orderKey = orderKey[0]
        return self

    def all(self):
        ret = self.data

        expr = []
        if self.conditions:
            tempExpr = []
            for k, v in self.conditions.items():
                kk = k.split("__")
                if len(kk) == 1:
                    tempExpr.append(f"{kk[0]}==`{v}`")
                    continue
                if kk[1] == "contains":
                    tempExpr.append(f"contains({kk[0]}, '{v}')")
                elif kk[1] in sOperator:
                    tempExpr.append(f"{kk[0]}{kk[1]}`{v}`")
                elif kk[1] in sOrmOperator:
                    tempExpr.append(f"{kk[0]}{sOrmOperator[kk[1]]}`{v}`")
                else:
                    logger.warning(f"不支持的操作{k}")
            expr = f"[?{'&&'.join(tempExpr)}]"

        if self.orderKey:
            okeys = self.orderKey.split("-")
            if len(okeys) == 1:
                expr = f"sort_by({expr}, &{okeys[0]})"
            elif len(okeys) == 2:
                expr = f"reverse(sort_by({expr}, &{okeys[1]}))"
            else:
                logger.warning(f"无效的排序字段{self.orderKey}")
                return ret
        logger.debug(expr)
        if expr == "[]":
            return ret
        return jmespath.search(expr, ret)