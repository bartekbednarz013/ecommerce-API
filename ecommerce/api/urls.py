from django.urls import include, path
from rest_framework import routers
from rest_framework import urls
from .api import ProductViewSet, MakeOrderAPI, OrderStatisticsAPI


router = routers.DefaultRouter()
router.register("product", ProductViewSet, "product")

urlpatterns = [
    path("auth/", include(urls, namespace="rest_framework")),
    path("order", MakeOrderAPI.as_view()),
    path("statistics", OrderStatisticsAPI.as_view()),
]

urlpatterns += router.urls
