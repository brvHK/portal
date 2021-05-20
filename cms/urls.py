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

app_name = 'cms'


urlpatterns = [
    #作品一覧
    path('', views.ItemList.as_view(), name='item_list'),
    path('<int:pk>', views.ItemDetail.as_view(), name="item_detail"),
    path('add/', views.mod, name='item_add'),  # 登録
    path('mod/<int:item_id>/', views.mod, name='item_mod'),  # 修正
    #path(r'^del/(?P<art_id>\d+)/$', views.delete, name='item_del'),   # 削除
    #url(r'^', views.index, name="index"),
    #url(r'^img/(?P<path>.*)$','django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    
]
