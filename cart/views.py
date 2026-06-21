from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from books.models import Book
from .models import Cart, CartItem


class CartDetailView(LoginRequiredMixin, View):
    template_name = "cart/cart_detail.html"
    login_url = "accounts:login"

    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        items = cart.items.select_related("book", "book__category").all()
        return render(request, self.template_name, {
            "cart": cart,
            "items": items,
        })


class AddToCartView(LoginRequiredMixin, View):
    login_url = "accounts:login"

    def post(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)

        if not book.is_available:
            messages.error(
                request,
                f"متأسفانه کتاب «{book.title}» در حال حاضر موجود نیست."
            )
            return redirect("books:book_detail", slug=book.slug)

        try:
            quantity = int(request.POST.get("quantity", 1))
            if quantity < 1:
                quantity = 1
        except (ValueError, TypeError):
            quantity = 1

        if quantity > book.stock:
            messages.error(
                request,
                f"تعداد درخواستی از موجودی انبار ({book.stock} عدد) بیشتر است."
            )
            return redirect("books:book_detail", slug=book.slug)

        cart, _ = Cart.objects.get_or_create(user=request.user)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            book=book,
        )

        if created:
            cart_item.quantity = quantity
            messages.success(
                request,
                f"کتاب «{book.title}» با موفقیت به سبد خرید اضافه شد."
            )
        else:
            new_quantity = cart_item.quantity + quantity
            if new_quantity > book.stock:
                messages.warning(
                    request,
                    f"امکان افزایش تعداد وجود ندارد. موجودی انبار: {book.stock} عدد."
                )
                return redirect("cart:cart_detail")
            cart_item.quantity = new_quantity
            messages.success(
                request,
                f"تعداد کتاب «{book.title}» در سبد خرید به {cart_item.quantity} عدد افزایش یافت."
            )

        cart_item.save()
        return redirect("cart:cart_detail")


class RemoveFromCartView(LoginRequiredMixin, View):
    login_url = "accounts:login"

    def post(self, request, item_id):
        cart = get_object_or_404(Cart, user=request.user)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        book_title = cart_item.book.title
        cart_item.delete()
        messages.success(request, f"کتاب «{book_title}» از سبد خرید حذف شد.")
        return redirect("cart:cart_detail")


class UpdateCartItemView(LoginRequiredMixin, View):
    login_url = "accounts:login"

    def post(self, request, item_id):
        cart = get_object_or_404(Cart, user=request.user)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)

        try:
            quantity = int(request.POST.get("quantity", 1))
        except (ValueError, TypeError):
            messages.error(request, "تعداد وارد شده معتبر نیست.")
            return redirect("cart:cart_detail")

        if quantity < 1:
            cart_item.delete()
            messages.success(request, f"کتاب «{cart_item.book.title}» از سبد خرید حذف شد.")
            return redirect("cart:cart_detail")

        if quantity > cart_item.book.stock:
            messages.error(
                request,
                f"تعداد درخواستی از موجودی انبار ({cart_item.book.stock} عدد) بیشتر است."
            )
            return redirect("cart:cart_detail")

        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, f"تعداد کتاب «{cart_item.book.title}» بروزرسانی شد.")
        return redirect("cart:cart_detail")