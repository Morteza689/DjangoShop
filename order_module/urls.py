from django.urls import path
from . import views
urlpatterns=[
    path('add-to-order/',views.add_product_to_order,name='add-product-to-order'),
    path('request-payment/', views.request_payment, name='request_payment'),
    path('verify-payment/', views.verify_payment, name='verify_payment'),
]
