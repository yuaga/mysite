from django.db import models
from apps.login.models import User


class AddCategory(models.Model):
    name = models.CharField(max_length=100)


class News(models.Model):
    title = models.CharField(max_length=100)
    desc = models.CharField(max_length=200)
    thumbnail = models.URLField()
    content = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)
    # 如果到时候分类删除，此新闻保留。
    category = models.ForeignKey(AddCategory, on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    # 在此声明排列顺序，那么所有数据都按这个规则排列
    class Meta:
        ordering = ['-pub_time']
