from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("book", "quantity", "unit_price", "subtotal")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status", "total_price", "created_at", "updated_at")
    search_fields = ("user__username", "user__email")
    list_filter = ("status", "created_at")
    readonly_fields = ("total_price", "created_at", "updated_at")
    ordering = ("-created_at",)
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "book", "quantity", "unit_price", "subtotal")
    search_fields = ("order__user__username", "book__title")
    list_filter = ("order__status",)
    readonly_fields = ("subtotal",)