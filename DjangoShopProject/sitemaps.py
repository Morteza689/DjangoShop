from django.contrib.sitemaps import Sitemap
from product_module.models import *



class ProductSitemaps(Sitemap):
    changefreq = "daily"
    priority = 0.7

    def items(self):
        return Product.objects.filter(is_active=True)
    def lastmod(self, obj:Product):
        return obj.created_deta


class BrandSitemaps(Sitemap):
    changefreq = "daily"
    priority = 0.7

    def items(self):
        return ProductBrand.objects.filter(is_active=True)

class CategorySitemaps(Sitemap):
    changefreq = "daily"
    priority = 0.7

    def items(self):
        return ProductCategory.objects.filter(is_active=True)



class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return ['/']

    def location(self, item):
        return item