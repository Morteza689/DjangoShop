from django.db.models import Count, Sum
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views import View

from product_module.models import Product,ProductCategory
from site_module.models import SiteSetting, FooterLinkBox, Slider, SiteBanner
from utils.convertors import group_list


# Create your views here.


class HomeView(TemplateView):
    template_name = 'home_moduls/index_page.html'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['sliders']=Slider.objects.filter(is_active=True)
        latest_products=Product.objects.filter(is_active=True,is_delete=False).order_by('-id')[:12]
        most_visit_product=Product.objects.filter(is_active=True,is_delete=False).annotate(Count('productvisit')).order_by('-productvisit')[:12]
        context['latest_products']=group_list(latest_products)
        context['most_visit_product']=group_list(most_visit_product)
        context['offer_products']=Product.objects.filter(is_active=True,is_delete=False,off=True).order_by('-id')[:5]
        categories=list(ProductCategory.objects.annotate(products_count=Count('product_catgorys')).filter(is_active=True,is_delete=False,products_count__gt=0)[:6])
        categories_products=[]
        for category in categories:
            item={
                'id':category.id,
                'title':category.title,
                'products': list(category.product_catgorys.all()[:4])
            }
            categories_products.append(item)
        context['categories_products']=categories_products
        context['banners']=SiteBanner.objects.filter(is_active=True,position__iexact=SiteBanner.SiteBannerPosition.home_page)[:2]
        most_bought_product=Product.objects.filter(orderdetaile__order__is_paid=True).annotate(product_count=Sum('orderdetaile__count')).order_by('-product_count')[:9]
        context['most_bought_product']=group_list(most_bought_product)


        return context



class AbuotView(TemplateView):
    template_name = 'home_moduls/abuot_page.html'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['site_setting']=SiteSetting.objects.filter(is_main_setting=True).first()
        return context



def site_header_component(requests):
    setting:SiteSetting =SiteSetting.objects.filter(is_main_setting=True).first()
    context={
        'site_setting':setting
    }
    return render(requests,'shared/site_header_component.html',context)

def site_footer_component(requests):
    setting:SiteSetting =SiteSetting.objects.filter(is_main_setting=True).first()
    footer_link_boxs=FooterLinkBox.objects.all()
    context={
        'footer_link_boxs':footer_link_boxs,
        'site_setting':setting
    }
    return render(requests,'shared/site_footer_component.html',context)

def site_setting(request):
    return {'site_setting':SiteSetting.objects.filter(is_main_setting=True).first()}