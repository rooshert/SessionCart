from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from shop.models import Product
from coupons.forms import CouponApplyForm

from .cart import Cart
from .forms import AddProduct2CartForm

import ipdb

@require_POST
def add2cart_view(request, product_id):
    '''
        Это представление для добавления продуктов в корзину или 
        обновления количества для существующих продуктов.
        
        Мы используем декоратор require_POST, чтобы разрешить 
        только POST запросы, поскольку это представление изменит данные.

        
    '''
    cart = Cart(request)  # Получаем объект корзины пользователя
    prod = get_object_or_404(Product, id=product_id)
    form = AddProduct2CartForm(request.POST or None)
    if form.is_valid():
        form_data = form.cleaned_data
        cart.add(
            product=prod,
            quantity=form_data['quantity'],
            update_quantity=form_data['update']
        )
    return redirect('cart:cart_detail')


def remove_from_cart_view(request, product_id):
    '''
        Представление cart_remove получает id продукта в качестве параметра. 
        Мы извлекаем экземпляр продукта с заданным id и удаляем продукт из корзины. 
        Затем мы перенаправляем пользователя на URL-адрес cart_detail.
    '''
    cart = Cart(request)
    prod = get_object_or_404(Product, id=product_id)
    cart.remove(prod)
    return redirect('cart:cart_detail')


def cart_detail(request):
    '''
        Представление cart_detail выводит на экран текущее состояние корзины.
    '''
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = AddProduct2CartForm(
            initial={'quantity': item['quantity'], 'update': True})

    coupon_apply_form = CouponApplyForm()
    data = {
            'cart': cart, 
            'coupon_apply_form': coupon_apply_form
        }
    return render(request, 'cart/detail.html', data)

