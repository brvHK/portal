from django.contrib import admin
from django.urls import include
from django.urls import path

from api.views import ItemList
from api.views import ItemDetail

app_name = 'api'

urlpatterns = [
    path('<int:pk>', ItemDetail.as_view(), name="item_detail"),
    path('', ItemList.as_view(), name="item_list"),
]