from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from cart.models import Cart
from .models import Order, OrderItem


class OrderListView(LoginRequiredMixin, View):
    template_name = "orders/order_list.html"
    login_url = "accounts:login"

    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by("-created_at")
        return render(request, self.template_name, {"orders": orders})


class OrderDetailView(LoginRequiredMixin, View):
    template_name = "orders/order_detail.html"
    login_url = "accounts:login"

    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk, user=request.user)
        items = order.items.select_related("book").all()
        return render(request, self.template_name, {
            "order": order,
            "items": items,
        })


class CheckoutView(LoginRequiredMixin, View):
    template_name = "orders/checkout.html"
    login_url = "accounts:login"

    def get(self, request):
        cart = get_object_or_404(Cart, user=request.user)
        items = cart.items.select_related("book").all()

        if not items.exists():
            messages.warning(request, "سبد خرید شما خالی است. ابتدا کتابی اضافه کنید.")
            return redirect("cart:cart_detail")

        return render(request, self.template_name, {
            "cart": cart,
            "items": items,
        })

    def post(self, request):
        cart = get_object_or_404(Cart, user=request.user)
        items = cart.items.select_related("book").all()

        if not items.exists():
            messages.warning(request, "سبد خرید شما خالی است. ابتدا کتابی اضافه کنید.")
            return redirect("cart:cart_detail")

        shipping_address = request.POST.get("shipping_address", "").strip()
        if not shipping_address:
            messages.error(request, "لطفاً آدرس ارسال را وارد کنید.")
            return render(request, self.template_name, {
                "cart": cart,
                "items": items,
            })

        for item in items:
            if item.quantity > item.book.stock:
                messages.error(
                    request,
                    f"موجودی کتاب «{item.book.title}» کافی نیست. "
                    f"موجودی فعلی: {item.book.stock} عدد."
                )
                return redirect("cart:cart_detail")

        total_price = cart.total_price

        order = Order.objects.create(
            user=request.user,
            status=Order.Status.PENDING,
            total_price=total_price,
            shipping_address=shipping_address,
        )

        for item in items:
            OrderItem.objects.create(
                order=order,
                book=item.book,
                quantity=item.quantity,
                unit_price=item.book.price,
            )
            item.book.stock -= item.quantity
            item.book.save()

        cart.items.all().delete()

        messages.success(
            request,
            f"سفارش شما با موفقیت ثبت شد. شماره سفارش: #{order.id}"
        )
        return redirect("orders:order_detail", pk=order.id)