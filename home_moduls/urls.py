from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView.as_view() , name='home_page'),
    path('abuot-us', AbuotView.as_view() , name='abuot_page'),
    ]