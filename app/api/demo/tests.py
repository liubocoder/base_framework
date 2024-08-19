from django.test import TestCase

from app.api.demo.models import MyJsonData

"""
python manage.py test 包名.类名.函数名
python manage.py test app.api.demo.MyUnitTest.test1 --keepdb
    参数选项 --keepdb 保存测试数据库
        可在数据库配置中指定测试数据库，默认是与项目数据库一致
"""

class MyUnitTest(TestCase):
    def test1(self):
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

