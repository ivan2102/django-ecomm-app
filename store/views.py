from django.shortcuts import render
from . models import Category, Product
from django.shortcuts import get_object_or_404

# Create your views here.
def store(request):
    products = Product.objects.all()

    context = {
        'products': products
    }
    return render(request, 'store/store.html', context)


def categories(request):
    categories = Category.objects.all()

    return { 'categories': categories }

def single_category(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)

    products = Product.objects.filter(category=category)

    context = {'category': category, 'products': products }

    return render(request, 'store/single_category.html', context)

def single_product(request, product_slug):
    single_product = get_object_or_404(Product, slug=product_slug)

    context = {
        'product': single_product
    }

    return render(request, 'store/single_product.html', context)


