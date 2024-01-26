from rest_framework import serializers
from .models import Product, Order


class ProductSerializer(serializers.ModelSerializer):
    image_thumbnail = serializers.ImageField(read_only=True)

    class Meta:
        model = Product
        fields = ["id", "name", "description", "price", "category", "image", "image_thumbnail"]


class OrderSerializer(serializers.ModelSerializer):
    client = serializers.ReadOnlyField()
    total = serializers.FloatField(read_only=True)
    payment_date = serializers.DateField(read_only=True)

    class Meta:
        model = Order
        fields = [
            "client",
            "client_name",
            "delivery_address",
            "products_list",
            "date",
            "payment_date",
            "total",
        ]


class OrderStatisticsSerializer(serializers.Serializer):
    product__id = serializers.IntegerField()
    product__name = serializers.CharField()
    total_quantity = serializers.IntegerField()
