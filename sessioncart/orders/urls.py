from django.urls import path

from . import views

app_name = 'orders'
urlpatterns = [
    path('create/', views.order_create_view, name='order_create'), 
    path('admin/order/<int:order_id>/', views.admin_order_detail, name='admin_order_detail'), 
]
