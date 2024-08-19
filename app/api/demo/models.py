import uuid

from django.apps import AppConfig
from django.db import models
from django.db.models.signals import post_migrate
from django.dispatch import receiver

@receiver(post_migrate)
def create_def_val(sender: AppConfig, **kwargs):
    if sender.name != 'app.api.demo':
        return
    #处理数据迁移
    print(sender.name, sender.models, sender.verbose_name, sender.path)

class MyDemoData(models.Model):
    did = models.CharField(primary_key=True, max_length=64, default=uuid.uuid4, verbose_name="主键id")
    name = models.CharField(max_length=64, verbose_name="名称信息")
    factory = models.IntegerField(default=0, verbose_name="厂家")
    ctime = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    mtime = models.DateTimeField(auto_now=True, verbose_name="修改时间")
    myTextData = models.TextField()

    class Meta:
        ...

class MyFore(models.Model):
    # db_constraint是否应用到数据库 false不应用
    demoDid = models.ForeignKey(MyDemoData, on_delete=models.DO_NOTHING, verbose_name="示例数据id", db_constraint=False)
    name = models.CharField(max_length=64, verbose_name="名称信息")
    ctime = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    mtime = models.DateTimeField(auto_now=True, verbose_name="修改时间")
    class Meta:
        ...


class MyJsonData(models.Model):
    name = models.CharField(max_length=64, verbose_name="名称信息")
    content = models.JSONField(verbose_name="json数据")