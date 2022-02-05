# coding:utf-8

from django.forms import ModelForm
from django.forms import DateInput
from django.forms import RadioSelect
from django.forms import ImageField
from django.forms import Textarea
from django.forms import ClearableFileInput
from django.forms import inlineformset_factory

from django.contrib.auth.forms import AuthenticationForm

from markdownx.widgets import MarkdownxWidget

from cms.models import Item
from cms.models import ItemImage
from cms.models import Post
from cms.models import PostImage
from cms.models import Comment
from cms.models import Reply

class DateInput(DateInput):
    input_type = 'date'

class ItemForm(ModelForm):
    """作品のフォーム"""

    class Meta:
        model = Item
        fields = ('name', 'detail', 'category', 'chapter', 'date','minne_url','is_sold','price','price_sold','comment')
        widgets = {
            'date': DateInput(),
            'category':RadioSelect(),
            'chapter':RadioSelect()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label  # placeholderにフィールドのラベルを入れる

class LoginForm(AuthenticationForm):
    """ログインフォーム"""
 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label  # placeholderにフィールドのラベルを入れる

class ItemImageForm(ModelForm):

    class Meta:
        model = ItemImage
        fields = ('img', 'item', 'is_in_dark', 'is_topPageImage','is_itemlist')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label  # placeholderにフィールドのラベルを入れる


    img  = ImageField(
        widget=ClearableFileInput(attrs={'multiple': True}),
    )

ItemImageFormSet = inlineformset_factory(Item, ItemImage, ItemImageForm, extra=5, max_num=5, can_delete=False)

class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = ['title','body','category','tag','thumnail','is_publish','abstract']
        widgets = {
            'body': MarkdownxWidget(attrs={'class': 'textarea'}),
        }

class CommentCreateForm(ModelForm):
    """コメント投稿フォーム"""

    class Meta:
        model = Comment
        exclude = ('target', 'created_at')
        widgets = {
            'text': Textarea(
                attrs={'placeholder': 'マークダウンに対応しています。'}
            )
        }


class ReplyCreateForm(ModelForm):
    """返信コメント投稿フォーム"""

    class Meta:
        model = Reply
        exclude = ('target', 'created_at')
        widgets = {
            'text': Textarea(
                attrs={'placeholder': 'マークダウンに対応しています。'}
            )
        }

class PostImageForm(ModelForm):

    class Meta:
        model = PostImage
        fields = ('img',)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label  # placeholderにフィールドのラベルを入れる


    img  = ImageField(
        widget=ClearableFileInput(attrs={'multiple': True}),
    )
