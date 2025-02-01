from django.db import models

# Create your models here.

class SiteSetting(models.Model):
    site_name =models.CharField(max_length=200 ,verbose_name='نام سایت')
    site_description=models.TextField(verbose_name='توضیحات')
    site_url = models.CharField(max_length=200, verbose_name='دامنه سایت')
    instagram_url = models.URLField(verbose_name='لینک اینستگرام',blank=True)
    telegram_url = models.URLField(verbose_name='لینک تلگرام',blank=True)
    address = models.CharField(max_length=200, verbose_name='آدرس')
    phone = models.CharField(max_length=200,null=True,blank=True, verbose_name='تلفن')
    email = models.CharField(max_length=200,null=True,blank=True, verbose_name='ایمیل')
    copy_right = models.TextField( verbose_name='کپی رایت')
    about_us_text = models.TextField( verbose_name='درباره سایت')
    site_logo=models.ImageField(upload_to='images/site-setting/',verbose_name='لوگوی سایت')
    site_favicon=models.ImageField(upload_to='images/site-setting/',verbose_name='لوگوی سایت در url')
    is_main_setting = models.BooleanField(verbose_name='تنظیمات اصلی')



    class Meta:
        verbose_name='تنظیمات سایت'
        verbose_name_plural='تنظیمات'

    def __str__(self):
        return self.site_name


class FooterLinkBox(models.Model):
    title=models.CharField(max_length=200,verbose_name='عنوان')

    class Meta:
        verbose_name='دسته بندی لینک های فوتر'
        verbose_name_plural='دسته بندی های لینک های فوتر'

    def __str__(self):
        return self.title


class FooterLink(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان')
    url= models.URLField(max_length=500,verbose_name='لینک')
    footer_link_box=models.ForeignKey(to=FooterLinkBox,on_delete=models.CASCADE,verbose_name='دسته بندی')


    class Meta:
        verbose_name = ' لینک فوتر'
        verbose_name_plural = ' لینک های فوتر'

    def __str__(self):
        return self.title



class Slider(models.Model):
    title=models.CharField(max_length=200,verbose_name='عنوان')
    url = models.URLField(max_length=500, verbose_name='لینک')
    url_title = models.CharField(max_length=200, verbose_name='عنوان لینک')
    descriphtion = models.TextField(max_length=200, verbose_name='توضیحات اسلایدر')
    image=models.ImageField(upload_to='images/sliders/',verbose_name='تصویر اسلایدر')
    is_active=models.BooleanField(verbose_name='فعال / غیر فعال',default=False)

    class Meta:
        verbose_name='اسلایدر'
        verbose_name_plural='اسلاید ها'

    def __str__(self):
        return self.title



class SiteBanner(models.Model):
    class SiteBannerPosition(models.TextChoices):
        product_list='product_list','صفحه لیست محصولات'
        product_detail='product_detail','صفحه جزییات محصول'
        home_page='home_page','صفحه خانه'

    title=models.CharField(max_length=200,verbose_name='عنوان بنر')
    url=models.URLField(null=True,blank=True,max_length=200,verbose_name='url بنر')
    image=models.ImageField(upload_to='images/banners',verbose_name='تصویر بنر')
    is_active=models.BooleanField(verbose_name='فعال/غیرفعال')
    position=models.CharField(max_length=200,choices=SiteBannerPosition.choices,verbose_name='جایگاه نمایشی')

    def __str__(self):
        return self.title

    class Meta():
        verbose_name='بنر'
        verbose_name_plural='بنرها'
