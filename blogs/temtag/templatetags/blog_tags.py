"""
_*_ coding:utf-8 _*_
————————————————
@Time    : 2020/4/26 17:28
@Author  : Afan
@FileName: blog_tags.py
@Software: PyCharm
————————————————
"""

from django import template
from PerBlog.settings import SITE_CONFIG

# 自定义标签模板 可全局使用
# 详见 https://docs.djangoproject.com/en/dev/howto/custom-template-tags/

register = template.Library()


# 返回站点配置
@register.simple_tag
def get_site_config():
    return SITE_CONFIG


