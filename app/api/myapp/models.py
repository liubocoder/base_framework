from django.db import models

# Create your models here.


class Book(models.Model):
    name = models.CharField(max_length=64)
    desc = models.CharField(max_length=512)
    ctime = models.DateTimeField(auto_now_add=True)