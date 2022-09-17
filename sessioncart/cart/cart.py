from decimal import Decimal
from django.conf import settings

from shop.models import Product
from coupons.models import Coupon

import ipdb

class Cart:

    def __init__(self, request):
        '''
            Инициализация корзины.
            request - объкт запроса пользователя типа HttpRequest.
        '''
        self.session_id = settings.CART_SESSION_ID
        self.session = request.session
        cart = self.session.get(self.session_id)
        if not cart:
            '''
                Если нет корзины пользователя в сессии, то создаём сессию с пустой корзиной
            '''
            cart = self.session[self.session_id] = {}
        self.cart = cart
        self.coupon_id = self.session.get('coupon_id')  # сохранение текущего примененного купона

    def _add_new_product_to_cart(self, prod_id, price):
        self.cart[prod_id] = {'quantity': 0, 'price': str(price)}

    def _update_product_quantity(self, product_id, quantity):
        self.cart[prod_id]['quantity'] = quantity

    def add(self, product, quantity=1, update_quantity=False):
        ''' 
            Метод добавления продукта в корзину. 
            Если update_quantity=True, то обновляем количество имеющегося товара.
        '''
        prod_id = str(product.id)
        if prod_id not in self.cart:
            self._add_new_product_to_cart(prod_id, product.price)

        if update_quantity:
            self._update_product_quantity(prod_id, quantity)
        else:
            self.cart[prod_id]['quantity'] += quantity
        self.save()

    def remove(self, product):
        ''' 
            Метод удаления продукта из корзины. 
        '''
        prod_id = str(product.id)
        if prod_id in self.cart:
            del self.cart[prod_id]
            self.save()

    def get_total_price(self):
        '''
            Подсчет стоимости товаров в корзине.
        '''
        return sum(
                Decimal(item['price']) * item['quantity'] 
                for item in self.cart.values())

    @property
    def coupon(self):
        if self.coupon_id:
            return Coupon.objects.get(id=self.coupon_id)
        return None

    def get_discount(self):
        if self.coupon:
            return (self.coupon.discount / Decimal('100')) * self.get_total_price()
        return Decimal('0')

    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()
    
    def save(self):
        '''
            Метод обновления сессии cart
        '''
        self.session[self.session_id] = self.cart
        self.session.modified = True
 
    def clear(self):
        '''
            Удаление корзины пользователя из сессии
        '''
        del self.session[self.session_id]
        self.session.modified = True

    def __iter__(self):
        '''
            Перебор элементов в корзине и получение продуктов из базы данных.
            проходим по элементам корзины, преобразуя цену 
            номенклатуры обратно в десятичное число и добавляя атрибут total_price к каждому элементу. 
            Теперь можно легко выполнить итерацию по товарам в корзине.
        '''
        prod_ids = self.cart.keys()
        # получение объектов product и добавление их в корзину
        prods = Product.objects.filter(id__in=prod_ids)
        for prod in prods:
            self.cart[str(prod.id)]['product'] = prod
        
        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item
     
    def __len__(self):
        '''
            Подсчет всех товаров в корзине.
        '''
        return sum(item['quantity'] for item in self.cart.values())

