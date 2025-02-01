from django.db import models
from account_module.models import User ,UserAddress
from product_module.models import Product
# Create your models here.

class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='کاربر')
    is_paid=models.BooleanField(verbose_name='نهایی شده/نشده',)
    paymant_date=models.DateField(verbose_name='تاریخ پرداخت',null=True,blank=True)
    posted=models.BooleanField(verbose_name='ارسال شده/نشده',default=False)
    ref_code_post=models.CharField(max_length=30,verbose_name='کد پیگیری پست',null=True,blank=True)
    address=models.ForeignKey(UserAddress,on_delete=models.CASCADE,verbose_name='آدرس',null=True,blank=True)

    def __str__(self):
        return str(self.user)

    def calculate_total_price(self):
        total_amount = 0
        if self.is_paid:
            for order_detail in self.orderdetaile_set.all():
                total_amount += order_detail.final_price * order_detail.count
        else:
            for order_detail in self.orderdetaile_set.all():
                if order_detail.product.off:
                    total_amount += order_detail.product.offer_price * order_detail.count
                else:
                    total_amount += order_detail.product.price * order_detail.count
        return total_amount

    class Meta:
        verbose_name='سبد خرید'
        verbose_name_plural='سبد خرید کاربران'

class OrderDetaile(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,verbose_name='سبد خرید')
    product=models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name='محصول')
    final_price=models.IntegerField(null=True,blank=True,verbose_name='قیمت نهایی تکی محصول')
    count=models.IntegerField(verbose_name='تعداد')

    def __str__(self):
        return str(self.order)

    class Meta:
        verbose_name='جزییات سبد خرید'
        verbose_name_plural='جزییات سبد خرید کاربران'