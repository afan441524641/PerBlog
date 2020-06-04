"""
_*_ coding:utf-8 _*_
————————————————
@Time    : 2020/5/2 18:57
@Author  : Afan
@FileName: urls.py
@Software: PyCharm
@QQ      : 441524641
————————————————
"""
from django.urls import path, re_path, reverse
from . import views

# app_name = 'blog'
# 参考文献:https://docs.djangoproject.com/en/dev/topics/http/urls/#url-dispatcher
urlpatterns = [
    path('', views.RedirectView.as_view()),
    path('page/<int:page_num>/', views.PageView.as_view(), name='page'),
    path('details/<int:article_id>/', views.ArticleDetails.as_view(), name='details'),
    path('GetNewArticle/', views.GetNewArticleView.as_view()),
    path('GetTags/', views.GetTags.as_view()),
    path('GetCateGory/', views.GetCate.as_view()),
    # path('test/', views.Test.as_view()),
    # 标签页路由
    path('tags/', views.CateTagsView.as_view(), name='tags'),
    # 分类页路由 category
    path('category/', views.CateTagsView.as_view(), name='category'),

    re_path(r'^cate_tags/(?P<name>\w+)/(?P<obj_id>\d+)/page/(?P<pag_num>\d+)/$', views.CateTagsView.as_view(),
            name='cate_tags')
    # re_path(r'^category/(?P<cate_id>\d+)/page/(?P<pag_num>\d+)/$', views.CateView.as_view(), name='category'),
    # re_path(r'^categorys/(?P<cate_id>\d+)*/*', views.CateView.as_view()),
    # path('tags/<int:tags_id>/', views.TagsView.as_view()),
    # path('categories/<int:cate_id>/', views.CateView.as_view()),
]
