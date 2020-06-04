import markdown
from django import http
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views import View
from markdown.extensions.toc import TocExtension
from django.utils.text import slugify
# import mistune  # 开发文档 https://pypi.org/project/mistune/
from articles.models import Article
import time
# Create your views here.
from utils.get_arcitle import get_article_data


class IndexView(View):
    # 返回博客主页

    def get(self, request):
        # print(request, '进来了')
        # raise http.Http404("No")
        # context = get_object_or_404(Article, pk=100)
        # post = Article.objects.filter(pk=100)
        # if not post:
        #     return render(request, '404.html')
        context = get_article_data(Article.objects.all().order_by('-create_time'))
        # context = get_article_data(Article.objects.filter(pk=2))
        # print(context)
        return render(request, 'index.html', context=context)
        # context = mistune.markdown(data)
        # ctime = time.time()
        # print(ctime)
        # return render(request, 'test.html', {'ctime': ctime})




