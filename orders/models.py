from django.db import models
from django.contrib.auth.models import User
from books.models import Book


class Order(models.Model):

    class Status(models.TextChoices):
        PENDING = "pending", "در انتظار تأیید"
        CONFIRMED = "confirmed", "تأیید شده"
        SHIPPED = "shipped", "ارسال شده"
        DELIVERED = "delivered", "تحویل داده شده"
        CANCELLED = "cancelled", "لغو شده"

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name="کاربر",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name="وضعیت",
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="قیمت کل",
    )
    shipping_address = models.TextField(verbose_name="آدرس ارسال")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    class Meta:
        verbose_name = "سفارش"
        verbose_name_plural = "سفارش‌ها"
        ordering = ["-created_at"]

    def __str__(self):
        return f"سفارش #{self.id} — {self.user.username} — {self.get_status_display()}"

    @property
    def is_cancellable(self):
        return self.status in (self.Status.PENDING, self.Status.CONFIRMED)


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="سفارش",
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.SET_NULL,
        null=True,
        related_name="order_items",
        verbose_name="کتاب",
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name="تعداد")
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="قیمت واحد",
    )

    class Meta:
        verbose_name = "آیتم سفارش"
        verbose_name_plural = "آیتم‌های سفارش"

    def __str__(self):
        book_title = self.book.title if self.book else "کتاب حذف شده"
        return f"{self.quantity} × {book_title} (سفارش #{self.order.id})"

    @property
    def subtotal(self):
        return self.unit_price * self.quantity