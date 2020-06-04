# from ckeditor.fields import RichTextField
from django.db import models
from mdeditor.fields import MDTextField

from utils.models import BaseModel
from django.contrib.auth.models import User

# on_delete=None,               # 删除关联表中的数据时,当前表与其关联的field的行为
# on_delete=models.CASCADE,     # 删除关联数据,与之关联也删除
# on_delete=models.DO_NOTHING,  # 删除关联数据,什么也不做
# on_delete=models.PROTECT,     # 删除关联数据,引发错误ProtectedError
# # models.ForeignKey('关联表', on_delete=models.SET_NULL, blank=True, null=True)
# on_delete=models.SET_NULL,    # 删除关联数据,与之关联的值设置为null（前提FK字段需要设置为可空,一对一同理）
# # models.ForeignKey('关联表', on_delete=models.SET_DEFAULT, default='默认值')
# on_delete=models.SET_DEFAULT, # 删除关联数据,与之关联的值设置为默认值（前提FK字段需要设置默认值,一对一同理）
# on_delete=models.SET,         # 删除关联数据,
#  a. 与之关联的值设置为指定值,设置：models.SET(值)
#  b. 与之关联的值设置为可执行对象的返回值,设置：models.SET(可执行对象)
# ————————————————

# Create your models here.
# 将模型类同步到数据库中。

# 生成迁移文件
# python manage.py makemigrations
# 同步到数据库中
# python manage.py migrate
# verbose_name 页面展示用 相当于对字段的描述
# 文章类别
STATUS_ITEMS = (
    (1, '正常'),
    (0, '删除')
)


class CategoryInfo(BaseModel):
    # STATUS_ITEMS = (
    #     (1, '正常'),
    #     (0, '删除')
    # )
    # 分类名
    name = models.CharField(max_length=20, verbose_name='分类')
    # 标签状态选项
    status = models.PositiveIntegerField(default=1, choices=STATUS_ITEMS, verbose_name='状态')

    # 作者
    # owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')

    class Meta:
        db_table = 'categories_info_table'
        verbose_name = verbose_name_plural = '分类'

    def __str__(self):
        return self.name

    # 文章标签


# 标签
class TagsInfo(BaseModel):
    # STATUS_ITEMS = (
    #     (1, '正常'),
    #     (0, '删除')
    # )
    # 标签名
    name = models.CharField(max_length=20, verbose_name='名称')
    # 标签状态选项
    status = models.PositiveIntegerField(default=1, choices=STATUS_ITEMS, verbose_name='状态')

    class Meta:
        db_table = 'tags_info_table'  # 表名
        verbose_name = verbose_name_plural = '标签'  # 在admin站点中显示的名称
        # verbose_name_plural  # 显示的复数名称

    def __str__(self):
        return self.name


# 默认图片地址
class DefaultImage(BaseModel):
    # 图片名
    name = models.CharField(max_length=100, null=True, blank=True, verbose_name='名称')
    # 最大长度200 为空时数据库里为null 允许为空
    default_image = models.ImageField(max_length=200, verbose_name='图片')

    class Meta:
        db_table = 'default_image_table'  # 表名
        verbose_name = verbose_name_plural = '图片地址'  # 在admin站点中显示的名称
        # verbose_name_plural = verbose_name  # 显示的复数名称

    def __str__(self):
        return self.name


# 文章的基本信息
class Article(BaseModel):
    # STATUS_ITEMS = (
    #     (1, '正常'),
    #     (0, '删除'),
    #     (2, '草稿')
    # )
    # 新生成一个状态选项元组
    STATUS_ITEMS = (STATUS_ITEMS[0], STATUS_ITEMS[1], (2, '草稿'))
    # 文章标题
    title = models.CharField(max_length=100, verbose_name='标题')
    # 评论量
    comments = models.IntegerField(default=0, verbose_name='评论数')
    # 阅读量
    reads = models.IntegerField(default=0, verbose_name='阅读数')
    # 状态
    status = models.PositiveIntegerField(default=1, choices=STATUS_ITEMS, verbose_name='状态')
    # 分类，关联CategoryInfo表
    category = models.ForeignKey(CategoryInfo, on_delete=models.CASCADE, verbose_name='分类')
    # 标签
    tag = models.ForeignKey(TagsInfo, on_delete=models.CASCADE, verbose_name='标签')
    # 图片地址
    default_images = models.ForeignKey(DefaultImage, null=True, blank=True, on_delete=models.CASCADE,
                                       verbose_name='图片地址')
    # 作者
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')
    # 文章摘要
    # desc = models.CharField(max_length=1024, blank=True, verbose_name='摘要')
    # 文章正文
    content = MDTextField(verbose_name=u'正文')
    # content = RichTextField()

    class Meta:
        db_table = 'article_info_table'  # 表名
        verbose_name = verbose_name_plural = '文章'  # 在admin站点中显示的名称
        # verbose_name_plural = verbose_name  # 显示的复数名称

    def __str__(self):
        return self.title

# 文章内容 废弃
# class ArticleContent(BaseModel):
#     # 文章摘要
#     desc = models.CharField(max_length=1024, blank=True, verbose_name='摘要')
#     # 文章正文
#     content = models.TextField(verbose_name='正文', help_text='正文必须为MarkDown格式')
#     # 绑定外键 关联文章信息
#     article_info = models.ForeignKey(ArticleInfo, on_delete=models.CASCADE, verbose_name='文章信息')
#
#     # @property
#     # def decade_born_in(self):
#     #     return self.article_info.title
#
#     # decade_born_in.short_description = 'Birth decade'
#
#     class Meta:
#         db_table = 'article_content_table'  # 表名
#         verbose_name = verbose_name_plural = '文章内容'  # 在admin站点中显示的名称
#         # verbose_name_plural = verbose_name  # 显示的复数名称
#
#     def __str__(self):
#         return self.desc
