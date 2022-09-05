from django.shortcuts import render

from .models import OrderItem
from .forms import OrderCreateForm

from cart.cart import Cart
import ipdb

def order_create_view(request):
    ipdb.set_trace()
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST or None)
        if form.is_valid():
            order = form.save()
            for item in cart:
                ipdb.set_trace()
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()
            return render(request, 
                    'orders/order/created.html', 
                    {'order': order})
    else:
        form = OrderCreateForm()
        data = {'cart': cart, 'form': form}
        return render(request, 'orders/order/create.html', data)


