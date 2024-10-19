from . import views
from django.urls import path

urlpatterns = [

    path('payment_success', views.payment_success, name='payment_success'),
    path('payment_failed', views.payment_failed, name='payment_failed'),
    path('checkout', views.checkout, name='checkout'),
    path('complete-order', views.complete_order, name='complete_order')
    
]
