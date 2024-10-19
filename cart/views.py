from django.shortcuts import render
from .cart import Cart
from store.models import Product
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

# Create your views here.

def cart_summary(request):
    cart = Cart(request)
    return render(request, 'cart/cart_summary.html', {'cart': cart})

def add_to_cart(request):
    cart = Cart(request)
    if request.POST.get('action') == 'POST':

        product_id = int(request.POST.get('product_id'))
        product_quantity = int(request.POST.get('product_quantity'))

        product = get_object_or_404(Product, id=product_id)

        cart.add(product=product, product_qty=product_quantity)

        cart_quantity = cart.__len__()

        response = JsonResponse({'qty': cart_quantity })
        return response



def delete_cart(request):
    cart = Cart(request)
    if request.POST.get('action') == 'POST':

        product_id = int(request.POST.get('product_id'))

        product = get_object_or_404(Product, id=product_id)

        cart.delete(product=product_id)

        cart_quantity = cart.__len__()

        cart_total = cart.total_price()

        response = JsonResponse({'qty': cart_quantity, 'total': cart_total})

        return response

def update_cart(request):
    cart = Cart(request)
    if request.POST.get('action') == 'POST':

        product_id = int(request.POST.get('product_id'))
        product_quantity = int(request.POST.get('product_quantity'))


        cart.update(product=product_id, qty=product_quantity)

        cart_quantity = cart.__len__()

        cart_total = cart.total_price()

        response = JsonResponse({'qty': cart_quantity, 'total': cart_total})

        return response
