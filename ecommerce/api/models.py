from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit


class Category(models.Model):
    name = models.CharField(max_length=50)


class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    price = models.FloatField()
    category = models.ForeignKey(Category, related_name="products", null=True, on_delete=models.SET_NULL)
    image = models.ImageField(upload_to="products")
    image_thumbnail = ImageSpecField(source="image", processors=[ResizeToFit(width=200, upscale=False)], format="PNG")


class Order(models.Model):
    client = models.ForeignKey(User, related_name="orders", null=True, on_delete=models.SET_NULL)
    client_name = models.CharField(max_length=50)
    delivery_address = models.CharField(max_length=50)
    products_list = models.JSONField()
    date = models.DateField(auto_now_add=True)
    payment_date = models.DateField(null=True)
    total = models.FloatField(null=True)


class OrderProducts(models.Model):
    order = models.ForeignKey(Order, related_name="products", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="ordered", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
