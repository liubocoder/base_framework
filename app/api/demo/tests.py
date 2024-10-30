import uuid

import loguru
from django.db import transaction
from django.test import TestCase

from app.api.demo.models import MyJsonData, MyDemoData, MyFore, Author, Book

"""
python manage.py test 包名.类名.函数名
python manage.py test app.api.demo.MyUnitTest.test1 --keepdb
    参数选项 --keepdb 保存测试数据库
        可在数据库配置中指定测试数据库，默认是与项目数据库一致
"""

class MyUnitTest(TestCase):
    def testDbAtomic(self):
        #方案1使用注解  using参数指定数据库
        #@transaction.atomic()

        #方案2使用with transaction.atomic()

        #方案3使用try except
        sid = transaction.savepoint()
        try:
            mdd = MyDemoData()
            mdd.name = "n1"
            mdd.save()
            dbMdd = MyDemoData.objects.get(did=mdd.did)
            mf = MyFore()
            mf.name = "mf1"
            mf.demoDid = dbMdd
            mf.save()
            # 产生异常
            # raise Exception("xx")
            transaction.savepoint_commit(sid)
        except Exception as e:
            transaction.savepoint_rollback(sid)

        print(f"MyDemoData 数据量： {MyDemoData.objects.count()}")
        print(f"MyFore 数据量： {MyFore.objects.count()}")


    def testDbRel(self):
        # 测试简单的关联关系
        mdd = MyDemoData()
        mdd.name = "n1"
        mdd.save()
        dbMdd = MyDemoData.objects.get(did=mdd.did)
        mf = MyFore()
        mf.name = "mf1"
        mf.demoDid = dbMdd
        mf.save()
        print(mf)

    def testDbPre(self):
        # prefetch_related
        print("-------------")
        aid = uuid.uuid4()
        at = {"name": "zs", "age": 20, "id": aid}
        ar = Author(**at)
        ar.save()

        bid = uuid.uuid4()
        bk = {"name": "jyud", "price": 110, "id": bid, "author": ar}
        Book(**bk).save()

        bobj = Book.objects.all()

        print(bobj.author)

        print("--------------")



    def testDbJson(self):
        # 测试json格式的数据
        md = MyJsonData()
        md.name = "zs"
        md.content = {
          "level": "DEBUG",
          "handlers": ["aa", "bb"],
          "propagate": False
        }
        md.save()
        md = MyJsonData()
        md.name = "zs"
        md.content = {
            "level": "INFO",
            "handlers": ["xx", "dd"],
            "propagate": True
        }
        md.save()

        vs = MyJsonData.objects.filter(content__level='INFO').values()
        for it in vs:
            print(it)

