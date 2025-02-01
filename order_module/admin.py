from django.contrib import admin
from .models import *
# Register your models here.


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user','posted','ref_code_post','is_paid']
    list_editable = ['posted','ref_code_post']


class OrderDetaileAdmin(admin.ModelAdmin):
    list_display = ['order','product','final_price','count']


admin.site.register(Order,OrderAdmin)
admin.site.register(OrderDetaile,OrderDetaileAdmin)