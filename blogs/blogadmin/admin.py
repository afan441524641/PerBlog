# from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib import admin

# Register your models here.
from django.contrib.admin import AdminSite
from django.urls import reverse
from django.utils.html import format_html
from mdeditor.widgets import MDEditorWidget
from articles.models import CategoryInfo, TagsInfo, Article, DefaultImage
from django.db import models




# 参考文献：
# https://docs.djangoproject.com/en/3.0/ref/contrib/admin/#inlinemodeladmin-objects
# ModelAdmin 配置
# https://docs.djangoproject.com/en/dev/ref/contrib/admin/#modeladmin-options

# 在一对多的关系中，可以在一端的编辑页面中编辑多端的对象，嵌入多端对象的方式包括表格、块两种。

# # 类型InlineModelAdmin：表示在模型的编辑页面嵌入关联模型的编辑。
# # 子类TabularInline：以表格的形式嵌入。
# class HeroInfoTabular(admin.TabularInline):
#     # 关联模型的名字
#     model = HeroInfo
#     # 编辑的个数
#     extra = 1


# # 子类StackedInline：以块的形式嵌入
# class HeroInfoStack(admin.StackedInline):
#     # 关联模型的名字
#     model = HeroInfo
#     # 编辑的个数
#     extra = 1




# 标签
@admin.register(TagsInfo)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'create_time')
    fields = ('name', 'status')
    # 右侧过滤器
    # list_filter = ['hgender']


# 分类
# @admin.register(CategoryInfo)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'create_time', 'article_count')
    fields = ('name', 'status')

    # 查询文章数量
    def article_count(self, obj):
        return obj.article_set.count()

    # short_description可调用对象添加属性来自定义列标题。
    article_count.short_description = '文章数量'


# class CategoryInfoStack(admin.StackedInline):
#     # 关联模型的名字
#     model = Article
#     # 编辑的个数
#     extra = 1


# cke富文本编辑器写法
# class ArticleAdminForm(forms.ModelForm):
#     content = forms.CharField(widget=CKEditorWidget(), label='正文', required=True)
#
#     class Meta:
#         model = Article
#         # fields = '__all__'
#         fields = (
#             'title', 'category', 'tag',
#             'status',
#             'content',
#             'default_images',
#             'owner'
#         )
#
#
# class ArticleAdmin(admin.ModelAdmin):
#     form = ArticleAdminForm
#
#
# admin.site.register(Article, ArticleAdmin)


# class MDEditorForm(forms.Form):
# name = forms.CharField()
# content = MDTextFormField()

# class Meta:
#     model = Article
#     fields = (
#         'title',
#         'category',
#         'tag',
#         'status',
#         'desc',
#         'content',
#         'default_images',
#         'owner'
#     )


# class MDEditorModleForm(forms.ModelForm):
# content = MDTextField()

# class Meta:
#     model = Article
#     fields = ('content',)
# fields = (
#     'title',
#     # 'category',
#     # 'tag',
#     # 'status',
#     # 'desc',
#     # 'content',
#     # 'default_images',
#     # 'owner'
# )


# 文章
class ExampleModelAdmin(admin.ModelAdmin):
    # inlines = [CategoryInfoStack]
    # 搜索框
    search_fields = ['title']
    # 列表页每页显示的个数
    list_per_page = 10

    list_display = [
        'title', 'category', 'tag', 'status', 'create_time', 'owner', 'operator'
    ]
    # 控制列表页操作栏在页面上的显示位置。默认情况下，管理员更改列表在页面（）的顶部显示操作。
    # actions_on_bottom = True
    # 控制是否在操作下拉菜单旁边显示选择计数器。默认情况下，管理员更改列表将显示它（）。
    # actions_selection_counter = True
    # date_hierarchy = 'author__pub_date'
    # save_on_top = True

    # 不包括
    # exclude = ('comments', 'reads')
    # description 描述
    fieldsets = (
        ('选项', {
            'fields': (('owner', 'category', 'tag'),
                       'default_images'),
            # 起一个折叠功能
            # 'classes': ('collapse',),
        }),
        ('编写栏', {
            'fields': ('title',
                       'status',
                       'content',
                       )
        })
    )

    # 反向管理参考文献
    # https://docs.djangoproject.com/en/3.0/ref/contrib/admin/#reversing-admin-urls
    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('admin:articles_article_change', args=(obj.id,))
        )

    operator.short_description = '操作'
    # formfield_overrides
    # 是为特定类型的字段添加自定义窗口小部件。
    # 为TextField字段添加自定义窗口组件 MDEditorWidget
    formfield_overrides = {
        models.TextField: {'widget': MDEditorWidget}
    }


@admin.register(DefaultImage)
class DefaultImageAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'default_image'
    ]
    fields = (
        'name',
        'default_image',
    )


admin.site.register(Article, ExampleModelAdmin)
admin.site.register(CategoryInfo, CategoryAdmin)
admin.site.site_header = 'Blog‘s'
admin.site.site_title = 'Blog后台管理'
admin.site.index_title = '欢迎使用Blog后台管理系统'

# @admin.register(Article)
# # class ArticleAdmin(forms.ModelForm):
# #
# #     content = forms.CharField(widget=forms.HiddenInput(), label='正文', required=True)
# #
# #     list_display = [
# #         'title', 'category', 'tag', 'status', 'create_time', 'owner'
# #     ]
# #     # list_display_links = []
# #     #
# #     # search_fields = ['category', ]
# #
# #     # actions_on_top = True
# #     # actions_on_bottom = True
# #     # save_on_top = True
# #
# #     # fields = (
# #     #     ('title', 'category', 'tag'),
# #     #     'status',
# #     #     'desc',
# #     #     'content',
# #     #     'default_images',
# #     #     'owner'
# #     # )
# #
# #     class Meta:
# #         model = Article
# #         fields = (
# #             ('title', 'category', 'tag'),
# #             'status',
# #             'desc',
# #             'content',
# #             'default_images',
# #             'owner'
# #         )
# #     # def operator(self, obj):
# #     #     return format_html(
# #     #         '<a href="{}">编辑</a>',
# #     #         reverse('admin:blog_post_change', args=(obj.id,))
# #     #     )
# #
# #     # operator.short_description = '操作'
