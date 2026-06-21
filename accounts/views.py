from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.auth.views import LogoutView as DjangoLogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login
from django.views import View
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm


class RegisterView(View):
    template_name = "accounts/register.html"
    form_class = UserRegistrationForm

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("books:home")
        return render(request, self.template_name, {"form": self.form_class()})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(
                request,
                f"حساب کاربری شما با موفقیت ساخته شد. لطفاً وارد شوید."
            )
            return redirect("accounts:login")
        messages.error(
            request,
            "لطفاً خطاهای زیر را برطرف کنید."
        )
        return render(request, self.template_name, {"form": form})


class LoginView(DjangoLoginView):
    template_name = "accounts/login.html"
    authentication_form = AuthenticationForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return self.get_redirect_url() or "/"

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        messages.success(
            self.request,
            f"خوش آمدید {user.get_full_name() or user.username}! ورود با موفقیت انجام شد."
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "نام کاربری یا رمز عبور اشتباه است. لطفاً دوباره تلاش کنید."
        )
        return super().form_invalid(form)


class LogoutView(DjangoLogoutView):
    next_page = "books:home"

    def dispatch(self, request, *args, **kwargs):
        messages.info(
            request,
            "با موفقیت از حساب کاربری خود خارج شدید."
        )
        return super().dispatch(request, *args, **kwargs)