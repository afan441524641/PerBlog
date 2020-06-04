# -*- coding: utf-8 -*-

from django.urls import path
from django.views.decorators.cache import cache_page

from . import views

# app_name = 'blog'

urlpatterns = [
    path('', views.IndexView.as_view()),
    path('home/', views.IndexView.as_view(), name='index'),
    # path('home/', cache_page(10,key_prefix='home_key')(views.IndexView.as_view()), name='index'),
    # path('', views.IndexView.as_view()),
]
