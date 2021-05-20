from django.shortcuts import render
from rest_framework import generics

from cms.models import Item
from .serializers import ItemSerializer


class ItemListAPIView(generics.ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class ItemList(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


# RetrieveUpdateDestoryAPIView -> ALlows read, update, delete
class ItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
# Create your views here.
