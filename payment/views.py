from django.shortcuts import render
from .models import ShippingAddress, Order, OrderItem
from cart.cart import Cart
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
import datetime


# Create your views here.

def checkout(request):

   # User with accounts prefilled form
   if request.user.is_authenticated:

    try:
       
       # Authenticated users with shipping address
        shipping_address = ShippingAddress.objects.get(user=request.user.id)

        context = {'shipping_address': shipping_address}

        return render(request, 'payment/checkout.html', context)

    except:
       
       # Authenticated with no shipping information
       return render(request, 'payment/checkout.html')
    
   else:
       
          return render(request, 'payment/checkout.html')
   
def complete_order(request):
    if request.POST.get('action') == 'post':
           
        name = request.POST.get('name')
        email = request.POST.get('email')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zipcode = request.POST.get('zipcode')
        shipping_address = (address1 + "\n" + address2 + 
                            
          "\n"  + city + "\n" + state + "\n" + zipcode                
        )
       
        # Shopping cart information
        cart = Cart(request)

        #Get the total price of items
        total = cart.total_price()

        # Create order for users with and without shipping information
        if request.user.is_authenticated:

            order = Order.objects.create(full_name=name, email=email, shipping_address=shipping_address, total=total, user=request.user)

            order_id = order.pk

            for item in cart:
                OrderItem.objects.create(order_id=order_id, product=item['product'], quantity=item['qty'], 
                price=item['price'], user=request.user)

        mail_subject = 'Thank you for your order'
        message = render_to_string('payment/payment_complete.html', {
 
       'user': request.user,
       'order': order
       
        

    })

        to_email = request.user.email
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send()   
       

        # Create order for guest users without account
    else:

            order = Order.objects.create(full_name=name, email=email, total=total, shipping_address=shipping_address)

            order_id = order.pk

            
           
            for item in cart:
                OrderItem.objects.create(order_id=order_id, product=item['product'], quantity=item['quantity'],
                price=item['price'])

           

       
    mail_subject = 'Thank you for your order'
    message = render_to_string('payment/payment_complete.html', {

       'user': request.user,
       'order': order
       
        

    })

    to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()
          
            
    order_success = True
    response = JsonResponse({'success': order_success })
    return response
    

def payment_success(request):

    # Clear shopping cart
    for key in list(request.session.keys()):

        if key == 'session_key':
            del request.session[key]

    return render(request, 'payment/payment_success.html')

def payment_failed(request):
    return render(request, 'payment/payment_failed.html')
