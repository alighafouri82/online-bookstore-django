from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="نام")
    slug = models.SlugField(max_length=120, unique=True, blank=True, verbose_name="اسلاگ")
    description = models.TextField(blank=True, verbose_name="توضیحات")

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="نام")
    last_name = models.CharField(max_length=100, verbose_name="نام خانوادگی")
    bio = models.TextField(blank=True, verbose_name="بیوگرافی")
    photo = models.ImageField(upload_to="authors/", blank=True, null=True, verbose_name="تصویر")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    class Meta:
        verbose_name = "نویسنده"
        verbose_name_plural = "نویسندگان"
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Book(models.Model):
    title = models.CharField(max_length=255, verbose_name="عنوان")
    isbn = models.CharField(max_length=20, unique=True, verbose_name="شابک")
    publisher = models.CharField(max_length=200, verbose_name="ناشر")
    slug = models.SlugField(max_length=275, unique=True, blank=True, verbose_name="اسلاگ")
    description = models.TextField(verbose_name="توضیحات")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="قیمت")
    stock = models.PositiveIntegerField(default=0, verbose_name="موجودی")
    cover_image = models.ImageField(upload_to="books/covers/", blank=True, null=True, verbose_name="تصویر جلد")
    published_date = models.DateField(verbose_name="تاریخ انتشار")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="books",
        verbose_name="دسته‌بندی",
    )
    authors = models.ManyToManyField(
        Author,
        related_name="books",
        verbose_name="نویسندگان",
    )

    class Meta:
        verbose_name = "کتاب"
        verbose_name_plural = "کتاب‌ها"
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def is_available(self):
        return self.stock > 0