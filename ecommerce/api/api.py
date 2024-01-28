from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView, ListAPIView
from .serializers import ProductSerializer, OrderSerializer, OrderStatisticsSerializer
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.db.models import Sum
from .models import Product, OrderProducts
from .permissions import ProductPermission, OrderPermission, SellerPermission
from datetime import date, timedelta, datetime
from .tasks import send_payment_reminder
from rest_framework.exceptions import ValidationError


class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [ProductPermission]

    def get_queryset(self):
        params = self.request.query_params
        queryset = Product.objects.all()
        if "sort_by" in params:
            sort_value = params.get("sort_by")
            if sort_value in ["name", "-name", "category", "-category", "price", "-price"]:
                queryset = Product.objects.all().order_by(params.get("sort_by"))
        if "name" in params:
            queryset = queryset.filter(name__contains=params.get("name"))
        if "category" in params:
            queryset = queryset.filter(category=params.get("category"))
        if "description" in params:
            queryset = queryset.filter(description__contains=params.get("description"))
        if "min_price" in params:
            queryset = queryset.filter(price__gte=params.get("min_price"))
        if "max_price" in params:
            queryset = queryset.filter(price__lte=params.get("max_price"))
        return queryset


class MakeOrderAPI(CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [OrderPermission]

    def post(self, request, *args, **kwargs):
        order = self.save_order(request)
        self.send_order_confirmation(order)
        self.create_reminder_task(order)
        return Response({"total": order.total, "payment_date": order.payment_date}, status=status.HTTP_201_CREATED)

    def save_order(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        products_list = request.data["products_list"]
        self.validate_products_list(products_list)
        order = serializer.save(client=request.user)
        order.payment_date = self._calculate_payment_date()
        total = 0
        for item in products_list:
            product = Product.objects.get(id=item["id"])
            quantity = item["quantity"]
            total += product.price * quantity
            orderProducts = OrderProducts(order=order, product=product, quantity=quantity)
            orderProducts.save()
        order.total = total
        order.save()
        return order

    @staticmethod
    def _calculate_payment_date():
        return date.today() + timedelta(days=5)

    def send_order_confirmation(self, order):
        mail_subject = f"Nowe zamówienie nr {order.id}"
        products_string = ""
        for item in order.products_list:
            product = Product.objects.get(id=item["id"])
            quantity = item["quantity"]
            products_string += (
                f"\n{product.name}; {product.price} zł/szt; {quantity} szt; {product.price * quantity}zł"
            )
        mail_message = f"Dzień dobry,\npotwierdzamy przyjęcie zamówienia nr {order.id} z dnia {order.date}.\n\nZamówione produkty:{products_string}\n\nKwota do zapłaty: {order.total}zł.\nTermin płatności: {order.payment_date}"
        send_mail(
            subject=mail_subject,
            message=mail_message,
            from_email="ecommerce@example.com",
            recipient_list=[order.client.email],
        )

    def create_reminder_task(self, order):
        day_to_send_reminder = order.payment_date - timedelta(days=1)
        eta = datetime(year=day_to_send_reminder.year, month=day_to_send_reminder.month, day=day_to_send_reminder.day)
        send_payment_reminder.apply_async(args=[order.id], eta=eta)

    def validate_products_list(self, products_list):
        if products_list == [] or not isinstance(products_list, list):
            raise ValidationError()
        total = 0
        for item in products_list:
            try:
                product = Product.objects.get(id=item["id"])
                quantity = item["quantity"]
                if quantity == 0:
                    raise Exception
                total += product.price * quantity
            except:
                raise ValidationError()


class OrderStatisticsAPI(ListAPIView):
    serializer_class = OrderStatisticsSerializer
    permission_classes = [SellerPermission]

    def list(self, request, *args, **kwargs):
        params = request.query_params
        queryset = (
            OrderProducts.objects.filter(order__date__gte=params.get("from_date"))
            if "from_date" in params
            else OrderProducts.objects
        )
        queryset = queryset.filter(order__date__lte=params.get("to_date")) if "to_date" in params else queryset
        queryset = (
            queryset.values("product__id", "product__name")
            .annotate(total_quantity=Sum("quantity"))
            .order_by("-total_quantity")
        )
        queryset = queryset[: int(params.get("count"))] if "count" in params else queryset

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
