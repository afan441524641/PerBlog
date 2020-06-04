"""
_*_ coding:utf-8 _*_
————————————————
@Time    : 2020/5/4 11:48
@Author  : Afan
@FileName: get_arcitle.py
@Software: PyCharm
@QQ      : 441524641
————————————————
"""
import markdown
# import mistune
from django.core.paginator import Paginator
from django.shortcuts import render
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension

from articles.models import Article


# 参考文档:https://python-markdown.github.io/
def mark():
    return markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        TocExtension(slugify=slugify),
    ])


# 获取文章摘要
def get_article_data(article_list, page_num=1):
    md = mark()
    # print(page_num)
    # 传入文章对象,每页要显示多少条数据
    paginator = Paginator(article_list, per_page=2)
    # 获取某页的数据
    post_list = paginator.page(page_num)
    # print(post_list)

    # 循环遍历,将文章内容格式化
    for i in post_list:
        # 使用mistune库 传入Markdown格式文本，返回格式化好后的html代码
        i.content = md.convert(i.content)
        # print(post_list[i].body)
        i.toc = md.toc  # 目录
        i.img_url = '/media/' + i.default_images.default_image.name
        # print(i.toc)
        # i.content = mistune.markdown(post_list[0].content)
        # print(i.content, 1111)
    # 获取总页数
    total_page = paginator.num_pages

    return {'article_list': post_list, 'total_page': ''.join([str(i) for i in range(1, total_page + 1)]),
            'page_num': page_num}
