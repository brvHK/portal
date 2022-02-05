from datetime import date
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import sys

from plotly.offline import plot
import plotly.figure_factory as ff


import django
from django.db.models.query import QuerySet
from django.db.models import Count
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

from django.urls import reverse_lazy

from cms.forms import ItemForm
from cms.forms import LoginForm
from cms.forms import ItemImageFormSet
from cms.forms import PostForm
from cms.forms import CommentCreateForm
from cms.forms import ReplyCreateForm
from cms.models import Item
from cms.models import ItemImage
from cms.models import Category
from cms.models import SiteInfo
from cms.models import ItemImage
from cms.models import Post
from cms.models import PostImage
from cms.models import SmallCategory
from cms.models import PostBigCategory
from cms.models import Tag
from cms.models import Comment
from cms.models import Reply

from portal.settings import RECAPTHA_SECRET_KEY

today= date.today()

MODEL_BY_QUERYPARAM = {
    "category":Category,
    "smallcategory":SmallCategory,
    "postbigcategory":PostBigCategory,
    "tag":Tag
}

POST_FILTER_NAMES = {
    "postbigcategory":"category__parent",
    "smallcategory":"category",
    "tag":"tag"
}


def index(request):
    u"""Index View"""
    context = {}
    
    context["year"]=str(today.year)
    context["month"]=str(today.month)

    context["siteinfos"] = SiteInfo.objects.all().order_by('-date')
    context["top_images"] = ItemImage.objects.filter(is_topPageImage=True).order_by('-id')[:4]

    context["category_1_item"] = Item.objects.filter(category=1).select_related().first()
    context["category_2_item"] = Item.objects.filter(category=2).select_related().first()
    context["category_3_item"] = Item.objects.filter(category=3).select_related().first()
    context["last_item"] = Item.objects.select_related().last()

    return render(request, 'index.html', context)



class ItemList(ListView):
    model = Item
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super(ItemList, self).get_context_data(**kwargs)

        context['images'] = ItemImage.objects.all()
        category_id = self.request.GET.get("category")
        context['category_id'] = self.request.GET.get("category")
        try:
            category = Category.objects.get(pk=category_id)
            context['category'] = category
        except Category.DoesNotExist as e:
            print(e)
        except ObjectDoesNotExist as e:
            print(e)
        except ValueError as e:
            print(e)
        context["last_item"] = Item.objects.select_related().last()
        
        return context

    def get_queryset(self) -> QuerySet:
        object_list = Item.objects.all().order_by('-date','-id')
        param_value = self.request.GET.get("category")
        if ("category" in self.request.GET) and param_value.isdigit():
            try:
                category = Category.objects.get(pk=param_value)
                object_list = Item.objects.filter(category=category).order_by('-date')
            except Category.DoesNotExist as e:
                print(e)
            except ObjectDoesNotExist as e:
                print(e)
            except ValueError as e:
                print(e)
        return object_list

class ItemDetail(DetailView):
    #template_name = 'user/member_detail.html'
    model = Item
    queryset = Item.objects.select_related()

    def get_context_data(self, **kwargs):
        context = super(ItemDetail, self).get_context_data(**kwargs)

        context['images'] = ItemImage.objects.all().filter(item_id=kwargs["object"].id)
        return context

@login_required
def mod(request, item_id=None):
    """
    HaLu の作品の修正
    """
    context = {}
    initial_formset=[]
    

    if item_id:
        context['edit_type'] = '編集'
        context['item_id'] = item_id
        context['images'] = ItemImage.objects.filter(item__id=item_id)
        item = get_object_or_404(Item, pk=item_id)
        initial_formset = [
            {'item':item.id},
            {'item':item.id},
            {'item':item.id},
            {'item':item.id},
            {'item':item.id},
        ]

        
    else:
        context['edit_type'] = '新規投稿'
        item = Item()
    if request.method == 'POST':  
        form = ItemForm(request.POST, instance=item)

        image_formset = ItemImageFormSet(request.POST or None, files=request.FILES, instance=item,initial = initial_formset)

        if form.is_valid() and image_formset.is_valid():
            item = form.save(commit=False)
            item.save()
            image_formset.save()
            return redirect('cms:item_list')
        else:
            context['image_formset'] = image_formset
    else:
        form = ItemForm(instance=item)
        image_formset = ItemImageFormSet(instance=item,initial = initial_formset)
        
    context["form"] = form
    context["image_formset"] = image_formset
    return render(request, 'cms/mod.html', context)

class InformationView(TemplateView):

    template_name = 'information.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["python_version"] = sys.version
        ctx["django_version"] = django.VERSION
        return ctx


class HaLu(TemplateView):
    """カレンダーを表示するビュー."""

    template_name = 'cms/about/Artist.html'

    def get_context_data(self, *args, **kwargs):
        """HaLu"""
        
        context = super().get_context_data(**kwargs)
        context['Artist'] = 'HaLu'
        context['nickname'] = 'F の創人'
        context['act1'] = '2013年から各地イベントに参加。'
        context['act2'] = 'F の創人'
        context['comments'] = """自作ファンタジー世界の「World of F ～Fの世界～」で使用されているアイテムや幻想的な風景を、
                                様々な素材を用いて表現しています。
                                自然と歴史が好き。"""
        context['since'] = '2013'
        context['twitter'] = 'https://twitter.com/Hyu_HaLu?ref_src=twsrc%5Etfw'

        return context

class Ken(TemplateView):

    template_name = 'cms/about/Artist.html'

    def get_context_data(self, *args, **kwargs):
        """HaLu"""
        
        context = super().get_context_data(**kwargs)
        context['Artist'] = 'Ken'
        context['nickname'] = 'F の案内人'
        context['comments'] = 'あいうえおお'
        context['since'] = '2017'
        context['twitter'] = 'https://twitter.com/brv_HK?ref_src=twsrc%5Etfw'

        return context

class WorldOfFView(TemplateView):

    template_name = 'cms/about/World-of-F.html'

    def get_context_date(self, *args, **kwargs):

        context = super().get_context_data(**kwargs)

        return context

class PrivacyPolicyView(TemplateView):

    template_name = 'privacy-policy.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        privacy_policy = """\
本文書は、 [当サイト](https://world-of-f.website) （Fの世界, World of F）における個人情報の保護およびその適切な取り扱いについての方針を示したものです。\n
## 個人情報の管理
当サイトは、お問い合わせいただいた内容についての確認・相談、情報提供のためのメール送信（返信）の目的以外には使用しません。また知り得た個人情報を第三者に開示することは、警察・裁判所など公的機関からの書面をもった請求以外に一切利用いたしません。\n
## 免責事項
当サイトで掲載している画像の著作権・肖像権等は各権利所有者に帰属致します。権利を侵害する目的ではございません。記事の内容や掲載画像等に問題がございましたら、各権利所有者様本人が直接メールでご連絡下さい。確認後、対応させて頂きます。

当サイトからリンクやバナーなどによって他のサイトに移動された場合、移動先サイトで提供される情報、サービス等について一切の責任を負いません。

当サイトのコンテンツ・情報につきまして、可能な限り正確な情報を掲載するよう努めておりますが、誤情報が入り込んだり、情報が古くなっていることもございます。

当サイトに掲載された内容によって生じた損害等の一切の責任を負いかねますのでご了承ください。

## 当サイトに掲載されている広告について
当サイトでは、第三者配信の広告サービス（ **Googleアドセンス** ）を利用しています。

このような広告配信事業者は、ユーザーの興味に応じた商品やサービスの広告を表示するため、当サイトや他サイトへのアクセスに関する情報 『Cookie』(氏名、住所、メール アドレス、電話番号は含まれません) を使用することがあります。

またGoogleアドセンスに関して、このプロセスの詳細やこのような情報が広告配信事業者に使用されないようにする方法については、 [こちら](http://www.google.co.jp/policies/technologies/ads/){:target="_blank"} をクリックしてください。

## 当サイトが使用しているアクセス解析ツールについて
当サイトでは、Googleによるアクセス解析ツール「 **Googleアナリティクス** 」を利用しています。

このGoogleアナリティクスはトラフィックデータの収集のためにCookieを使用しています。このトラフィックデータは匿名で収集されており、個人を特定するものではありません。

この機能はCookieを無効にすることで収集を拒否することが出来ますので、お使いのブラウザの設定をご確認ください。

この規約に関して、詳しくは [こちら](https://www.google.com/analytics/terms/jp.html){:target="_blank"} をクリックしてください。"""

        ctx["body"] = privacy_policy

        return ctx


class Login(LoginView):
    """ログインページ"""
    form_class = LoginForm
    template_name = 'cms/login.html'
 
 
class Logout(LoginRequiredMixin, LogoutView):
    """ログアウトページ"""
    template_name = 'cms/logout.html'


class PostListView(ListView):
    """アイテム"""

    template_name = 'cms/post/list.html'
    #content_object_name = 'arts'
    paginate_by = 20
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        smallcategory = self.request.GET.get("smallcategory")
        postbigcategory = self.request.GET.get("postbigcategory")
        tag = self.request.GET.get("tag")
        if smallcategory:
            context.update(get_context_from_model("smallcategory", smallcategory))
        if postbigcategory:
            context.update(get_context_from_model("postbigcategory", postbigcategory))
        if tag:
            context.update(get_context_from_model("tag", tag))
        
        return context


    def get_queryset(self):
        
        smallcategory = self.request.GET.get("smallcategory")
        postbigcategory = self.request.GET.get("postbigcategory")
        tag = self.request.GET.get("tag")
        if smallcategory:
            object_list = get_post_data("smallcategory", smallcategory)
        elif postbigcategory:
            object_list = get_post_data("postbigcategory", postbigcategory)
        elif tag:
            object_list = get_post_data("tag", tag)
        else:
            object_list = Post.objects.filter(is_publish=True).order_by('created_at').reverse()
        
        return object_list


def get_context_from_model(param_key, param_value):
    context ={}
    model = MODEL_BY_QUERYPARAM[param_key] if param_key in MODEL_BY_QUERYPARAM else None
    if model:
        try:
            value = model.objects.get(pk=param_value)
            context[param_key] = value
        except model.DoesNotExist as e:
            print(e)    
        except ObjectDoesNotExist as e:
            print(e)
        except ValueError as e:
            print(e)

    return context

def get_post_data(param_key, param_value):
    object_list = None
    filter_name = POST_FILTER_NAMES[param_key] if POST_FILTER_NAMES[param_key] else None
    context = get_context_from_model(param_key, param_value)
    filter_value = context[param_key] if param_key in context else None
    filter_query={
        filter_name: filter_value
    }
    if filter_query[filter_name]:
        object_list = Post.objects.filter(**filter_query).filter(is_publish=True).order_by('created_at').reverse()
    else:
        object_list = []
    
    
    return object_list
class PostDetail(DetailView):
    template_name = 'cms/post/detail.html'
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        comments = Comment.objects.filter(target=self.kwargs['pk'], is_publish=True)
        context["comments"] = comments

        return context

@login_required
def post_mod(request, post_id=None):

    """
    投稿作品の修正
    """
    context = {}
    initial_dict= {}
    initial_dict["writer"] = request.user
    
    if post_id:
        context['edit_type'] = '編集'
        context['post_id'] = post_id

        post = get_object_or_404(Post, pk=post_id)
        context['post_thumnail'] = post.thumnail
        
    else:
        context['edit_type'] = '新規投稿'
        post = Post()
    if request.method == 'POST':  
        form = PostForm(request.POST, request.FILES, instance=post, initial=initial_dict)
        if form.is_valid():
            form.instance.writer = request.user
            post = form.save(commit=False)
            post.save()
            form.save_m2m()
            if 'save_and_add' in request.POST:
                return redirect('post:add')

                # 保存して編集を続けるボタン
            elif 'save_and_edit' in request.POST:
                return redirect('post:mod', post_id=post.pk)
            return redirect('post:list')
    else:
        form = PostForm(instance=post, initial=initial_dict)
        
    context["form"] = form
    context["item_images"] = ItemImage.objects.all()
    context["post_images"] = PostImage.objects.all()

    return render(request, 'cms/post/mod.html', context)

def post_index(request):
    u"""Index View"""
    context = {}

    
    if request.user.is_authenticated:
        """
        df = [dict(Task="体裁整える", Start='2021-01-01', Finish='2021-02-28'),
            dict(Task="記事10個書く", Start='2021-03-05', Finish='2021-04-15'),
            dict(Task="公開", Start='2021-04-30', Finish='2021-05-05')]

        fig = ff.create_gantt(df,title='スケジュール')
        plot_fig = plot(fig, output_type='div', include_plotlyjs=False)
        context["plot_gantt"] = plot_fig
        """
        context["comments_not_allowed"] =  Comment.objects.filter(is_publish=False)
    
    
    return render(request, 'cms/post/index.html', context)

class SmallCategoryCreate(CreateView):
    """カテゴリの作成"""
    model = SmallCategory
    fields = '__all__'
    success_url = reverse_lazy('post:list')


class TagCreate(CreateView):
    """タグの作成"""
    model = Tag
    fields = '__all__'
    success_url = reverse_lazy('post:list')


class PopupSmallCategoryCreate(SmallCategoryCreate):
    """ポップアップでのカテゴリ作成"""

    def form_valid(self, form):
        category = form.save()
        context = {
            'object_name': str(category),
            'object_pk': category.pk,
            'function_name': 'add_category'
        }
        return render(self.request, 'app/close.html', context)


class PopupTagCreate(TagCreate):
    """ポップアップでのタグ作成"""

    def form_valid(self, form):
        tag = form.save()
        context = {
            'object_name': str(tag),
            'object_pk': tag.pk,
            'function_name': 'add_tag'
        }
        return render(self.request, 'app/close.html', context)

def recaptha(req):
    import urllib, urllib.request, urllib.parse, json
    recaptcha_response = req.POST.get('g-recaptcha-response')
    url = 'https://www.google.com/recaptcha/api/siteverify'
    values = { 
        'secret': RECAPTHA_SECRET_KEY, # GOOGLE RECAPTHA SECRET KEY
        'response': recaptcha_response
    }   
    data = urllib.parse.urlencode(values).encode('utf-8')
    request = urllib.request.Request(url, data)
    response = urllib.request.urlopen(request)
    result = json.loads(response.read().decode('utf-8'))
    return result

class CommentCreate(CreateView):
    """記事へのコメント作成ビュー。"""
    model = Comment
    form_class = CommentCreateForm
    template_name =  'cms/post/comment_form.html'

    def form_valid(self, form):
        res = recaptha(self.request)
        post_pk = self.kwargs['pk']
        if res['success']:
            post = get_object_or_404(Post, pk=post_pk)
            comment = form.save(commit=False)
            comment.target = post
            comment.save()
            return redirect('post:detail', pk=post_pk)
        else:
            return redirect('post:comment_create', pk=post_pk)           

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = get_object_or_404(Post, pk=self.kwargs['pk'])
        return context

class ReplyCreate(CreateView):
    """コメントへの返信作成ビュー。"""
    model = Reply
    form_class = ReplyCreateForm
    template_name =  'cms/post/comment_form.html'

    def form_valid(self, form):
        res = recaptha(self.request)
        if res['success']:
            comment_pk = self.kwargs['pk']
            comment = get_object_or_404(Comment, pk=comment_pk)
            reply = form.save(commit=False)
            reply.target = comment
            reply.save()
            return redirect('post:detail', pk=comment.target.pk)
        else:
            pass

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comment_pk = self.kwargs['pk']
        comment = get_object_or_404(Comment, pk=comment_pk)
        context['post'] = comment.target
        return context

