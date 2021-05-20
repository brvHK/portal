# coding:utf-8

from django.urls import path
from django.urls import include
from story import views

urlpatterns =[
    #作品一覧
    path('', views.IndexView.as_view(), name='Index'),
    path('prologue', views.IndexView.as_view(), name='Index'),
    path('prologue/1st', views.First.as_view(), name='First'),
    path('prologue/2nd', views.Second.as_view(), name='Second'),
    path('prologue/3rd', views.IndexView.as_view(), name='Third'),
    #url(r'^main/$', views.MainView.as_view(), name='Main'),
]