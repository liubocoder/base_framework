# -*- coding: utf-8 -*-
# FileName       : base_filter_backends.py
# Create Time    : 2024/8/1 14:59:46
# Create By      : liubo
"""
base_filter_backends.py 使用说明:
    自定义一个过滤器，方便list业务的过滤功能
    用于自动处理搜索条件和swagger的文档，仅影响mixins.ListModelMixin

    使用示例如下：

    from app.utils.django.base_filter_backends import ListFilterBackends, QFieldParamType, QField, QListField

    class MyFilterBackends(ListFilterBackends):
        fooStr = QField(paramType=QFieldParamType.STR, description="测试str类型数据，模糊匹配", lookup_expr="icontains")
        fooInt = QField(paramType=QFieldParamType.INT, description="测试int类型数据，精确匹配")
        fooGt = QField(paramType=QFieldParamType.INT, model_name="xxdata", description="测试大于判断", lookup_expr=">")
        fooDatetime = QField(paramType=QFieldParamType.DATETIME, description="时间判断", lookup_expr="<=")
        fooRange = QListField(paramType=QFieldParamType.DATETIME, model_name="xxIntVal",
                          description="范围判断，区间可支持数字和时间", lookup_expr='[]')

        # 可选
        class Meta:
            # 模型会覆盖view传入的queryset（可选）
            model = DemoModel
            # 注意这里是按xxfield降序，必须是tuple类型（可选）
            order_by = ("-xxfield", )

    class DemoViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
        queryset = DemoModel.objects.all()
        #或者重写get_queryset函数，
        #def get_queryset(self):
        #   ...
        #   当需要将已有的列表数据以分页list形式返回时，也可以用app.utils.list_query_set.ListQuerySet类
        #   ListQuerySet 目前仅支持QField的STR和数字类型的全匹配、模糊匹配（contains）、大于(等于)、小于(等于)
        #   return ListQuerySet.create([{"fooInt": 1}, {"fooInt": 2}])
        filter_backends = [MyFilterBackends]
"""
import enum
from collections import OrderedDict

from app.settings import logger
from rest_framework import filters


class QFieldParamType(enum.Enum):
    INT = 1
    STR = 2
    FLOAT = 3
    DATETIME = 4
    DATE = 5


_QFieldParamSchemaMap = {
    QFieldParamType.INT: {"type": "integer"},
    QFieldParamType.STR: {"type": "string"},
    QFieldParamType.FLOAT: {"type": "number", "format": "float"},
    QFieldParamType.DATETIME: {"type": "string", "format": "date-time"},
    QFieldParamType.DATE: {"type": "string", "format": "date"},
}

_CompareMarks = {">": "gt", ">=": "gte", "<": "lt", "<=": "lte"}
_ListCompareMarks = ["()", "(]", "[)", "[]", "in"]

class QField:
    """
    :param paramType: 参数类型 QFieldParamType
    :param name: web传入的参数名称，默认使用自定义过滤类定义的参数名称
    :param required: 是否必填，默认False （swagger使用）
    :param description: 参数描述（swagger使用）
    :param default: 默认值（swagger使用）
    :param model_name: 模型内成参数名称，默认使用name
    :param lookup_expr: 过滤时的条件，支持orm的过滤条件，可以用时">",">=","<", "<="表示orm的操作符，默认动作是全匹配
    """
    def __init__(self, paramType: QFieldParamType, name=None, required=False, description="",
                 default=None, model_name=None, lookup_expr=None):
        self.name = name
        self.model_name = model_name
        self.required = required
        self.description = description
        self.default = default
        self.paramType = paramType
        self.lookup_expr = lookup_expr

    def to_oper_parameters(self):
        return {
            "name": self.name,
            "required": self.required,
            "in": "query",
            "description": self.description,
            "schema": self._to_schema()
        }

    def take_query_data(self, params) -> dict:
        pv = params.get(self.name)
        conditions = {}
        if pv is None:
            return conditions
        mName = self.name if self.model_name is None else self.model_name
        if self.lookup_expr is None:
            conditions[f"{mName}"] = pv
        else:
            le = _CompareMarks.get(self.lookup_expr, self.lookup_expr)
            conditions[f"{mName}__{le}"] = pv

        return conditions

    def _to_schema(self):
        ret = dict(_QFieldParamSchemaMap[self.paramType])
        if self.default:
            ret["default"] = self.default
        return ret

class QListField(QField):
    """
    参数可以参考 QField，不能配置默认参数
    该参数用于配置范围型查询条件，范围的定义为：
    1. 目标值包含在List中，使用in，比如 x in [a, b, c]
    2. 目标值包含在List的取值范围中，使用[]，比如  [a < x < b ]

    :param lookup_expr: 滤时条件，包括"()", "(]", "[)", "[]", "in"，默认为in
    """
    def __init__(self, paramType: QFieldParamType, name=None, required=False, description="",
                 default=None, model_name=None, lookup_expr=None):
        if lookup_expr is None:
            lookup_expr = "in"
        assert lookup_expr in _ListCompareMarks, f"无效的lookup_expr参数: {lookup_expr}"
        super().__init__(paramType, name, required, description, None, model_name, lookup_expr)

    def take_query_data(self, params) -> dict:
        pv = params.getlist(self.name)
        conditions = {}
        if pv is None:
            return conditions
        mName = self.name if self.model_name is None else self.model_name
        if self.lookup_expr is None:
            conditions[f"{mName}__in"] = pv
        else:
            if self.lookup_expr == "in":
                conditions[f"{mName}__in"] = pv
            else:
                if len(pv) != 2:
                    return conditions
                if self.lookup_expr == "()":
                    conditions[f"{mName}__gt"] = pv[0]
                    conditions[f"{mName}__lt"] = pv[1]
                elif self.lookup_expr == "(]":
                    conditions[f"{mName}__gt"] = pv[0]
                    conditions[f"{mName}__lte"] = pv[1]
                elif self.lookup_expr == "[)":
                    conditions[f"{mName}__gte"] = pv[0]
                    conditions[f"{mName}__lt"] = pv[1]
                elif self.lookup_expr == "[]":
                    conditions[f"{mName}__gte"] = pv[0]
                    conditions[f"{mName}__lte"] = pv[1]

        return conditions

    def _to_schema(self):
        return {"type": "array", "items": super()._to_schema()}

class FilterSetOptions:
    def __init__(self, options=None):
        self.model = getattr(options, "model", None)
        self.order_by = getattr(options, "order_by", None)


class FilterMetaclass(type):
    def __new__(cls, name, bases, attrs):
        attrs["_declared_filters"] = cls.get_declared_filters(bases, attrs)

        new_class = super().__new__(cls, name, bases, attrs)
        new_class._meta = FilterSetOptions(getattr(new_class, "Meta", None))
        return new_class

    @classmethod
    def get_declared_filters(cls, bases, attrs):
        collects = {}
        for it in bases:
            if hasattr(it, "_declared_filters"):
                collects.update(it._declared_filters)
        fs = [
            (filter_name, attrs.pop(filter_name))
            for filter_name, obj in list(attrs.items())
            if isinstance(obj, QField)
        ]

        for filter_name, f in fs:
            if getattr(f, "name", None) is None:
                f.name = filter_name

        collects.update(fs)
        return OrderedDict(collects)


class ListFilterBackends(filters.BaseFilterBackend, metaclass=FilterMetaclass):
    _meta = None
    _declared_filters = None

    def filter_queryset(self, request, queryset, view):
        if view.action != 'list':
            return queryset
        if self._meta and self._meta.model:
            queryset = self._meta.model.objects

        if request.query_params is None:
            return self._order_query_set(queryset)

        params = request.query_params
        conditions = {}
        for k, it in self._declared_filters.items():
            ct = it.take_query_data(params)
            conditions.update(ct)

        logger.debug(f"filter_queryset conditions: {conditions}")
        if len(conditions) > 0:
            queryset = queryset.filter(**conditions)
        return self._order_query_set(queryset)

    def _order_query_set(self, query_set):
        if self._meta and self._meta.order_by:
            query_set = query_set.order_by(*self._meta.order_by)
        return query_set.all()

    def get_schema_operation_parameters(self, view):
        return [
            it.to_oper_parameters()
            for k, it in self._declared_filters.items()
        ]


