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
from django.views.generic import TemplateView

from cms import views
from cms.views import InformationView
from cms.views import Login
from cms.views import Logout

# 追加
admin.site.site_title = 'Fの世界' 
admin.site.site_header = 'Fの世界' 
admin.site.index_title = 'メニュー'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls')),
    path('', views.index,name='index'),
    path('information/', InformationView.as_view(),name='information'),
    path('item/', include('cms.urls')),
    path('about/HaLu', TemplateView.as_view(template_name = 'cms/about/HaLu.html'), name='HaLu'),
    path('about/Ken', TemplateView.as_view(template_name = 'cms/about/Ken.html'), name='Ken'),
    path('about/this-site', views.WorldOfFView.as_view(), name='this-site'),
    path('privacy-policy', views.PrivacyPolicyView.as_view(), name='privacy-policy'),
    path('story/', include('story.urls')),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('markdownx/', include('markdownx.urls')), 
    path('post/', include('cms.post_urls')),
    path('cms/', include('kakeibo.urls')),
]
