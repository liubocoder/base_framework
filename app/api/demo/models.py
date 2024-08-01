import uuid

from django.db import models


# Create your models here.

class MyDemoData(models.Model):
    did = models.CharField(primary_key=True, max_length=64, default=uuid.uuid4, verbose_name="主键id")
    name = models.CharField(max_length=64, verbose_name="名称信息")
    factory = models.IntegerField(default=0, verbose_name="厂家")
    ctime = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    mtime = models.DateTimeField(auto_now=True, verbose_name="修改时间")
    myTextData = models.TextField()

    class Meta:
        db_table = 'my_demo_datas'