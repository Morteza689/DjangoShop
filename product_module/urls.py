from django.urls import path
from . import views

urlpatterns = [
    path('',views.ProductListView.as_view(),name='product-list'),
    path('cat/<cat>',views.ProductListView.as_view(),name='product-categories-list'),
    path('add-product-comment',views.add_product_comment,name='add-article-comment'),
    path('brand/<brand>',views.ProductListView.as_view(),name='product-list-by-brands'),
    path('<slug:slug>', views.ProductDetailView.as_view(), name='product-detail')
]
