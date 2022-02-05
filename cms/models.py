from django.db import models
from markdownx.models import MarkdownxField
from django.contrib.auth.models import User

from portal.settings import MEDIA_ROOT

import uuid
import os

# Create your models here.

default_markdown_text = """\
[TOC]
# 見出し1
本文
## 見出し2

**強調**
*斜字*
"""

class Profile(models.Model):

    class Meta:
        verbose_name = 'プロフィール'
        verbose_name_plural = 'プロフィール'  
    text = models.TextField("プロフィール", max_length=255)
    user = models.OneToOneField(User,related_name="profile", on_delete=models.PROTECT)

    def __str__(self):
        return self.user.username + "のプロフィール"


class Tag(models.Model):
    """ タグ """
    class Meta:
        verbose_name = 'タグ'
        verbose_name_plural = 'タグ'  
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return self.name
 
    def get_latest_post(self):
        result = Post.objects.filter(
            tag=self).filter(
            is_publish=True).order_by('-created_at')[:5]
        return result

class PostBigCategory(models.Model):
    """ 大カテゴリー """
    class Meta:
        verbose_name = '投稿の大カテゴリ'
        verbose_name_plural = '投稿の大カテゴリ' 
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return self.name
 
    def get_latest_post(self):
        result = Post.objects.filter(
            category__parent=self).filter(
            is_publish=True).order_by('-created_at')[:5]
        return result

class SmallCategory(models.Model):
    """ 小カテゴリー """

    class Meta:
        verbose_name = '投稿のカテゴリ'
        verbose_name_plural = '投稿のカテゴリ'

    name = models.CharField(max_length=255)
    parent = models.ForeignKey(PostBigCategory, verbose_name='親カテゴリー',on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return self.name
 
    def get_latest_post(self):
        result = Post.objects.filter(
            category=self).filter(
            is_publish=True).order_by('-created_at')[:5]
        return result


class Post(models.Model):
    class Meta:
        verbose_name = '投稿'
        verbose_name_plural = '投稿'

    title  = models.CharField(u'タイトル', max_length=30,null=True,blank=True)
    body = MarkdownxField('本文', help_text='Markdown形式で書いてください。',default = default_markdown_text, max_length=10000)
    created_at = models.DateField('作成日', auto_now_add=True)
    updated_at = models.DateField('更新日', auto_now=True)
    category = models.ForeignKey(SmallCategory, null=True, blank=True, verbose_name='カテゴリー',on_delete=models.PROTECT)
    tag = models.ManyToManyField(Tag, blank=True, verbose_name='タグ', related_name="tag")
    thumnail = models.ImageField("サムネイル画像", upload_to='post/', null=True, blank=True)
    is_publish = models.BooleanField('公開するか', default=True)
    writer = models.ForeignKey(
        User,
        verbose_name="ライター",
        on_delete=models.CASCADE,
        default=2
    )
    abstract = models.TextField('要約', blank=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    class Meta:
        verbose_name = '記事のコメント'
        verbose_name_plural = '記事のコメント'
    name = models.CharField('名前', max_length=255, blank=True)
    text = models.TextField('本文')
    target = models.ForeignKey(Post, verbose_name='コメント',on_delete=models.PROTECT)
    created_at = models.DateTimeField('作成日',auto_now_add=True)
    is_publish = models.BooleanField('公開するか', default=False)
 
    def __str__(self):
        return self.text[:10]

class Reply(models.Model):
    """コメントに紐づく返信"""
    class Meta:
        verbose_name = '返信'
        verbose_name_plural = '返信'
    name = models.CharField('名前', max_length=255, default='匿名希望')
    text = models.TextField('本文')
    target = models.ForeignKey(Comment, on_delete=models.CASCADE, verbose_name='対象コメント')
    created_at = models.DateTimeField('作成日', auto_now_add=True)
    is_publish = models.BooleanField('公開するか', default=False)

    def __str__(self):
        return self.text[:20]

class Category(models.Model):
    class Meta:
        verbose_name = 'カテゴリ'
        verbose_name_plural = 'カテゴリ'
    """
    HaLu の作品のカテゴリ（ネックレス…など）
    """
    category = models.CharField(u'カテゴリ', max_length=15)

    def __str__(self):
        return self.category


class Chapter(models.Model):
    """
    HaLu の小説の章
    """
    class Meta:
        verbose_name = '章'
        verbose_name_plural = '章'

    chapter = models.CharField(u'章', max_length=15)
    name = models.CharField(u'名前', max_length=30,null=True,blank=True)

    def __str__(self):
        n = self.name if self.name else ""
        return self.chapter + " " + n 

class Item(models.Model):
    """
    HaLu の作品
    """

    class Meta:
        verbose_name = '作品'
        verbose_name_plural = '作品'

    name = models.CharField(u'作品名', max_length=30)
    detail = models.TextField(u'詳細', max_length=300, blank=True, null=True)
    category = models.ForeignKey(Category, verbose_name='カテゴリー',on_delete=models.PROTECT)
    chapter = models.ForeignKey(Chapter, verbose_name='チャプター', on_delete=models.PROTECT)
    date = models.DateField(u'日付')
    minne_url = models.URLField(u'ミンネのURL', blank=True, null=True)
    is_sold = models.BooleanField(u'売れたか', default=False)
    price = models.IntegerField(u'値段', default=0)
    price_sold = models.IntegerField(u'実際売った値段', default=0)
    comment = models.TextField(
        u'作者のコメント', max_length=300, blank=True, null=True)

    def __str__(self):
        return "No. " + str(self.pk) + " " + self.name + "_" + self.date.strftime(u'%Y/%m/%d')+" 製作"


class ItemImage(models.Model):
    """
    Haru の作品の画像
    """

    class Meta:
        verbose_name = 'アイテム画像'
        verbose_name_plural = 'アイテム画像'

    def get_image_path(self, filename):
        """カスタマイズした画像パスを取得する.

        :param self: インスタンス (models.Model)
        :param filename: 元ファイル名
        :return: カスタマイズしたファイル名を含む画像パス
        """

        name = str(uuid.uuid4()).replace('-', '')
        extension = os.path.splitext(filename)[-1]
        return name + extension

    #alt = models.CharField(u'画像名', max_length=30, blank=True, null=True)
    img = models.ImageField(u'作品の画像', upload_to=get_image_path)
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, blank=True,
                            null=True, verbose_name="作品", related_name="ITEM")
    is_in_dark = models.BooleanField(u'暗闇', default=True)
    is_topPageImage = models.BooleanField(u'トップページ', default=False)
    is_itemlist = models.BooleanField(u'アイテムリストに載せる', default=True)

    def __str__(self):
        image_name = "関連付けられていないアイテムの画像"
        path = self.img.name
        if self.item:
            image_name = self.item.name + "の画像"
        return image_name + "({})".format(path)

    def delete_previous_file(function):
        """不要となる古いファイルを削除する為のデコレータ実装.

        :param function: メイン関数
        :return: wrapper
        """
        def wrapper(*args, **kwargs):
            """Wrapper 関数.

            :param args: 任意の引数
            :param kwargs: 任意のキーワード引数
            :return: メイン関数実行結果
            """
            self = args[0]

            # 保存前のファイル名を取得
            result = ItemImage.objects.filter(pk=self.pk)
            previous = result[0] if len(result) else None
            super(ItemImage, self).save()

            # 関数実行
            result = function(*args, **kwargs)

            # 保存前のファイルがあったら削除
            #if previous:
            #    os.remove(MEDIA_ROOT + "/" + previous.img.name)
            return result
        return wrapper

    @delete_previous_file
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(ItemImage, self).save()

    @delete_previous_file
    def delete(self, using=None, keep_parents=False):
        super(ItemImage, self).delete()

class InfoCategory(models.Model):

    class Meta:
        verbose_name = 'サイト情報カテゴリ'
        verbose_name_plural = 'サイト情報カテゴリ'

    name = models.CharField(u'名称', max_length=15)
    color = models.CharField(u'色', max_length=15)

    def __str__(self):
        return self.name

class PostImage(models.Model):
    """
    ブログ の作品の画像
    """

    class Meta:
        verbose_name = 'ブログ画像'
        verbose_name_plural = 'ブログ画像'

    def get_image_path(self, filename):
        """カスタマイズした画像パスを取得する.

        :param self: インスタンス (models.Model)
        :param filename: 元ファイル名
        :return: カスタマイズしたファイル名を含む画像パス
        """

        name = str(uuid.uuid4()).replace('-', '')
        extension = os.path.splitext(filename)[-1]
        return name + extension

    #alt = models.CharField(u'画像名', max_length=30, blank=True, null=True)
    img = models.ImageField(u'ブログ画像', upload_to=get_image_path)

    def __str__(self):
        name = str(self.id) if self.id else "ブログ画像"
        return name

    def delete_previous_file(function):
        """不要となる古いファイルを削除する為のデコレータ実装.

        :param function: メイン関数
        :return: wrapper
        """
        def wrapper(*args, **kwargs):
            """Wrapper 関数.

            :param args: 任意の引数
            :param kwargs: 任意のキーワード引数
            :return: メイン関数実行結果
            """
            self = args[0]

            # 保存前のファイル名を取得
            result = PostImage.objects.filter(pk=self.pk)
            previous = result[0] if len(result) else None
            super(PostImage, self).save()

            # 関数実行
            result = function(*args, **kwargs)

            # 保存前のファイルがあったら削除
            #if previous:
            #    os.remove(MEDIA_ROOT + "/" + previous.img.name)
            return result
        return wrapper

    @delete_previous_file
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(PostImage, self).save()

    @delete_previous_file
    def delete(self, using=None, keep_parents=False):
        super(PostImage, self).delete()


class SiteInfo(models.Model):

    class Meta:
        verbose_name = 'サイト情報'
        verbose_name_plural = 'サイト情報'

    date = models.DateField(u'日付')
    body = models.TextField(u'本文', max_length=300, blank=True, null=True)
    info_category = models.ForeignKey(InfoCategory, verbose_name='カテゴリー',on_delete=models.PROTECT)
    tag = models.CharField(u'タグ', max_length=15, default="INFO")

    def __str__(self):
        return "{0}:{1}...".format(self.date, self.body[:10])
