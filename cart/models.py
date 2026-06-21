from django.db import models
from django.contrib.auth.models import User
from books.models import Book


class Cart(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="cart",
        verbose_name="کاربر",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    class Meta:
        verbose_name = "سبد خرید"
        verbose_name_plural = "سبدهای خرید"

    def __str__(self):
        return f"سبد خرید {self.user.username}"

    @property
    def total_price(self):
        return sum(item.subtotal for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="سبد خرید",
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="cart_items",
        verbose_name="کتاب",
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name="تعداد")

    class Meta:
        verbose_name = "آیتم سبد خرید"
        verbose_name_plural = "آیتم‌های سبد خرید"
        unique_together = ("cart", "book")

    def __str__(self):
        return f"{self.quantity} × {self.book.title}"

    @property
    def subtotal(self):
        return self.book.price * self.quantity