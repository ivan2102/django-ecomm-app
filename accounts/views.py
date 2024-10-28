from django.shortcuts import redirect, render
from . forms import LoginForm, UserForm, UpdateUserForm
from payment.forms import ShippingForm
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib.sites.shortcuts import get_current_site
from . token import user_tokenizer_generate
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.models import User
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cart.cart import Cart


# Create your views here.
# Register account
def register(request):

    form = UserForm()

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()

            # Email verification setup
            current_site = get_current_site(request)
            subject = 'Account verification email'
            message = render_to_string('accounts/email_verification.html', {

                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': user_tokenizer_generate.make_token(user)
            })

            user.email_user(subject, message)
            return redirect('email_verification_sent')
        
    context = {'form': form}
    return render(request, 'accounts/register.html', context)


def email_verification(request, uidb64, token):
    uid = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=uid)

    # Success
    if user and user_tokenizer_generate.check_token(user, token):

        user.is_active = True
        user.save()
        return redirect('email_verification_success')


    # Failed

    else:

        return redirect('email_verification_failed')

def email_verification_sent(request):
    return render(request, 'accounts/email_verification_sent.html')

def email_verification_success(request):
    return render(request, 'accounts/email_verification_success.html')

def email_verification_failed(request):
    return render(request, 'accounts/email_verification_failed.html')


def login(request):

    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
         
           username = request.POST.get('username')
           password = request.POST.get('password')

           user = authenticate(request, username=username, password=password)

           if user is not None:
              
             auth.login(request, user)
             return redirect('dashboard')
    
    context = { 'form': form }
    return render(request, 'accounts/login.html', context)


def logout(request):

    try:
    
      for key in list(request.session.keys()):

        if key == 'session_key':

            continue

        else:

            del request.session[key]

    except KeyError:
        pass
    
    messages.success(request, 'Logout successfully')
    return redirect('login')

@login_required(login_url='login')
def dashboard(request):
    return render(request, 'accounts/dashboard.html')

@login_required(login_url='login')
def update_profile(request):

    user_form = UpdateUserForm(instance=request.user)

    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)

        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Successfully updated profile')
            return redirect('dashboard')
        
    

    context = {'user_form': user_form}

    return render(request, 'accounts/update_profile.html', context)

@login_required(login_url='login')
def delete_user(request):

    user = User.objects.get(id=request.user.id)

    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Your Profile deleted successfully')
        return redirect('login')
    
    
    return render(request, 'accounts/delete_user.html')


# Shipping view
@login_required(login_url='login')
def shipping_address(request):

    try:

        shipping = ShippingAddress.objects.get(user=request.user.id)

    except ShippingAddress.DoesNotExist:

        shipping = None

    form = ShippingForm(instance=shipping)

    if request.method == 'POST':

         form = ShippingForm(request.POST, instance=shipping)

         if form.is_valid():
             shipping_user = form.save(commit=False)
             shipping_user.user = request.user
             shipping_user.save()
             return redirect('checkout')
            

    context = {'form': form}

    return render(request, 'accounts/shipping_address.html', context)


# My orders
@login_required(login_url='login')
def my_orders(request):

    try:
        cart = Cart(request)
        
        # Calculate total price
        total_price = cart.total_price()  # Get the calculated total price

        request.session['total_price'] = str(total_price)
 
        # Get the other necessary data
        orders = OrderItem.objects.filter(user=request.user)
        shipping = ShippingAddress.objects.get(user=request.user.id)
 
        # Pass the total price and other data to the context
        context = { 
            'orders': orders, 
            'shipping': shipping, 
            'cart': cart, 
            'total_price': total_price  # Pass total_price to the template
        }
 
        return render(request, 'accounts/my_orders.html', context)
 
    except Exception as e:
        print(f"Error: {e}")
        return render(request, 'accounts/my_orders.html')
