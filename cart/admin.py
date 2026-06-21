from django.contrib import admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ("subtotal",)
    fields = ("book", "quantity", "subtotal")


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user", "total_price", "item_count", "created_at")
    search_fields = ("user__username", "user__email")
    readonly_fields = ("total_price", "created_at")
    ordering = ("-created_at",)
    inlines = [CartItemInline]

    @admin.display(description="تعداد اقلام")
    def item_count(self, obj):
        return obj.items.count()


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("cart", "book", "quantity", "subtotal")
    search_fields = ("cart__user__username", "book__title")
    list_filter = ("book__category",)
    readonly_fields = ("subtotal",)