from django.urls import path
from .views import RegisterView,LoginView,ActivateAccountView,ForgetPasswordView ,ResetPasswordView ,LogoutView

urlpatterns = [
    path('register/',RegisterView.as_view(),name='register_page'),
    path('login/',LoginView.as_view(),name='login_page'),
    path('logout/',LogoutView.as_view(),name='logout_page'),
    path('forget-password/',ForgetPasswordView.as_view(),name='forget_password_page'),
    path('activate-account/<email_active_code>',ActivateAccountView.as_view(),name='activate_account'),
    path('forget-password/<active_code>',ResetPasswordView.as_view(),name='reset_password_page'),
]


