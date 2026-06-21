from django.urls import path
from .views import OrderListView, OrderDetailView, CheckoutView

app_name = "orders"

urlpatterns = [
    path("orders/", OrderListView.as_view(), name="order_list"),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="order_detail"),
    path("orders/checkout/", CheckoutView.as_view(), name="checkout"),
]