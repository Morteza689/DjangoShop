import random
from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse, HttpRequest, JsonResponse, Http404
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from site_module.models import SiteSetting
from utils.sms_service import SMS
from .forms import *
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView
from account_module.models import User, UserAddress
from django.contrib.auth import logout
from order_module.models import Order, OrderDetaile


@method_decorator(login_required, 'dispatch')
class UserPanelDashbordView(TemplateView):
    template_name = 'user_panel_module/user_panel_dashbord_page.html'

    def get_context_data(self, **kwargs):
        request: HttpRequest = self.request
        context = super(UserPanelDashbordView, self).get_context_data()
        context['user'] = User.objects.filter(id=request.user.id).first()
        context['latest_order'] = Order.objects.filter(user_id=request.user.id, is_paid=True).order_by('-id')[:5]
        return context


@method_decorator(login_required, 'dispatch')
class EditUserProfileView(View):
    def get(self, request):
        current_user = User.objects.filter(id=request.user.id).first()
        edit_form = EditUserProfileModelForm(instance=current_user)
        context = {
            'form': edit_form,
            'current_user': current_user
        }
        return render(request, 'user_panel_module/user_edit_profile_page.html', context)

    def post(self, request: HttpRequest):
        current_user = User.objects.filter(id=request.user.id).first()
        edit_form = EditUserProfileModelForm(request.POST, request.FILES, instance=current_user)
        if edit_form.is_valid():
            edit_form.save()

        context = {
            'form': edit_form,
            'current_user': current_user
        }
        return render(request, 'user_panel_module/user_edit_profile_page.html', context)


@method_decorator(login_required, 'dispatch')
class ChangePasswordView(View):
    def get(self, request: HttpRequest):
        form = ChangePasswordForm()
        context = {
            'form': form
        }
        return render(request, 'user_panel_module/change_password_page.html', context)

    def post(self, request: HttpRequest):
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            current_user: User = User.objects.filter(id=request.user.id).first()
            if current_user.check_password(form.cleaned_data.get('current_password')):
                current_user.set_password(form.cleaned_data.get('password'))
                current_user.save()
                logout(request)
                return redirect(reverse('logout_page'))
            else:
                form.add_error('password', 'کلمه عبور اشتباه میباشد')

        context = {
            'form': form
        }
        return render(request, 'user_panel_module/change_password_page.html', context)


@method_decorator(login_required, 'dispatch')
class EditAddressView(View):
    def get(self, request):
        current_user = User.objects.filter(id=request.user.id).first()
        address = UserAddress.objects.filter(user_id=current_user.id)
        edit_form = EditUserAddressForm()
        context = {
            'address': address,
            'form': edit_form,
        }
        return render(request, 'user_panel_module/user_edit_address_page.html', context)

    def post(self, request: HttpRequest):
        current_user = User.objects.filter(id=request.user.id).first()
        address = UserAddress.objects.filter(user_id=current_user.id)
        edit_form = EditUserAddressForm(request.POST)
        if edit_form.is_valid():
            addres = edit_form.cleaned_data.get('address')
            zipcode = edit_form.cleaned_data.get('zipcode')
            receiver = edit_form.cleaned_data.get('receiver')
            number_receiver = edit_form.cleaned_data.get('number_receiver')
            if number_receiver < 9000000000:
                edit_form.add_error('number_receiver', 'شماره خود را کامل وارد کنید نمونه : 09102003040')
            elif number_receiver > 9999999999:
                edit_form.add_error('number_receiver', 'شماره خود را درست وارد کنید نمونه : 09102003040')
            else:
                new_address = UserAddress(user_id=current_user.id, receiver=receiver
                                          , number_receiver=number_receiver,
                                          address=addres, zipcode=zipcode)
                new_address.save()
                return redirect(reverse('user_edit_address'))

        context = {
            'address': address,
            'form': edit_form,
        }
        return render(request, 'user_panel_module/user_edit_address_page.html', context)


def delete_address(request: HttpRequest, id):
    address = UserAddress.objects.filter(user_id=request.user.id, id=id).first()
    if address is not None:
        print(address.id)
        address.delete()
        return redirect(reverse('user_edit_address'))
    else:
        raise Http404


@method_decorator(login_required, 'dispatch')
class MyShopingView(ListView):
    model = Order
    template_name = 'user_panel_module/user-shoping.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        request: HttpRequest = self.request
        queryset = queryset.filter(user_id=request.user.id, is_paid=True)
        return queryset


@login_required
def user_panel_menu_component(request):
    return render(request, 'user_panel_module/components/user_panel_menu_component.html', {
        'user': User.objects.filter(id=request.user.id).first()
    })


@login_required
def user_order(request: HttpRequest):
    current_order, created = Order.objects.prefetch_related('orderdetaile_set').get_or_create(is_paid=False,
                                                                                              user_id=request.user.id)
    total_amount = current_order.calculate_total_price()

    context = {
        'user': User.objects.filter(id=request.user.id),
        'order': current_order,
        'sum': total_amount
    }
    return render(request, 'user_panel_module/user_order.html', context)


@login_required
def order_shipping_payment(request: HttpRequest):
    current_order, created = Order.objects.prefetch_related('orderdetaile_set').get_or_create(is_paid=False,
                                                                                              user_id=request.user.id)
    total_amount = current_order.calculate_total_price()
    user: User = User.objects.prefetch_related('useraddress_set').filter(id=request.user.id).first()

    context = {
        'user': user,
        'order': current_order,
        'sum': total_amount
    }
    return render(request, 'user_panel_module/order_shipping_payment.html', context)


@login_required
def remove_order_detail(request: HttpRequest):
    detail_id = request.GET.get('detail_id')
    if detail_id is None:
        return JsonResponse({
            'status': 'not_found_detail_id'
        })

    deleted_count, deleted_dict = OrderDetaile.objects.filter(id=detail_id, order__is_paid=False,
                                                              order__user_id=request.user.id).delete()

    if deleted_count == 0:
        return JsonResponse({
            'status': 'detail_not_found'
        })

    current_order, created = Order.objects.prefetch_related('orderdetaile_set').get_or_create(is_paid=False,
                                                                                              user_id=request.user.id)
    total_amount = current_order.calculate_total_price()
    context = {
        'order': current_order,
        'sum': total_amount
    }

    return JsonResponse({
        'status': 'success',
        'body': render_to_string('user_panel_module/user_order_content.html', context)
    })


@login_required
def get_address_id(request: HttpRequest):
    address_id = request.GET.get('address_id')
    user = User.objects.filter(id=request.user.id).first()
    address = UserAddress.objects.filter(user_id=user.id, id=address_id).first()
    if address is not None:
        current_order, created = Order.objects.prefetch_related('orderdetaile_set').get_or_create(is_paid=False,
                                                                                                  user_id=request.user.id)
        current_order.address_id = address_id
        current_order.save()
        return HttpResponse('اضافه شد')
    return HttpResponse('err')


@login_required
def change_order_detail_count(request: HttpRequest):
    detail_id = request.GET.get('detail_id')
    state = request.GET.get('state')
    if detail_id is None or state is None:
        return JsonResponse({
            'status': 'not_found_detail_or_state'
        })

    order_detail = OrderDetaile.objects.filter(id=detail_id, order__user_id=request.user.id,
                                               order__is_paid=False).first()
    if order_detail is None:
        return JsonResponse({
            'status': 'detail_not_found'
        })

    if state == 'increase':
        order_detail.count += 1
        order_detail.save()
    elif state == 'decrease':
        if order_detail.count == 1:
            order_detail.delete()
        else:
            order_detail.count -= 1
            order_detail.save()
    else:
        return JsonResponse({
            'status': 'state_invalid'
        })

    current_order, created = Order.objects.prefetch_related('orderdetaile_set').get_or_create(is_paid=False,
                                                                                              user_id=request.user.id)
    total_amount = current_order.calculate_total_price()
    context = {
        'order': current_order,
        'sum': total_amount
    }
    return JsonResponse({
        'status': 'success',
        'body': render_to_string('user_panel_module/user_order_content.html', context)
    })


def my_shoping_detail(request: HttpRequest, order_id):
    order = Order.objects.filter(id=order_id, user_id=request.user.id).prefetch_related('orderdetaile_set').first()
    if order is None:
        raise Http404('سبد خرید مورد نظر یافت نشد')
    return render(request, 'user_panel_module/user-shoping_detail.html', {
        'order': order
    })


@method_decorator(login_required, 'dispatch')
class AddNumberView(View):
    def get(self, request):
        current_user = User.objects.filter(id=request.user.id).first()
        if current_user.number_is_active:
            return redirect(reverse('user_panel_dashbord'))
        number_form = AddNumberForm()
        context = {
            'form': number_form,
            'current_user': current_user
        }
        return render(request, 'user_panel_module/add_number_page.html', context)

    def post(self, request: HttpRequest):
        current_user = User.objects.filter(id=request.user.id).first()
        if current_user.number_is_active:
            return redirect(reverse('user_panel_dashbord'))
        number_form = AddNumberForm(request.POST)
        if number_form.is_valid():
            number = number_form.cleaned_data.get('number')
            number_user = User.objects.filter(number__exact=number).exists()
            if number_user:
                number_form.add_error('number', 'این شماره قبلا در سیستم ثبت شده است')
            elif number < 9000000000:
                number_form.add_error('number', 'شماره خود را کامل وارد کنید نمونه : 09102003040')
            elif number > 9999999999:
                number_form.add_error('number', 'شماره خود را درست وارد کنید نمونه : 09102003040')
            else:

                return redirect(reverse('active_number_page', args=[number]))

        context = {
            'form': number_form,
            'current_user': current_user
        }
        return render(request, 'user_panel_module/add_number_page.html', context)


@method_decorator(login_required, 'dispatch')
class ActiveNumberView(View):
    def get(self, request: HttpRequest, number):
        current_user = User.objects.filter(id=request.user.id).first()
        current_user.number_active_code = random.randrange(10000, 99999)
        current_user.save()
        setting: SiteSetting = SiteSetting.objects.filter(is_main_setting=True).first()
        SMS(f'''{setting.site_name}
                                    کد فعال سازی شما : {current_user.number_active_code}

                                    اینستاگرام ما:
                                    {setting.instagram_url}
                                    سایت ما:
                                    {setting.site_url}
                                    ''', number)

        if current_user.number_is_active:
            return redirect(reverse('user_panel_dashbord'))
        active_form = ActiveNummerForm()
        context = {
            'form': active_form,
            'current_user': current_user
        }
        return render(request, 'user_panel_module/active_number_page.html', context)

    def post(self, request: HttpRequest, number):
        current_user = User.objects.filter(id=request.user.id).first()
        if current_user.number_is_active:
            return redirect(reverse('user_panel_dashbord'))
        active_form = ActiveNummerForm(request.POST)
        if active_form.is_valid():
            number_active_code = active_form.cleaned_data.get('number_active_code')
            if current_user.number_active_code == number_active_code:
                current_user.number_is_active = True
                current_user.number = number
                current_user.save()
                return redirect(reverse('user_panel_dashbord'))
            else:
                active_form.add_error('number_active_code', 'کد نادرست است')

        context = {
            'form': active_form,
            'current_user': current_user
        }
        return render(request, 'user_panel_module/active_number_page.html', context)


@method_decorator(user_passes_test(lambda u: u.is_superuser), 'dispatch')
class AdminShopingListView(ListView):
    model = Order
    template_name = 'user_panel_module/shoping_admin.html'
    context_object_name = 'order'

    def get_queryset(self):
        queryset = super(AdminShopingListView, self).get_queryset()
        queryset = queryset.filter(is_paid=True)
        return queryset


@method_decorator(user_passes_test(lambda u: u.is_superuser), 'dispatch')
class AdminShopingDetailView(View):
    def get(self, request: HttpRequest, order_id):
        order_edit = Order.objects.filter(id=order_id).first()
        form = EditUserOrderModelForm(instance=order_edit)
        context = {
            'form': form,
            'order': order_edit
        }
        return render(request, 'user_panel_module/shoping_detail_admin.html', context)

    def post(self, request: HttpRequest,order_id):
        order_edit = Order.objects.filter(id=order_id).first()
        form = EditUserOrderModelForm(request.POST,instance=order_edit)
        if form.is_valid():
            form.save()
            return redirect(reverse('user_shoping_admin_page'))
        context = {
            'form': form,
            'order': order_edit
        }
        return render(request, 'user_panel_module/shoping_detail_admin.html', context)
