from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', Home),
    path('about/', About),
    path('products/', AllProducts, name='all_products'),
    path('products/<int:id>/', ProductDetail, name='product_detail'),
]

