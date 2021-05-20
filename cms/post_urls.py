"""portal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include
from django.urls import path

from cms import views

app_name = 'post'


urlpatterns = [
    #作品一覧
    path('', views.post_index, name='index'),
    path('list', views.PostListView.as_view(), name='list'),
    path('<int:pk>', views.PostDetail.as_view(), name="detail"),
    path('add/', views.post_mod, name='add'),  # 登録
    path('mod/<int:post_id>/', views.post_mod, name='mod'),  # 修正
    path('popup/category_create/', views.PopupSmallCategoryCreate.as_view(), name='popup_category_create'),
    path('popup/tag_create/', views.PopupTagCreate.as_view(), name='popup_tag_create'),
    path('comment/create/<int:pk>', views.CommentCreate.as_view(), name='comment_create'),
    path('reply/create/<int:pk>', views.ReplyCreate.as_view(), name='reply_create'),
    
]
