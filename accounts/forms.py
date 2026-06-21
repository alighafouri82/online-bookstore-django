from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        label="نام کاربری",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "نام کاربری خود را وارد کنید",
        }),
    )
    first_name = forms.CharField(
        max_length=100,
        label="نام",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "نام خود را وارد کنید",
        }),
    )
    last_name = forms.CharField(
        max_length=100,
        label="نام خانوادگی",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "نام خانوادگی خود را وارد کنید",
        }),
    )
    email = forms.EmailField(
        required=True,
        label="ایمیل",
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "ایمیل خود را وارد کنید",
        }),
    )
    password1 = forms.CharField(
        label="رمز عبور",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "رمز عبور خود را وارد کنید",
        }),
    )
    password2 = forms.CharField(
        label="تکرار رمز عبور",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "رمز عبور را دوباره وارد کنید",
        }),
    )

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("این ایمیل قبلاً توسط کاربر دیگری ثبت شده است.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("این نام کاربری قبلاً استفاده شده است.")
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user