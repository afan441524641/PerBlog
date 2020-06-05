import datetime
import markdown
from django import http
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
# Create your views here.
from django.utils.text import slugify
from django.views import View
from markdown.extensions.toc import TocExtension
from articles.models import Article, CategoryInfo, TagsInfo
from utils.get_arcitle import get_article_data, mark


class RedirectView(View):
    # 返回博客主页
    def get(self, request):
        return redirect('/')


class PageView(View):
    def get(self, request, page_num):
        # 按照创建时间排序
        article_list = Article.objects.all().order_by('-create_time')
        print(article_list, "文章数据")
        context = get_article_data(article_list, page_num)

        return render(request, 'index.html', context=context)


# 文章详情页
class ArticleDetails(View):
    def get(self, request, article_id):
        md = mark()
        # return render(request, 'index_2.html')
        # print(article_id)
        article_obj_list = Article.objects.filter(pk=article_id)
        # print(article_obj_list)
        # 查询不到文章数据，重定向至主页
        if not article_obj_list:
            return redirect('/')
            # return http.JsonResponse({'code': 0, 'errmsg': '文章id不存在'})
        # print(article_obj_list[0].title, article_obj_list[0].owner)
        # 返回的是列表对象，用索引取出
        article_obj = article_obj_list[0]
        # article_list = Article.objects.filter()
        # print(article_list)
        # html = etree.HTML(mistune.markdown(article_obj.content))
        # print(html)
        # h_tag = html.xpath('//h1/text()')
        # print(h_tag)
        context = {
            'id': article_id,
            'title': article_obj.title,
            'owner': article_obj.owner,
            'content': md.convert(article_obj.content),  # 使用mistune库 传入Markdown格式文本，返回格式化好后的html代码
            'create_time': (article_obj.create_time + + datetime.timedelta(hours=8)).strftime('%Y-%m-%d'),
            # 加8个时区，然后格式化时间
            'menu_list': md.toc,  # 文章目录
            "img_url": '/media/' + article_obj.default_images.default_image.name
        }
        print(article_obj.default_images.default_image.name)
        # print(context)
        # print(context)
        return render(request, 'details.html', context=context)


# 获取最新文章数据
class GetNewArticleView(View):
    def get(self, request):
        # 从数据库中取除最新得5篇文章
        # 当执行如下语句时，并未进行数据库查询，只是创建了一个查询集
        new_article = Article.objects.all().order_by('-create_time')[:5]
        # print(new_article)
        # 列表推导式生成文章列表,不包括内容
        article_list = [{
            'id': i.id,
            'title': i.title,
            'create_time': (i.create_time + datetime.timedelta(hours=8)).strftime('%Y-%m-%d'),
            'category': i.category.name,
            'tag': i.tag.name,
            "img_url": i.default_images.default_image.name,
            'category_id': i.category_id,
            'tag_id': i.tag_id
        } for i in new_article]
        # print(article_list)
        return http.JsonResponse({
            'code': 0,
            'errmsg': 'OK',
            'article_list': article_list,
        })


# 获取分类列表 边栏数据
class GetCate(View):
    def get(self, request):
        # 获取所有的分类对象
        category_obj = CategoryInfo.objects.all()
        # 生成分类属性的列表
        category_list = [{'id': obj.id, 'name': obj.name, 'total_num': obj.article_set.count()} for obj in category_obj]
        # print(category_list)
        return http.JsonResponse({
            'code': 0,
            'errmsg': 'OK',
            'category_list': category_list,
        })


# ajax请求获取标签列表 边栏数据
class GetTags(View):
    def get(self, request):
        # 获取标签属对象
        tags_obj = TagsInfo.objects.all().order_by('-create_time')
        # 生成列表
        tags_list = [{'id': tag_obj.id, 'name': tag_obj.name, 'total_num': tag_obj.article_set.count()} for tag_obj in
                     tags_obj]
        return http.JsonResponse({
            'code': 0,
            'errmsg': 'OK',
            'tags_list': tags_list,
        })


# 标签分类视图
class CateTagsView(View):

    def get(self, request, **kwargs):
        # print(kwargs)
        # print(all(kwargs))
        obj_id = kwargs.get('obj_id')
        page_num = kwargs.get('pag_num')
        name = kwargs.get('name')
        # print(all([obj_id, page_num, name]))
        # 判断是要到标签页,还是标签子类目页
        if not all([obj_id, page_num, name]):  # 如果无传入标签id,则跳转标签主页
            # if name == 'tags':
            #     lis = TagsInfo.objects.all().order_by('-create_time')
            # else:
            #     lis = CategoryInfo.objects.all().order_by('-create_time')
            return render(request, 'tag.html')

        # obj_id = kwargs['obj_id']
        if name == 'tags':
            # 获取标签对象
            obj = TagsInfo.objects.filter(pk=obj_id)
            # 获取标签下的所有文章
        else:
            # 获取分类对象
            obj = CategoryInfo.objects.filter(pk=obj_id)
            # 获取分类下的所有文章

        artcile_list = obj[0].article_set.all().order_by('-create_time')
        # 查询不到标签数据，重定向至主页
        if not artcile_list:
            return redirect('/')
        context = get_article_data(artcile_list, page_num=int(page_num))
        context['obj_id'] = obj_id
        context['name'] = name  # 判断是标签还是分类
        context['title'] = obj[0].name
        # context['url'] = 'tags'
        # print(context)
        return render(request, 'tag_cate_details.html', context=context)

# 分类视图
# class CateView(View):
#
#     def get(self, request, **kwargs):
#         print(kwargs)
#         # 判断是要到标签页,还是分类子类目页
#         if not kwargs:  # 如果无传入分类id,则跳转分类主页
#             return render(request, 'category.html')
#         cate_id = kwargs['cate_id']
#         # 获取分类对象
#         cate_obj = CategoryInfo.objects.filter(pk=cate_id)
#         # 获取分类下的所有文章
#         artcile_list = cate_obj[0].article_set.all().order_by('-create_time')
#         # 查询不到分类数据，重定向至主页
#         if not artcile_list:
#             return redirect('/')
#         context = get_article_data(artcile_list, page_num=int(kwargs['pag_num']))
#         context['cate_id'] = cate_id
#         context['code'] = 1  # 判断是标签还是分类
#         context['name'] = cate_obj[0].name
#         context['url'] = 'category'
#         print(context)
#         return render(request, 'tag_cate_details.html', context=context)


# class Test(View):
#     def get(self, request):
#         return render(request, 'blog_html/test.html')
