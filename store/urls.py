from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('product/<slug:product_slug>', views.single_product, name='single_product'),
    path('category/<slug:category_slug>', views.single_category, name='single_category')
]
