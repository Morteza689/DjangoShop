from django.urls import path
from  . import views

urlpatterns=[
    path('',views.UserPanelDashbordView.as_view(),name='user_panel_dashbord'),
    path('change-pass/',views.ChangePasswordView.as_view(),name='change_password_profile'),
    path('edit-profile/',views.EditUserProfileView.as_view(),name='user_edit_profile'),
    path('add-number/',views.AddNumberView.as_view(),name='add_number_page'),
    path('active-number/<number>',views.ActiveNumberView.as_view(),name='active_number_page'),
    path('edit-address/',views.EditAddressView.as_view(),name='user_edit_address'),
    path('delete-address/<id>/',views.delete_address,name='user_delete_address'),
    path('order/',views.user_order,name='user_order_page'),
    path('order/shipping-payment/',views.order_shipping_payment,name='order_shipping_payment'),
    path('my-shopings/',views.MyShopingView.as_view(),name='user_shoping_page'),
    path('my-shoping-detail/<order_id>/',views.my_shoping_detail,name='user_shoping_detail_page'),
    path('remove-order-detail/',views.remove_order_detail,name='remove_order_detail_ajax'),
    path('change-order-detail/',views.change_order_detail_count,name='change_order_detail_count_ajax'),
    path('get-address-id/',views.get_address_id,name='get_address_id'),
    path('shopings-admin/',views.AdminShopingListView.as_view(),name='user_shoping_admin_page'),
    path('shoping-detail-admin/<order_id>/', views.AdminShopingDetailView.as_view(), name='user_shoping_detail_admin_page'),
]

