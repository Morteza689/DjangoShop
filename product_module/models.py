import random
import os
from django.conf import settings
from django.utils.crypto import get_random_string
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.sitemaps import ping_google
from account_module.models import User


# Create your models here.


class ProductCategory(models.Model):
    title = models.CharField(max_length=300, verbose_name='عنوان', db_index=True)
    url_title = models.CharField(max_length=300, verbose_name='عنوان url', db_index=True)
    is_active = models.BooleanField(verbose_name='فغعال / غیر فعال')
    is_delete = models.BooleanField(verbose_name='حذف شده / نشده')

    def get_absolute_url(self):
        return reverse('product-categories-list', args=[self.url_title])

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False,*args, **kwargs):
        super().save(force_insert, force_update,*args, **kwargs)
        try:
            ping_google()
        except Exception:
            pass

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'


class ProductBrand(models.Model):
    title = models.CharField(max_length=255, verbose_name='نام برند', db_index=True)
    url_title = models.CharField(max_length=300, verbose_name='نام در url', db_index=True)
    is_active = models.BooleanField(verbose_name='فعال/ غیر فعال')

    def get_absolute_url(self):
        return reverse('product-list-by-brands', args=[self.url_title])

    class Meta:
        verbose_name = 'برند'
        verbose_name_plural = 'برندها'

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False,*args, **kwargs):
        super().save(force_insert, force_update,*args, **kwargs)
        try:
            ping_google()
        except Exception:
            pass


class Product(models.Model):
    title = models.CharField(max_length=300, verbose_name='نام محصول')
    price = models.IntegerField(verbose_name='قیمت')
    offer_price = models.IntegerField(verbose_name='قیمت همرا با تخفیف', null=True, blank=True)
    off = models.BooleanField(verbose_name='تخفیف خورده/نخورده', default=False)
    category = models.ManyToManyField(ProductCategory,
                                      related_name='product_catgorys',
                                      verbose_name='دسته بندی ها')
    image = models.ImageField(null=True, blank=True, verbose_name='تصویر محصول', upload_to='image/products')
    brand = models.ForeignKey(ProductBrand, on_delete=models.CASCADE, verbose_name='برند', null=True, blank=True)
    short_discription = models.CharField(max_length=500, null=True, verbose_name='توضیحات کوناه', db_index=True)
    description = models.TextField(verbose_name='توضیحات اصلی', db_index=True)
    is_active = models.BooleanField(default=False, verbose_name='فعال / غیر فعال')
    is_delete = models.BooleanField(verbose_name='حذف شده / نشده')
    slug = models.SlugField(default='', null=False, db_index=True, blank=True, unique=True, max_length=200,
                            verbose_name='عنوان در url', editable=False)
    created_deta = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    def get_absolute_url(self):
        return reverse('product-detail', args=[self.slug])

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        self.slug = f'{get_random_string(2)}-{random.randrange(1000, 9999)}'
        super().save(force_insert, force_update,*args, **kwargs)
        try:
            ping_google()
        except Exception:
            pass


    def delete(self, using=None, keep_parents=False):
        self.image.storage.delete(self.image.name)
        super().delete()



    def __str__(self):
        return self.title


    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'


class ProductTag(models.Model):
    caption = models.CharField(max_length=255, verbose_name="تگ", db_index=True)
    product_tags = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_tags', )

    class Meta:
        verbose_name = 'تگ محصول'
        verbose_name_plural = "تگ های محصول"

    def __str__(self):
        return self.caption


class ProductVisit(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    ip = models.CharField(max_length=30, verbose_name='آی پی کاربر')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='کاربر')

    def __str__(self):
        return f'{self.product.title}/{self.ip}'

    class Meta:
        verbose_name = 'بازدید محصول'
        verbose_name_plural = 'بازدیدهای محصول'


class ProductGallery(models.Model):
    product = models.ForeignKey(Product, verbose_name='محصول', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/product-gallery', verbose_name='تصویر')

    def __str__(self):
        return self.product.title

    def delete(self, using=None, keep_parents=False):
        self.image.storage.delete(self.image.name)
        super().delete()

    class Meta:
        verbose_name = 'تصویر گالری'
        verbose_name_plural = 'گالری تصاویر'


class ProductComment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    create_date = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='تاریخ ثبت')
    text = models.TextField(verbose_name='متن نظر')
    is_suggested = models.BooleanField(verbose_name='پیشنهاد میشود/نمیشود', default=True)

    class Meta:
        verbose_name = 'نظر محصول'
        verbose_name_plural = 'نظرات محصول'

    def __str__(self):
        return str(self.user)
