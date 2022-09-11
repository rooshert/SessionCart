'''
    Модуль асинхронный задач для выполнения celery.
    Celery автоматически будет искать асинхронные задаи в модуле tasks.py приложения

    Асинхронные задачи используются не только для процессов, требующих 
    длительного времени выполнения, но и для других процессов, подверженных сбою, которые 
    не занимают много времени для выполнения, но могут быть связаны с ошибками 
    подключения или требуют политики повторных попыток.
'''
from celery import shared_task
from sessioncart.celery import app

from django.core.mail import send_mail
from .models import Order

@shared_task
def order_created_task(order_id):
    '''
        Task для отправки уведомления по электронной почте при успешном создании заказа. 
    '''
    order = Order.objects.get(id=order_id)
    subject = 'Order nr. {}'.format(order_id)
    message = 'Dear {},\n\nYou have successfully placed an order.\
                Your order id is {}.'.format(order.first_name, order.id)
    ms = send_mail(subject, message, 'admin@myshop.com', [order.email], fail_silently=False)
    return ms

