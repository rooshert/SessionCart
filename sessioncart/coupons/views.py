from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.utils import timezone

from .forms import CouponApplyForm
from .models import Coupon

from cart import cart

import ipdb

@require_POST
def coupon_apply_view(request):
    '''
        Функция получения купона пользователя
        Купон можно получить если:
            1. код передаваемого в форме купона совпадает с кодом купона из БД;
            2. соблюдается временная валидность купона (нынешняя дата находится
                между valid_from и valid_to);
            3. купон активен (active=True);
    '''
    now = timezone.now()
    form = CouponApplyForm(request.POST or None)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            # Берём купон из БД
            c = Coupon.objects.get(
                    code__iexact=code, 
                    valid_from__lte=now,
                    valid_to__gte=now,
                    active=True)
            # Закрепляем купон за пользователем (в сессии и БД)
            request.session['coupon_id'] = c.id
        except Coupon.DoesNotExists:
            request.session['coupon_id'] = None

    return redirect('cart:cart_detail')


@require_POST
def coupon_delete_view(request):
    '''
        Удаление купона из сессии
    '''
    form = CouponApplyForm(request.POST or None)
    if form.is_valid():
        code = form.cleaned_data['code']
        # ...code processing
        del request.session['coupon_id']
    
    return redirect('cart:cart_detail')

