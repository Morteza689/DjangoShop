from django.urls import  path
from .views import *

urlpatterns=[
    path('',ContactUsView.as_view(),name='contact_us_page'),
]
