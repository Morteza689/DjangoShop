from django.contrib import admin
from django.urls import path ,include
from django.contrib.sitemaps.views import sitemap
from django.conf.urls.static import static
from django.conf import settings
from DjangoShopProject.sitemaps import *

sitemaps = {
    'site':StaticViewSitemap,
    'product':ProductSitemaps,
    'brand':BrandSitemaps,
    'Category':CategorySitemaps,
}




urlpatterns = [
    path('admin/', admin.site.urls ,),
    path('', include('account_module.urls')),
    path('', include('home_moduls.urls')),
    path('products/', include('product_module.urls')),
    path('contact-us/', include('contact_module.urls')),
    path('order/', include('order_module.urls')),
    path('user/', include('user_panel_module.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap')
]

urlpatterns+=(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
