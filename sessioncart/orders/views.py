from django.shortcuts import render

from .models import OrderItem
from .forms import OrderCreateForm
from .tasks import order_created_task

from cart.cart import Cart
import ipdb

def order_create_view(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST or None)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # очистка корзины
            cart.clear()
            '''
                запуск асинхронной задачи в Celery tasks
                Мы называем метод delay() задачи, чтобы выполнить ее асинхронно. 
                Задача будет добавлена в очередь celery и будет выполнена как можно скорее.
            '''
            order_created_task.delay(order.id)
            return render(request, 
                    'orders/order/created.html', 
                    {'order': order})
    else:
        form = OrderCreateForm()
        data = {'cart': cart, 'form': form}
        return render(request, 'orders/order/create.html', data)


