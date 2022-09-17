from django.urls import path 
from . import views

app_name = 'coupons'
urlpatterns = [
    path('apply/', views.coupon_apply_view, name='apply'), 
    path('', views.coupon_delete_view, name='delete'), 
]
