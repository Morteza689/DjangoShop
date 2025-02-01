from django.shortcuts import render, redirect
from django.views import View
from site_module.models import SiteSetting, FooterLinkBox
from .models import User
from .forms import RegisterForm, ResetPasswordForm
from .forms import LoginForm, ForgetPasswordForm
from django.utils.crypto import get_random_string
from django.urls import reverse
from django.http import Http404, HttpRequest
from django.contrib.auth import login, logout
from utils.email_service import send_email
import random


# Create your views here.


class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('home_page'))
        register_form = RegisterForm()
        context = {
            'register_form': register_form,
            'site_setting': SiteSetting.objects.filter(is_main_setting=True).first()
        }
        return render(request, 'account_module/register.html', context=context)

    def post(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('home_page'))
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_email = register_form.cleaned_data.get('email')
            user_password = register_form.cleaned_data.get('password')
            user: bool = User.objects.filter(email__iexact=user_email).exists()
            if user:
                register_form.add_error('email', 'کاربری با این ایمیل ثبت نام کرده')
            else:
                new_user = User(email=user_email,
                                email_active_code=get_random_string(72),
                                is_active=False,
                                username=user_email,
                                number_active_code=random.randrange(10000, 99999))
                new_user.set_password(user_password)
                new_user.save()
                send_email('فعال سازی حساب کاربری', new_user.email, {'user': new_user}, 'emails/active_account.html')
                context={
                    'user': new_user,
                    'site_setting': SiteSetting.objects.filter(is_main_setting=True).first()
                }
                return render(request,'account_module/email_sended.html',context)

        context = {
            'register_form': register_form,
            'site_setting': SiteSetting.objects.filter(is_main_setting=True).first()
        }
        return render(request, 'account_module/register.html', context)


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('home_page'))
        login_form = LoginForm()
        context = {
            'login_form': login_form,
            'site_setting': SiteSetting.objects.filter(is_main_setting=True).first()
        }
        return render(request, 'account_module/login.html', context=context)

    def post(self, request):
        login_form = LoginForm(request.POST)
        if request.user.is_authenticated:
            return redirect(reverse('home_page'))
        if login_form.is_valid():
            user_email = login_form.cleaned_data.get('email')
            user_pass = login_form.cleaned_data.get('password')
            user: User = User.objects.filter(email__iexact=user_email).first()
            if user is not None:
                if not user.is_active:
                    login_form.add_error('email', 'اکانت فعال نیست')
                else:
                    is_password_correct = user.check_password(user_pass)
                    if is_password_correct:
                        login(request, user)
                        if user.number_is_active:
                            return redirect(reverse('user_panel_dashbord'))
                        else:
                            return redirect(reverse('add_number_page'))
                    else:
                        login_form.add_error('email', 'کلمه عبور اشتباه')
            else:
                login_form.add_error('email', 'کاربر وجود ندارد')
        context = {
            'login_form': login_form,
            'site_setting': SiteSetting.objects.filter(is_main_setting=True).first()
        }

        return render(request, 'account_module/login.html', context=context)


class ForgetPasswordView(View):

    def get(self, request: HttpRequest):
        forget_password_form = ForgetPasswordForm()
        context = {
            'forget_password_form': forget_password_form,
            'site_setting': SiteSetting.objects.filter(is_main_setting=True).first()
        }

        return render(request, 'account_module/forget_password.html', context=context)

    def post(self, request: HttpRequest):
        forget_password_form = ForgetPasswordForm(request.POST)
        if forget_password_form.is_valid():
            user_email = forget_password_form.cleaned_data.get('email')
            user = User.objects.filter(email__iexact=user_email).first()
            if user is not None:
                send_email('بازیابی حساب کاربری', user.email, {'user': user}, 'emails/forget_password.html')
                return redirect(reverse('login_page'))

            else:
                return redirect(reverse('login_page'))

        context = {
            'forget_password_form': forget_password_form,
            'site_setting': SiteSetting.objects.filter(is_main_setting=True).first()
        }

        return render(request, 'account_module/forget_password.html', context=context)


class ResetPasswordView(View):
    def get(self, request, active_code):
        user: User = User.objects.filter(email_active_code__iexact=active_code).first()
        if user is None:
            return redirect(reverse('login_page'))
        else:
            reset_password_form = ResetPasswordForm()
            context = {
                'reset_password_form': reset_password_form,
                'user': user,
                'site_setting': SiteSetting.objects.filter(is_main_setting=True).first()
            }
            return render(request, 'account_module/reset_password.html', context=context)

    def post(self, request, active_code):
        reset_password_form = ResetPasswordForm(request.POST)
        user: User = User.objects.filter(email_active_code__iexact=active_code).first()
        if reset_password_form.is_valid():

            if user is None:
                return redirect(reverse('login_page'))
            user_pass = reset_password_form.cleaned_data.get('password')
            user.set_password(user_pass)
            user.email_active_code = get_random_string(72),
            user.is_active = True
            user.save()
            return redirect(reverse('login_page'))

        context = {
            'reset_password_form': reset_password_form,
            'user': user,
            'site_setting': SiteSetting.objects.filter(is_main_setting=True).first()

        }
        return render(request, 'account_module/reset_password.html', context=context)


class ActivateAccountView(View):
    def get(self, request, email_active_code):
        user: User = User.objects.filter(email_active_code__iexact=email_active_code).first()
        if user is not None:
            if not user.is_active:
                user.is_active = True
                user.email_active_code = get_random_string(72)
                user.save()
                context={
                    'user':user,
                    'site_setting':SiteSetting.objects.filter(is_main_setting=True).first()
                }
                return render(request,'account_module/activeated_account.html',context)
            else:
                pass
        raise Http404

    def post(self, request):
        pass


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('login_page'))


def site_footer_component(requests):
    setting: SiteSetting = SiteSetting.objects.filter(is_main_setting=True).first()
    footer_link_boxs = FooterLinkBox.objects.all()
    context = {
        'footer_link_boxs': footer_link_boxs,
        'site_setting': setting
    }
    return render(requests, 'account_module/shared/site_footer_component.html', context)
