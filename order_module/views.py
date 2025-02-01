from datetime import time
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse ,HttpResponse
from django.shortcuts import redirect, render
import requests
import json
from django.urls import reverse
from .models import *
from datetime import datetime

#cofig zarinpal
MERCHANT = '********************************************'
ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"
amount = 0  # Rial / Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
email = ''  # Optional
mobile = ''  # Optional
# Important: need to edit for realy server.
CallbackURL = 'https://127.0.0.1:8000/order/verify-payment/'
#cofig zarinpal------------------------------------------


def add_product_to_order(request:HttpRequest):
    product_id=int(request.GET.get('product_id'))
    count=int(request.GET.get('count'))
    if count < 1:
        return JsonResponse({
            'status':'invalid_count',
            'text':'مقدار وارد شده معتبر نمیباشد',
            'confirm_button_text':'باشه',
            'icon':'error'
    })

    if request.user.is_authenticated:
        product=Product.objects.filter(id=product_id,is_active=True,is_delete=False).first()
        if product is not None:
            current_order, created=Order.objects.get_or_create(is_paid=False,user_id=request.user.id)
            current_order_detail=current_order.orderdetaile_set.filter(product_id=product_id).first()
            if current_order_detail is not None:
                current_order_detail.count+=int(count)
                current_order_detail.save()
            else:
                new_detail=OrderDetaile(order_id=current_order.id,product_id=product_id,count=count)
                new_detail.save()

            return JsonResponse({
                    'status': '200',
                    'text': 'با موفقیت به سبد خرید شما اضافه شد',
                    'confirm_button_text': 'ممنون',
                    'icon': 'success'
                })
        else:
            return JsonResponse({
                'status': 'not_found',
                'text': 'محصول یافت نشد',
                'confirm_button_text': 'باشه',
                'icon': 'error'
            })
    return JsonResponse({
        'status':'not_auth',
        'text': 'ابتدا باید وارد سایت شوید',
        'confirm_button_text': 'ورود',
        'icon': 'warning'
    })


@login_required
def request_payment(request:HttpRequest):
    current_user = User.objects.filter(id=request.user.id).first()
    if not current_user.number_is_active:
        return JsonResponse({'error':'your number is not active. pleas active your number'})
    current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
    total_price=current_order.calculate_total_price()
    if total_price==0:
        return redirect(reverse('user_order_page'))


    req_data = {
        "merchant_id": MERCHANT,
        "amount": total_price*10,
        "callback_url": CallbackURL,
        "description": description,
        "metadata": {"email": request.user.email}
    }
    req_header = {"accept": "application/json","content-type": "application/json'"}
    req = requests.post(url=ZP_API_REQUEST, data=json.dumps(
        req_data), headers=req_header)
    authority = req.json()['data']['authority']
    if len(req.json()['errors']) == 0:
        return redirect(ZP_API_STARTPAY.format(authority=authority))
    else:
        e_code = req.json()['errors']['code']
        e_message = req.json()['errors']['message']
        return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")


@login_required
def verify_payment(request:HttpRequest):
    t_authority = request.GET['Authority']
    if request.GET.get('Status') == 'OK':

        current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
        total_price = current_order.calculate_total_price()

        req_header = {"accept": "application/json","content-type": "application/json'"}
        req_data = {
            "merchant_id": MERCHANT,
            "amount": total_price*10,
            "authority": t_authority
        }
        req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
        if len(req.json()['errors']) == 0:
            t_status = req.json()['data']['code']
            if t_status == 100:
                current_order.is_paid=True
                for i in current_order.orderdetaile_set.all():
                    if i.product.off:
                        i.final_price=i.product.offer_price
                        i.save()
                    else:
                        i.final_price = i.product.price
                        i.save()
                        
                current_order.paymant_date=datetime.now()
                current_order.save()
                ref_code=req.json()['data']['ref_id']
                return render(request,'order_module/payment_result.html',{
                    'success':200,
                    'ref_code':ref_code
                              })
            elif t_status == 101:
                return render(request, 'order_module/payment_result.html', {
                    'info': 'این تراکنش تکراری میباشد'
                })
            else:
                return render(request, 'order_module/payment_result.html', {
                    'error': str(req.json()['data']['message'])
                    })
        else:
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            return render(request, 'order_module/payment_result.html', {
                'error': f"Error code: {e_code}, Error Message: {e_message}"
            })
    else:
        return render(request, 'order_module/payment_result.html', {
            'error': 'تراکنش ناموفق/ممکن است توسط کاربر لغو شده است'
        })

