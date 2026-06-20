from django.shortcuts import get_object_or_404, render
from .models import Products

def Home(request):
    return render(request, 'home.html')

def About(request):
    return render(request, 'about.html')

def AllProducts(request):
    products = Products.objects.all()
    context = {
        'products': products
    }
    return render(request, 'allproducts.html', context)

def ProductDetail(request, id):
    product = get_object_or_404(Products, id=id)
    context = {
        'product': product
    }
    return render(request, 'products.html', context)