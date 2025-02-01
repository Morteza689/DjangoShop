from django.contrib import admin
from .models import *
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_filter = ['category','is_active',]
    list_display =['title','price','is_active','is_delete','brand']
    list_editable =['price','is_active']

class ProductCommentAdmin(admin.ModelAdmin):
    list_display = ['product','user','is_suggested',]


admin.site.register(ProductTag)
admin.site.register(Product,ProductAdmin)
admin.site.register(ProductCategory)
admin.site.register(ProductBrand)
admin.site.register(ProductVisit)
admin.site.register(ProductGallery)
admin.site.register(ProductComment,ProductCommentAdmin)

