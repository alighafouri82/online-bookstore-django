from django.urls import path
from .views import CartDetailView, AddToCartView, RemoveFromCartView, UpdateCartItemView

app_name = "cart"

urlpatterns = [
    path("cart/", CartDetailView.as_view(), name="cart_detail"),
    path("cart/add/<int:book_id>/", AddToCartView.as_view(), name="add_to_cart"),
    path("cart/remove/<int:item_id>/", RemoveFromCartView.as_view(), name="remove_from_cart"),
    path("cart/update/<int:item_id>/", UpdateCartItemView.as_view(), name="update_cart_item"),
]