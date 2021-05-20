from rest_framework import serializers

from cms.models import Item


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('name', 'detail', 'category', 'chapter', 'date', 'minne_url', 'is_sold', 'price', 'price_sold', 'comment')