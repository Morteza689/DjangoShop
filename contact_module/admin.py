from django.contrib import admin
from .models import *

# Register your models here.
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['title','full_name','email','is_read_by_admin']
    list_editable = ['is_read_by_admin']



admin.site.register(ContactUs,ContactUsAdmin)