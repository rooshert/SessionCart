from django.db import models

from shop.models import Product


class Order(models.Model):
    '''
        Модель общего заказа.
        В один Order может входить несколько OrderItem (подзаказов)
    '''
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        '''
            Метод считает стоимость всех OrderItem, входящих в Order
        '''
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    '''
        Модель части заказа. Включает в себя выбранный конкретный продукт + его количество
    '''
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        '''
            Возвращает цену OrderItem (цена + количество)
        ''' 
        return self.price * self.quantity



