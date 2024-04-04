from rest_framework import serializers
from .models import Product, Bid

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'bid_price', 'min_bid_price']


class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = ['user', 'product', 'bid_amount']



