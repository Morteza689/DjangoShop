from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404

from site_module.models import SiteBanner
from .models import Product, ProductCategory, ProductBrand, ProductVisit, ProductGallery, ProductComment
from django.views.generic import ListView, DetailView
from django.db.models import Avg, Count
from utils.http_service import get_client_ip
from utils.convertors import group_list


# Create your views here.

class ProductListView(ListView):
    template_name = 'product_module/product_list.html'
    model = Product
    context_object_name = 'products'
    ordering = ['-created_deta']
    paginate_by = 12

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data()
        product = Product.objects.all().order_by('-price').first()
        db_max_price = product.price if product is not None else 10000000
        context['db_max_price'] = db_max_price
        context['start_price'] = self.request.GET.get('start_price') or 0
        context['end_price'] = self.request.GET.get('end_price') or db_max_price
        context['banners'] = SiteBanner.objects.filter(is_active=True,
                                                       position__iexact=SiteBanner.SiteBannerPosition.product_list)
        return context

    def get_queryset(self):
        query = super(ProductListView, self).get_queryset()
        category_name = self.kwargs.get('cat')
        brand_name = self.kwargs.get('brand')
        request: HttpRequest = self.request
        start_price = request.GET.get('start_price')
        end_price = request.GET.get('end_price')
        search = request.GET.get('search')
        if start_price is not None:
            query = query.filter(price__gte=start_price)

        if end_price is not None:
            query = query.filter(price__lte=end_price)

        if category_name is not None:
            query = query.filter(category__url_title__iexact=category_name)

        if search is not None:
            query = query.filter(title__contains=search)

        if brand_name is not None:
            query = query.filter(brand__url_title__iexact=brand_name)
        return query


class ProductDetailView(DetailView):
    template_name = 'product_module/product_detail.html'
    model = Product

    def get_queryset(self):
        base_query = super(ProductDetailView, self).get_queryset()
        data = base_query.filter(is_active=True)
        return data

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data()
        product = self.object
        request: HttpRequest = self.request
        gallery_list = list(ProductGallery.objects.filter(product_id=product.id).all())
        gallery_list.insert(0, product)
        context['banners'] = SiteBanner.objects.filter(is_active=True,
                                                       position__iexact=SiteBanner.SiteBannerPosition.product_detail)
        context['gallery_product'] = gallery_list
        context['related_products'] = list(
            Product.objects.filter(brand_id=product.brand_id).exclude(pk=product.id).all()[:12])

        context['comments'] = ProductComment.objects.filter(product_id=product.id).order_by('-create_date')
        context['comments_count'] = ProductComment.objects.filter(product_id=product.id).count()

        user_ip = get_client_ip(request)
        user_id = None
        if request.user.is_authenticated:
            user_id = request.user.id
        has_been_visited = ProductVisit.objects.filter(ip__iexact=user_ip, product=product).exists()
        if not has_been_visited:
            new_visit = ProductVisit(ip=user_ip, user_id=user_id, product_id=product.id)
            new_visit.save()
        return context


# def product_ditail(request,slug):
#     product=get_object_or_404(Product,slug=slug)
#     return render(request, 'product_module/product_detail.html', {
#         'product':product
#     })


def product_categories_components(request):
    product_categories = ProductCategory.objects.filter(is_active=True, is_delete=False)
    context = {
        'categories': product_categories
    }
    return render(request, 'product_module/component/product_categories_component.html', context)


def product_brands_components(request):
    product_brands = ProductBrand.objects.annotate(product_count=Count('product')).filter(is_active=True)
    context = {
        'brands': product_brands
    }
    return render(request, 'product_module/component/product_brands_component.html', context)


def add_product_comment(request: HttpRequest):
    if request.user.is_authenticated:
        product_id = request.GET.get('product_id')
        suggested = request.GET.get('is_suggested')
        if suggested == 'false':
            is_suggested = False
        elif suggested == 'true':
            is_suggested = True
        else:
            return HttpResponse(f'err{suggested}')

        product_comment = request.GET.get('product_comment')
        if len(product_comment) < 10:
            return HttpResponse('err minlength')
        new_comment = ProductComment(product_id=product_id, text=product_comment, user_id=request.user.id,
                                         is_suggested=is_suggested)
        new_comment.save()

        context = {
            'comments': ProductComment.objects.filter(product_id=product_id).order_by('-create_date'),
            'comments_count': ProductComment.objects.filter(product_id=product_id).count()
        }
        return render(request, 'product_module/includes/product_comment_partial.html', context)

    return HttpResponse('response')
