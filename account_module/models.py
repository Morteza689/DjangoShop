from django.contrib.auth.models import AbstractUser
from django.db import models
import random
# Create your models here.

class User(AbstractUser):
    national_code=models.IntegerField(blank=True,null=True,verbose_name='کد ملی')
    number=models.IntegerField(verbose_name='شماره موبایل',unique=True,null=True,blank=True)
    number_is_active = models.BooleanField(default=False,verbose_name='فعال بودن/نبودن شماره')
    number_active_code=models.IntegerField(verbose_name='کد فعالسازی شماره',default=random.randrange(10000, 99999))
    email_active_code=models.CharField(max_length=100,verbose_name='کد فعالسازی ایمیل')
    abuot_user=models.TextField(null=True,blank=True,verbose_name='درباره شخص')

    class Meta:
        verbose_name='کاربر'
        verbose_name_plural='کاربران'


    def __str__(self):
        if self.last_name is not '' and self.first_name is not '':
            return self.get_full_name()
        return self.email


class UserAddress(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='کاربر')
    receiver=models.CharField(max_length=200,verbose_name='گیرنده',)
    number_receiver=models.IntegerField(verbose_name='شماره گیرنده')
    address=models.TextField(verbose_name='آدرس')
    zipcode=models.IntegerField(verbose_name='کد پستی')

    class Meta:
        verbose_name='آدرس'
        verbose_name_plural='آدرس ها'

    def __str__(self):
        return self.address




