# coding:utf-8

from datetime import date

from django import template
from django.utils.safestring import mark_safe

#from markdownx.utils import markdownify
# from markdownx.settings import MARKDOWNX_MARKDOWN_EXTENSIONS
from markdownx.settings import MARKDOWNX_MARKDOWN_EXTENSION_CONFIGS

from portal.settings import MARKDOWNX_MARKDOWN_EXTENSIONS
#from portal.settings import MARKDOWNX_MARKDOWN_EXTENSION_CONFIGS

from markdown import markdown
from markdown.extensions import Extension

from cms.models import ItemImage

register = template.Library()
today = date.today()

@register.filter(name='is_new',expects_localtime=True)
def is_new(value):
    if type(value) is date:
        target_date = value
        diff = today - target_date
        return diff.days < 50
    else:
        return True 


@register.filter
def item_images(pk):
    return ItemImage.objects.filter(item_id=pk)

# カスタムフィルタとして登録する
@register.filter
def make_delay(counter):
    delay = 9
    return counter * delay - delay

@register.simple_tag 
def slice(body, end):
    return body[:end]

def markdownify(content):
    md = markdown(
        text=content,
        extensions=MARKDOWNX_MARKDOWN_EXTENSIONS,
        extension_configs=MARKDOWNX_MARKDOWN_EXTENSION_CONFIGS
    )
    return md


@register.filter
def markdown_to_html(text):
    """マークダウンをhtmlに変換する。"""
    md = markdownify(text)

    
    return mark_safe(md)

class EscapeHtml(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.deregister('html_block')
        md.inlinePatterns.deregister('html')


@register.filter
def markdown_to_html_with_escape(text):
    """
    コメント欄等

    """
    extensions = MARKDOWNX_MARKDOWN_EXTENSIONS + [EscapeHtml()]
    html = markdown(text, extensions=extensions, extension_configs=MARKDOWNX_MARKDOWN_EXTENSION_CONFIGS)
    return mark_safe(html)

@register.simple_tag
def query_transform(request, **kwargs):
    updated = request.GET.copy()
    for k, v in kwargs.items():
        updated[k] = v

    return updated.urlencode()