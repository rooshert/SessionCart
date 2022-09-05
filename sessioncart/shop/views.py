from django.shortcuts import render
from django.shortcuts import render, get_object_or_404

from cart.forms import AddProduct2CartForm

from .models import Product, Category

def product_detail(request, id, product_slug):
    product = get_object_or_404(
        Product,
        id=id,
        slug=product_slug,
        available=True
    )
    data = {
        'product': product, 
        'cart_product_form': AddProduct2CartForm()
    }
    return render(request, 'shop/products/detail.html', data)


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    data = {'category': category or None, 
            'categories': categories, 
            'products': products
        }
    return render(request, 'shop/products/list.html', data)

