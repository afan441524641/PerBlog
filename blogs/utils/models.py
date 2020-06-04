"""
_*_ coding:utf-8 _*_
————————————————
@Time    : 2020/4/27 12:53
@Author  : Afan
@FileName: models.py
@Software: PyCharm
@QQ      : 441524641
————————————————
"""

from django.db import models


class BaseModel(models.Model):
    """为模型类补充字段"""
    # 以下为DateTimeField特有的字段
    # auto_now_add
    # 创建或添加对象时的时间, 修改或更新对象时, 不会更改时间
    # auto_now
    # 凡是对对象进行操作(创建/添加/修改/更新),时间都会随之改变
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        abstract = True  # 说明是抽象模型类, 用于继承使用，数据库迁移时不会创建BaseModel的表
